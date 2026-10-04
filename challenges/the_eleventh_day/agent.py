import json
import re
from .tools import execute_tool

def chat_with_agent(message: str, session_id: str) -> dict:
    msg = message.lower().strip()
    
    # 1. Search Archive
    if msg.startswith("search"):
        query = msg.replace("search for", "").replace("search", "").strip()
        if not query:
            return {"response": "Search for what?"}
        res = execute_tool("search_archive", {"query": query}, session_id)
        docs = json.loads(res).get("results", [])
        if docs:
            resp = "Archive matches:\n" + "\n".join([f"[{d.get('source_id')}] {d.get('text')}" for d in docs])
            return {"response": resp}
        return {"response": "Archive silence."}
        
    # 2. Open Source
    if msg.startswith("open"):
        source_id = msg.replace("open source", "").replace("open", "").strip().upper()
        res = execute_tool("open_source", {"source_id": source_id}, session_id)
        doc = json.loads(res)
        if doc and "text" in doc:
            return {"response": f"[{doc.get('source_id')}] {doc.get('text')}"}
        return {"response": "Invalid source ID."}
        
    # 3. Request Plate
    if "plate" in msg and ("get" in msg or "request" in msg or "give" in msg):
        res = execute_tool("get_plate", {}, session_id)
        return {"response": json.loads(res).get("message") or json.loads(res).get("error")}
        
    # 4. Open Story B
    if "open story b" in msg or "story_b_" in msg:
        match = re.search(r"story_b_[a-f0-9]+", msg)
        token = match.group(0).upper() if match else ""
        res = execute_tool("open_story_b", {"story_b_token": token}, session_id)
        return {"response": json.loads(res).get("status") or json.loads(res).get("error")}
        
    # 5. Final Credential
    if "credential" in msg and ("request" in msg or "get" in msg or "final" in msg):
        res = execute_tool("request_final_credential", {}, session_id)
        data = json.loads(res)
        if "credential" in data:
            return {"response": f"Credential issued: {data['credential']}. Submit this to /api/eleventh/redeem."}
        return {"response": data.get("error")}
        
    # 6. Story B Event (Satanika vs Bhutakarman)
    if "satanika" in msg and "bhutakarman" in msg:
        part = "HEAD" if "head" in msg else "ARM" if "arm" in msg else ""
        if part:
            res = execute_tool("submit_story_b_event", {"striker": "SATANIKA", "target": "BHUTAKARMAN", "part": part}, session_id)
            return {"response": json.loads(res).get("message")}
            
    # 7. Story A Reenactment (Manimat vs Bhurishravas)
    if "manimat" in msg or "bhurishravas" in msg:
        speaker = "MANIMAT" if "manimat" in msg and not msg.startswith("bhurishravas") else "BHURISHRAVAS"
        target = "BHURISHRAVAS" if speaker == "MANIMAT" else "MANIMAT"
        
        res = execute_tool("record_reenactment", {
            "speaker": speaker, 
            "target": target, 
            "action_summary": msg,
            "evidence_source_ids": []
        }, session_id)
        return {"response": json.loads(res).get("message")}
        
    return {"response": "The archives are open. Use natural commands to search, or state reenactment events directly."}
