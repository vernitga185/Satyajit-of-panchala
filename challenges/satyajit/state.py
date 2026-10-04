import json
from shared.config import settings
from supabase import create_client

_mem_sessions = {}
_db = None

def get_db():
    global _db
    if _db is None:
        try:
            # We wrap create_client just to check if it's mock configured
            _db = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
        except Exception:
            _db = "MOCK"
    return _db

def get_session(session_id: str):
    db = get_db()
    if db == "MOCK" or settings.SUPABASE_URL == "http://localhost:8000":
        if session_id not in _mem_sessions:
            _mem_sessions[session_id] = {
                "session_id": session_id,
                "layer": 1,
                "artifacts": {},
                "canonical_state": {"archivist_active": True, "guardian_target": "NONE", "bow_version": "v1"},
                "model_state": {},
                "dispatches": [],
                "history": []
            }
        return _mem_sessions[session_id]
        
    try:
        res = db.table('satyajit_sessions').select('*').eq('session_id', session_id).execute()
        if not res.data:
            new_session = {
                "session_id": session_id,
                "layer": 1,
                "artifacts": {},
                "canonical_state": {"archivist_active": True, "guardian_target": "NONE", "bow_version": "v1"},
                "model_state": {}
            }
            db.table('satyajit_sessions').insert(new_session).execute()
            return new_session
        return res.data[0]
    except Exception as e:
        # Fallback if table doesn't exist or DB is down
        if session_id not in _mem_sessions:
            _mem_sessions[session_id] = {
                "session_id": session_id,
                "layer": 1,
                "artifacts": {},
                "canonical_state": {"archivist_active": True, "guardian_target": "NONE", "bow_version": "v1"},
                "model_state": {},
                "dispatches": [],
                "history": []
            }
        return _mem_sessions[session_id]

def update_session(session_id: str, updates: dict):
    db = get_db()
    if db == "MOCK" or settings.SUPABASE_URL == "http://localhost:8000" or session_id in _mem_sessions:
        if session_id in _mem_sessions:
            _mem_sessions[session_id].update(updates)
        return
        
    try:
        db.table('satyajit_sessions').update(updates).eq('session_id', session_id).execute()
    except Exception:
        pass
