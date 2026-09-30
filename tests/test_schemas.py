"""Unit tests for the itinerary schema and validator.

Run with:  pytest tests/test_schemas.py -v

These need no API key and no network access -- they only exercise the pure
Python logic in schemas.py, which is exactly the code the validate node in
graph.py calls on every planner attempt.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from schemas import Activity, Day, Itinerary, validate_itinerary


def make_plan(n_days: int, cost_per_day: float) -> Itinerary:
    days = [
        Day(
            day_number=i + 1,
            theme="Sightseeing",
            activities=[Activity(time_slot="Morning", name="Visit", description="desc", est_cost=cost_per_day)],
        )
        for i in range(n_days)
    ]
    total = n_days * cost_per_day
    return Itinerary(destination="Goa", total_budget=total, estimated_total=total, days=days)


def test_valid_plan_has_no_problems():
    plan = make_plan(2, 500)
    assert validate_itinerary(plan, expected_days=2, budget=2000) == []


def test_wrong_day_count_is_caught():
    plan = make_plan(2, 500)
    problems = validate_itinerary(plan, expected_days=3, budget=2000)
    assert any("Expected 3 day" in p for p in problems)


def test_over_budget_is_caught():
    plan = make_plan(2, 700)  # total 1400
    problems = validate_itinerary(plan, expected_days=2, budget=1000)
    assert any("above the budget" in p for p in problems)


def test_stale_estimated_total_is_caught():
    plan = make_plan(2, 500)  # real total 1000
    plan.estimated_total = 100  # deliberately wrong
    problems = validate_itinerary(plan, expected_days=2, budget=2000)
    assert any("estimated_total" in p for p in problems)


def test_empty_day_is_caught():
    day = Day(day_number=1, theme="Empty", activities=[])
    plan = Itinerary(destination="Goa", total_budget=1000, estimated_total=0, days=[day])
    problems = validate_itinerary(plan, expected_days=1, budget=1000)
    assert any("no activities" in p for p in problems)


def test_malformed_json_raises_before_validation():
    import pytest

    with pytest.raises(Exception):
        Itinerary.model_validate_json('{"destination": "X", "days": "not-a-list"}')


if __name__ == "__main__":
    test_valid_plan_has_no_problems()
    test_wrong_day_count_is_caught()
    test_over_budget_is_caught()
    test_stale_estimated_total_is_caught()
    test_empty_day_is_caught()
    print("All schema tests passed.")
