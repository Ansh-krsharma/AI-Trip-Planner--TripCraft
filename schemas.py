"""Pydantic schema for the itinerary the planner node returns, plus the
rule-based validator the validate node runs against it.

Keeping the schema and the validator in one file with no LangGraph or
Streamlit imports means both can be unit-tested (see tests/test_schemas.py)
without needing an API key or network access.
"""
from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class Activity(BaseModel):
    time_slot: str = Field(..., description="e.g. 'Morning', '9:00 AM'")
    name: str
    description: str
    est_cost: float = Field(..., ge=0)
    source_doc: Optional[str] = Field(
        default=None, description="Destination guide this suggestion was grounded in"
    )


class Day(BaseModel):
    day_number: int = Field(..., ge=1)
    theme: str
    activities: list[Activity]


class Itinerary(BaseModel):
    destination: str
    total_budget: float = Field(..., ge=0)
    estimated_total: float = Field(..., ge=0)
    days: list[Day]


def validate_itinerary(plan: Itinerary, expected_days: int, budget: float) -> list[str]:
    """Rule-based checks the LLM's JSON output must pass.

    Returns a list of human-readable problems. An empty list means the plan
    is valid. This is intentionally simple and deterministic -- no second
    LLM call is used to grade the first one.
    """
    problems: list[str] = []

    if len(plan.days) != expected_days:
        problems.append(
            f"Expected {expected_days} day(s), got {len(plan.days)}."
        )

    seen_days = sorted(d.day_number for d in plan.days)
    if seen_days != list(range(1, len(plan.days) + 1)):
        problems.append(
            f"day_number values should run 1..{len(plan.days)} with no gaps or repeats, got {seen_days}."
        )

    for d in plan.days:
        if not d.activities:
            problems.append(f"Day {d.day_number} has no activities.")

    total = sum(a.est_cost for d in plan.days for a in d.activities)
    if budget and total > budget:
        problems.append(
            f"Estimated total Rs. {total:,.0f} is above the budget Rs. {budget:,.0f}."
        )

    # The model can report a stale estimated_total that doesn't match the
    # activities it actually listed -- catch drift beyond a small tolerance.
    if total > 0 and abs(total - plan.estimated_total) > max(50.0, 0.05 * total):
        problems.append(
            "The estimated_total field does not match the sum of activity costs."
        )

    return problems
