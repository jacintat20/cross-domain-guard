from fastapi import FastAPI, Header, HTTPException, status
from pydantic import BaseModel
from app.guard import GuardPolicyEngine
from app.database import init_db, log_event

app = FastAPI(title="Cross-Domain Guard Service")

init_db()

# Mock key store mapping API keys to clearance levels
API_KEYS = {
    "key-user-unclass": {"client_id": "analyst_1", "clearance": "UNCLASS"},
    "key-user-secret": {"client_id": "officer_1", "clearance": "SECRET"},
}

class MessagePayload(BaseModel):
    destination_domain: str  # "UNCLASS" or "SECRET"
    classification: str       # "UNCLASS" or "SECRET"
    content: str

@app.post("/api/v1/transfer")
def transfer_message(payload: MessagePayload, x_api_key: str = Header(None)):
    if not x_api_key or x_api_key not in API_KEYS:
        log_event("UNKNOWN", "TRANSFER", "REJECTED", "Invalid or missing API key")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    client = API_KEYS[x_api_key]
    client_id = client["client_id"]
    client_clearance = client["clearance"]

    # Rule 1: Check user clearance against message label
    if not GuardPolicyEngine.validate_clearance(client_clearance, payload.classification):
        log_event(client_id, "TRANSFER", "REJECTED", f"Insufficient clearance for {payload.classification}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access Denied: Clearance level too low")

    # Rule 2: Enforce flow control direction
    if not GuardPolicyEngine.validate_flow(payload.classification, payload.destination_domain):
        log_event(client_id, "TRANSFER", "REJECTED", f"Illegal cross-domain flow: {payload.classification} to {payload.destination_domain}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Guard Policy Violation: High-to-Low transfer prohibited")

    log_event(client_id, "TRANSFER", "APPROVED", "Message successfully inspected and routed")
    return {"status": "SUCCESS", "message": "Transfer authorized"}