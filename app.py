import os

import streamlit as st
from dotenv import load_dotenv

from data.guides import DESTINATION_NAMES
from graph import build_graph
load_dotenv()
st.set_page_config(page_title="TripCraft AI", page_icon="🧭", layout="wide")


def get_api_key() -> str:
    try:
        if "GROQ_API_KEY" in st.secrets:
            return st.secrets["GROQ_API_KEY"]
    except Exception:
        pass
    return os.environ.get("GROQ_API_KEY", "")


API_KEY = get_api_key()

st.title("🧭 TripCraft AI")
st.caption(
    "An agentic travel planner that checks every itinerary against your "
    "budget and trip length before showing it to you."
)

if not API_KEY:
    st.error(
        "No Groq API key found. Copy .env.example to .env and set GROQ_API_KEY "
        "(for local runs), or add GROQ_API_KEY to Streamlit secrets (for a "
        "deployed app), then restart."
    )
    st.stop()


@st.cache_resource(show_spinner="Setting up the knowledge base...")
def get_app_graph(api_key: str):
    return build_graph(api_key)


app = get_app_graph(API_KEY)

with st.sidebar:
    st.header("Trip preferences")
    destination = st.selectbox("Destination", DESTINATION_NAMES)
    days = st.number_input("Number of days", min_value=1, max_value=7, value=3)
    budget = st.number_input(
        "Total budget (INR)", min_value=500, max_value=200000, value=12000, step=500
    )
    interests = st.text_input(
        "Interests (optional)", placeholder="e.g. food, trekking, temples"
    )
    plan_clicked = st.button("Plan my trip", type="primary", use_container_width=True)
    st.divider()
    st.caption("Knowledge base covers: " + ", ".join(DESTINATION_NAMES))
    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []  # each: {"role", "content", optional "plan"}


def render_itinerary(plan_dict: dict) -> None:
    st.subheader(f"{plan_dict.get('destination', '')} itinerary")
    total = plan_dict.get("estimated_total", 0) or 0
    budget_val = plan_dict.get("total_budget", 0) or 0
    c1, c2 = st.columns(2)
    c1.metric("Estimated total", f"Rs. {total:,.0f}")
    c2.metric("Budget", f"Rs. {budget_val:,.0f}", delta=f"Rs. {budget_val - total:,.0f} left")

    for day in plan_dict.get("days", []):
        with st.expander(f"Day {day.get('day_number')} — {day.get('theme', '')}", expanded=True):
            for act in day.get("activities", []):
                line = (
                    f"**{act.get('time_slot', '')} — {act.get('name', '')}**  \n"
                    f"{act.get('description', '')}  \n"
                    f"Est. cost: Rs. {act.get('est_cost', 0):,.0f}"
                )
                if act.get("source_doc"):
                    line += f"  ·  Source: {act['source_doc']}"
                st.markdown(line)


def run_request(question: str) -> dict:
    history = st.session_state.messages[-6:]
    state = {
        "question": question,
        "history": history,
        "destination": destination,
        "days": int(days),
        "budget": float(budget),
        "interests": interests,
        "retries": 0,
        "problems": [],
    }
    with st.spinner("Planning..."):
        return app.invoke(state)


for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["role"] == "assistant" and msg.get("plan"):
            render_itinerary(msg["plan"])
        else:
            st.write(msg["content"])

user_input = st.chat_input('Ask for a plan, e.g. "Plan 3 days in Goa", or a follow-up question')

question = None
if plan_clicked:
    question = (
        f"Plan {int(days)} days in {destination} under Rs. {int(budget)}. "
        f"Interests: {interests or 'general sightseeing'}."
    )
elif user_input:
    question = user_input

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)

    result = run_request(question)

    with st.chat_message("assistant"):
        plan = result.get("plan")
        if plan:
            plan_dict = plan.model_dump()
            render_itinerary(plan_dict)
            if result.get("retries", 0) > 1:
                st.caption(f"(Needed {result['retries']} attempt(s) to pass validation.)")
            st.session_state.messages.append(
                {"role": "assistant", "content": "Here is your itinerary.", "plan": plan_dict}
            )
        else:
            answer = result.get("final_answer") or (
                "I couldn't produce a valid itinerary from that. Could you try rephrasing?"
            )
            st.write(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
