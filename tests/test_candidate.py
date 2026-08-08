from retriever.candidate import (
    get_candidate,
    get_completed_days,
)

candidate = get_candidate("CAND-001")

print("Candidate Name:")
print(candidate["member"]["name"])

print("\nCompleted Days:")
print(get_completed_days("CAND-001"))