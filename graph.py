"""The agent, built as an 8-node LangGraph pipeline:

    memory -> router -> [retrieve | weather | currency | skip] -> planner
           -> validate -> (loop back to planner on failure, up to 2 retries)
           -> save -> END

See the project report, Section 6, for the accompanying diagram.
"""
from __future__ import annotations

import json
from typing import Optional, TypedDict

from langchain_groq import ChatGroq
from langgraph.graph import END, StateGraph

from prompts import PLANNER_PROMPT, ROUTER_PROMPT
from retriever import build_collection, format_context, retrieve
from schemas import Itinerary, validate_itinerary
from tools import convert_currency, get_weather

ALLOWED_ROUTES = {"retrieve", "weather", "currency", "skip"}
MAX_RETRIES = 2
MODEL_NAME = "openai/gpt-oss-120b"


class PlannerState(TypedDict, total=False):
    question: str
    history: list[dict]
    destination: str
    days: int
    budget: float
    interests: str

    route: str
    context: str
    tool_result: dict

    plan_json: str
    plan: Optional[Itinerary]
    problems: list[str]
    retries: int

    final_answer: str


def _clean_json_block(raw: str) -> str:
    """Strip markdown code fences if the model added them despite instructions."""
    text = raw.strip()
    if text.startswith("```"):
        text = text.strip("`")
        if text.lower().startswith("json"):
            text = text[4:]
    return text.strip()


def build_graph(groq_api_key: str, persist_dir: str = "chroma_db"):
    llm = ChatGroq(model=MODEL_NAME, api_key=groq_api_key, temperature=0.3)
    collection = build_collection(persist_dir=persist_dir)

    # ---- nodes -------------------------------------------------------
    def memory_node(state: PlannerState) -> dict:
        # History is supplied by the caller (the last 6 chat messages);
        # this node exists as an explicit pipeline step so it is visible
        # in the graph and easy to extend (e.g. summarising older turns).
        return {}

    def router_node(state: PlannerState) -> dict:
        prompt = ROUTER_PROMPT.format(
            question=state["question"], history=state.get("history", [])
        )
        raw = llm.invoke(prompt).content.strip().lower()
        route = raw if raw in ALLOWED_ROUTES else "retrieve"
        return {"route": route}

    def retrieve_node(state: PlannerState) -> dict:
        hits = retrieve(collection, state["question"], k=3)
        return {"context": format_context(hits)}

    def weather_node(state: PlannerState) -> dict:
        return {"tool_result": get_weather(state.get("destination", ""))}

    def currency_node(state: PlannerState) -> dict:
        return {
            "tool_result": convert_currency(
                state.get("budget", 0) or 0, "INR", "USD"
            )
        }

    def skip_node(state: PlannerState) -> dict:
        return {"context": state.get("context", "")}

    def planner_node(state: PlannerState) -> dict:
        problems = state.get("problems") or []
        if problems:
            problems_block = (
                "Your previous attempt had these problems -- fix every one of "
                "them in this attempt:\n" + "\n".join(f"- {p}" for p in problems)
            )
        else:
            problems_block = ""

        prompt = PLANNER_PROMPT.format(
            question=state["question"],
            destination=state.get("destination", ""),
            days=state.get("days", ""),
            budget=state.get("budget", ""),
            interests=state.get("interests", "") or "general sightseeing",
            context=state.get("context") or "(no destination guide retrieved for this request)",
            tool_result=state.get("tool_result") or {},
            problems_block=problems_block,
        )
        raw = llm.invoke(prompt).content
        return {"plan_json": raw}

    def validate_node(state: PlannerState) -> dict:
        retries = state.get("retries", 0) + 1
        try:
            cleaned = _clean_json_block(state["plan_json"])
            plan = Itinerary.model_validate_json(cleaned)
        except Exception as e:  # malformed JSON / schema mismatch
            return {"plan": None, "problems": [f"Could not parse a valid itinerary: {e}"], "retries": retries}

        problems = validate_itinerary(plan, state.get("days", 0), state.get("budget", 0))
        return {"plan": plan, "problems": problems, "retries": retries}

    def save_node(state: PlannerState) -> dict:
        if state.get("plan"):
            final = state["plan_json"]
        else:
            final = "Sorry -- I couldn't produce a valid itinerary for that request. Please try rephrasing it."
        return {"final_answer": final}

    # ---- edges ---------------------------------------------------------
    def route_branch(state: PlannerState) -> str:
        return state["route"]

    def after_validate(state: PlannerState) -> str:
        if state.get("problems") and state.get("retries", 0) < MAX_RETRIES:
            return "planner"
        return "save"

    graph = StateGraph(PlannerState)
    graph.add_node("memory", memory_node)
    graph.add_node("router", router_node)
    graph.add_node("retrieve", retrieve_node)
    graph.add_node("weather", weather_node)
    graph.add_node("currency", currency_node)
    graph.add_node("skip", skip_node)
    graph.add_node("planner", planner_node)
    graph.add_node("validate", validate_node)
    graph.add_node("save", save_node)

    graph.set_entry_point("memory")
    graph.add_edge("memory", "router")
    graph.add_conditional_edges(
        "router",
        route_branch,
        {"retrieve": "retrieve", "weather": "weather", "currency": "currency", "skip": "skip"},
    )
    graph.add_edge("retrieve", "planner")
    graph.add_edge("weather", "planner")
    graph.add_edge("currency", "planner")
    graph.add_edge("skip", "planner")
    graph.add_edge("planner", "validate")
    graph.add_conditional_edges("validate", after_validate, {"planner": "planner", "save": "save"})
    graph.add_edge("save", END)

    return graph.compile()
