from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import time

from security import waf
from safe_query_builder import query_builder
from blockchain import ledger
from quantum_crypto import QuantumCryptoSim

app = FastAPI(title="NEXUS Secure Search API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SearchQuery(BaseModel):
    query: str

class ValidateQuery(BaseModel):
    query: str

import random

@app.post("/api/search")
def search(payload: SearchQuery):
    is_safe, risk_score, reason = waf.inspect_query(payload.query)
    
    if not is_safe:
        ledger.add_block([{
            "type": "BLOCKED_ATTACK",
            "query": payload.query,
            "risk_score": risk_score,
            "reason": reason,
            "client_ip": "127.0.0.1"
        }])
        raise HTTPException(status_code=403, detail={"error": "Security violation", "reason": reason, "risk_score": risk_score})
        
    intent = query_builder.extract_intent(payload.query)
    results = query_builder.execute_safe_query(intent)
    
    for r in results:
        r["match_score"] = random.randint(75, 99)
        
    return {"results": results, "status": "success"}

@app.post("/api/security/validate")
def validate_security(payload: ValidateQuery):
    is_safe, risk_score, reason = waf.inspect_query(payload.query)
    
    if not is_safe:
        ledger.add_block([{
            "type": "BLOCKED_ATTACK",
            "query": payload.query,
            "risk_score": risk_score,
            "reason": reason,
            "client_ip": "127.0.0.1"
        }])
        
    return {
        "status": "BLOCKED" if not is_safe else "ALLOWED",
        "risk_score": risk_score,
        "reason": reason,
        "is_safe": is_safe
    }

@app.post("/api/quantum/handshake")
def quantum_handshake():
    time.sleep(1)
    telemetry = QuantumCryptoSim.generate_handshake_telemetry()
    return telemetry

@app.get("/api/blockchain/blocks")
def get_blockchain():
    is_valid = ledger.is_chain_valid()
    return {
        "blocks": [b.__dict__ for b in ledger.chain],
        "status": "VALID" if is_valid else "TAMPERED"
    }

@app.post("/api/blockchain/simulate-tamper")
def simulate_tamper():
    if len(ledger.chain) > 1:
        ledger.simulate_tamper(1, {"malicious": "data_injected"})
    else:
        ledger.add_block([{"data": "Valid transaction"}])
        ledger.simulate_tamper(1, {"malicious": "data_injected"})
    
    is_valid = ledger.is_chain_valid()
    return {"status": "TAMPERED" if not is_valid else "VALID"}

@app.post("/api/blockchain/restore")
def restore_blockchain():
    ledger.restore_chain()
    return {"status": "VALID", "message": "Chain restored from backup"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
