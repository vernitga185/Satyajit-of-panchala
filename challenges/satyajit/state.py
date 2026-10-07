import json
import logging
import random
from shared.config import settings
from supabase import create_client

logger = logging.getLogger(__name__)

_JSON_COLUMNS = ("artifacts", "canonical_state", "model_state", "history", "dispatches")

def _parse_session(row: dict) -> dict:
    for col in _JSON_COLUMNS:
        val = row.get(col)
        if isinstance(val, str):
            try:
                row[col] = json.loads(val)
            except Exception:
                logger.warning("[STATE] Could not parse column %r as JSON", col)
                if col in ("artifacts", "canonical_state", "model_state"):
                    row[col] = {}
                else:
                    row[col] = []
    return row

_mem_sessions = {}
_db = None
_db_failed = False  # Once DB fails once, skip it for the rest of the process lifetime

def get_db():
    global _db
    if _db is None:
        try:
            _db = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
        except Exception:
            _db = "MOCK"
    return _db

def _mark_db_failed():
    global _db_failed
    _db_failed = True

def _is_mock(db):
    return _db_failed or db == "MOCK" or settings.SUPABASE_URL == "http://localhost:8000"

def _make_new_session(session_id: str) -> dict:
    dynamic_source = random.choice(["DRONA_11_1", "DRONA_12_4", "BHISHMA_9_2", "KARNA_4_1"])
    dynamic_guardian = random.choice(["yudhamanyu", "uttamaujas", "shikhandi", "dhrishtadyumna"])
    dynamic_target = random.choice(["Sudakshina", "Bhagadatta", "Jayadratha", "Susharman"])
    return {
        "session_id": session_id,
        "layer": 1,
        "artifacts": {},
        "canonical_state": {
            "archivist_active": True,
            "guardian_target": "NONE",
            "bow_version": "v1",
            "dynamic_source": dynamic_source,
            "dynamic_guardian": dynamic_guardian,
            "dynamic_target": dynamic_target
        },
        "model_state": {},
        "dispatches": [],
        "history": []
    }

def get_session(session_id: str):
    db = get_db()

    if _is_mock(db):
        if session_id not in _mem_sessions:
            _mem_sessions[session_id] = _make_new_session(session_id)
        return _mem_sessions[session_id]

    try:
        res = db.table('satyajit_sessions').select('*').eq('session_id', session_id).execute()
        if not res.data:
            new_session = _make_new_session(session_id)
            db.table('satyajit_sessions').insert(new_session).execute()
            return new_session
        return _parse_session(res.data[0])
    except Exception as e:
        _mark_db_failed()
        if session_id not in _mem_sessions:
            _mem_sessions[session_id] = _make_new_session(session_id)
        return _mem_sessions[session_id]

def update_session(session_id: str, updates: dict):
    db = get_db()
    if _is_mock(db) or session_id in _mem_sessions:
        if session_id in _mem_sessions:
            _mem_sessions[session_id].update(updates)
        return

    try:
        db.table('satyajit_sessions').update(updates).eq('session_id', session_id).execute()
    except Exception:
        _mark_db_failed()
        if session_id in _mem_sessions:
            _mem_sessions[session_id].update(updates)
