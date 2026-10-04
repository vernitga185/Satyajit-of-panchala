from fastapi.testclient import TestClient
from main import app

client = TestClient(app)
r2 = client.post("/api/eleventh/init")
sid2 = r2.json()["session_id"]

r_search = client.post("/api/eleventh/chat", json={"session_id": sid2, "message": "search for Bhurishravas"})
print("Eleventh RAG:", r_search.status_code, r_search.text)
