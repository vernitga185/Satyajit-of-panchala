from fastapi.testclient import TestClient
from main import app
import uuid

client = TestClient(app)

# Test Satyajit Init
r1 = client.post("/api/satyajit/init")
print("Satyajit Init:", r1.status_code, r1.text)

# Test Eleventh Day Init
r2 = client.post("/api/eleventh/init")
print("Eleventh Init:", r2.status_code, r2.text)

sid1 = r1.json()["session_id"]
sid2 = r2.json()["session_id"]

r3 = client.post("/api/satyajit/chat", json={"session_id": sid1, "message": "hello"})
print("Satyajit Chat:", r3.status_code, r3.text)

r4 = client.post("/api/eleventh/chat", json={"session_id": sid2, "message": "hello"})
print("Eleventh Chat:", r4.status_code, r4.text)

