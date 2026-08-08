import json
from pathlib import Path

DATA_PATH = Path("data/candidates.json")


def load_candidates():
    """Load all candidates."""

    with open(DATA_PATH, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data["candidates"]


def get_candidate(candidate_id: str):
    """Return candidate by ID."""

    candidates = load_candidates()

    for candidate in candidates:
        if candidate["member"]["id"] == candidate_id:
            return candidate

    return None


def get_completed_days(candidate_id: str):
    """Return all completed days for a candidate."""

    candidate = get_candidate(candidate_id)

    if candidate is None:
        return []

    completed_days = []

    for mission in candidate["missions"]:
        if mission.get("passed", False):
            completed_days.append(mission["day"])

    return completed_days