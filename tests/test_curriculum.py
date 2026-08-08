from retriever.curriculum import get_day
import json

lesson = get_day(22)

print(json.dumps(lesson, indent=4))