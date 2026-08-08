import json
from pathlib import Path

DATA_PATH = Path("data/curriculum.json")


def load_curriculum():
    """
    Load complete curriculum JSON.
    """

    with open(DATA_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def get_day(day: int):
    """
    Return curriculum details for a specific day.
    """

    curriculum = load_curriculum()

    for lesson in curriculum["days"]:

        if lesson["day"] == day:
            return lesson

    return None