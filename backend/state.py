import json
from .config import settings
from supabase import create_client

def get_db():
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

def get_session(session_id: str):
    db = get_db()
    res = db.table('sessions').select('*').eq('session_id', session_id).execute()
    if not res.data:
        # Create default
        new_session = {
            "session_id": session_id,
            "layer": 1,
            "artifacts": {},
            "canonical_state": {"archivist_active": True, "guardian_target": "NONE", "bow_version": "v1"},
            "model_state": {}
        }
        db.table('sessions').insert(new_session).execute()
        return new_session
    return res.data[0]

def update_session(session_id: str, updates: dict):
    db = get_db()
    db.table('sessions').update(updates).eq('session_id', session_id).execute()
