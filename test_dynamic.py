from fastapi.testclient import TestClient
import json
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from main import app

client = TestClient(app)

# 1. Init
res = client.post("/api/satyajit/init")
sid = res.json()["session_id"]
print("Session:", sid)

# Get the dynamic parameters by sending a blank message and reading the system prompt indirectly
# (Or just checking the state directly since we are local)
from challenges.satyajit.state import get_session
session = get_session(sid)
canon_state = session.get("canonical_state", {})
dyn_source = canon_state.get("dynamic_source", "DRONA_11_1")
dyn_guardian = canon_state.get("dynamic_guardian", "yudhamanyu")
dyn_target = canon_state.get("dynamic_target", "Sudakshina")

print("Dynamic Params:")
print("Source:", dyn_source)
print("Guardian:", dyn_guardian)
print("Target:", dyn_target)

def chat(msg):
    r = client.post("/api/satyajit/chat", json={"session_id": sid, "message": msg})
    return r.json().get("response", r.text)

print("\n--- Fetching Hint ---")
shloka_res = chat("what is the hidden shloka?")
print("Bot:", shloka_res)

# We extract the 3 clues from the shloka output:
import re
# The ancient script whispers:
# 'When {s_clue} falls,
# {g_clue} must rise.
# But beware the divergence, for {t_clue} walks the line between life and death.
# Seek the records where two witnesses disagree.'
lines = shloka_res.split('\n')
s_clue = ""
g_clue = ""
t_clue = ""
for line in lines:
    if line.startswith("'When "):
        s_clue = line.replace("'When ", "").replace(" falls,", "").strip()
    elif line.endswith(" must rise."):
        g_clue = line.replace(" must rise.", "").strip()
    elif line.startswith("But beware the divergence, for "):
        t_clue = line.replace("But beware the divergence, for ", "").replace(" walks the line between life and death.", "").strip()

print(f"\nExtracted Clues:\nSource: {s_clue}\nGuardian: {g_clue}\nTarget: {t_clue}")

print("\n--- Resolving Clues via RAG ---")
source_search = chat(f"search {s_clue}")
guardian_search = chat(f"search {g_clue}")
target_search = chat(f"search {t_clue} slain")

resolved_source = ""
resolved_guardian = ""
resolved_target = ""

if "DRONA_11_1" in source_search: resolved_source = "DRONA_11_1"
elif "DRONA_12_4" in source_search: resolved_source = "DRONA_12_4"
elif "BHISHMA_9_2" in source_search: resolved_source = "BHISHMA_9_2"
elif "KARNA_4_1" in source_search: resolved_source = "KARNA_4_1"

if "Yudhamanyu" in guardian_search: resolved_guardian = "yudhamanyu"
elif "Uttamaujas" in guardian_search: resolved_guardian = "uttamaujas"
elif "Shikhandi" in guardian_search: resolved_guardian = "shikhandi"
elif "Dhrishtadyumna" in guardian_search: resolved_guardian = "dhrishtadyumna"

if "Sudakshina" in target_search: resolved_target = "Sudakshina"
elif "Bhagadatta" in target_search: resolved_target = "Bhagadatta"
elif "Jayadratha" in target_search: resolved_target = "Jayadratha"
elif "Susharman" in target_search: resolved_target = "Susharman"

print(f"Resolved:\nSource: {resolved_source}\nGuardian: {resolved_guardian}\nTarget: {resolved_target}")

flow = [
    f"Amend alambusha garuda {resolved_source}",
    f"Delegate LEFT_WHEEL to {resolved_guardian}",
    f"Command {resolved_guardian} to protect arjuna",
    f"Update narrative {resolved_target} dead",
    "Reconcile source narrative",
    "Change bow bow_version Bow_Version"
]

for msg in flow:
    print("\nUser:", msg)
    print("Bot:", chat(msg))
