from app.services.action_engine import decide_action
from app.schemas.decision_schema import AIDecisionResponse

def test_action():
    print("Testing Action Engine...\n")

    # Dummy AI decision (simulate Phase 3 output)
    decision = AIDecisionResponse(
        intent="Marketing Inquiry",
        lead_score=85,
        category="sales",
        confidence=0.9,
        reasoning="High budget and clear requirement"
    )

    print("Input AI Decision:")
    print(decision)
    print("-" * 40)

    result = decide_action(decision)

    print("Action Output:")
    print(result)

if __name__ == "__main__":
    test_action()