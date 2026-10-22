from app.guard import GuardPolicyEngine

def test_clearance_enforcement():
    assert GuardPolicyEngine.validate_clearance("SECRET", "UNCLASS") is True
    assert GuardPolicyEngine.validate_clearance("UNCLASS", "SECRET") is False

def test_flow_control():
    assert GuardPolicyEngine.validate_flow("UNCLASS", "SECRET") is True  # Low to High allowed
    assert GuardPolicyEngine.validate_flow("SECRET", "UNCLASS") is False # High to Low blocked