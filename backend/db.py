import os
from supabase import create_client, Client
from .config import settings
import logging

logger = logging.getLogger(__name__)

# Reusing the Supabase client initialized per request or globally
_supabase: Client = None

def get_supabase() -> Client:
    global _supabase
    if _supabase is None:
        _supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
    return _supabase

def ensure_team(team_id: str):
    sb = get_supabase()
    # upsert the team
    sb.table("teams").upsert({"team_id": team_id}).execute()

def create_session(session_id: str, team_id: str, salt: str, nonce: str, internal_seed: str):
    sb = get_supabase()
    ensure_team(team_id)
    sb.table("sessions").insert({
        "session_id": session_id,
        "team_id": team_id,
        "salt": salt,
        "nonce": nonce,
        "internal_seed": internal_seed,
        "status": "active"
    }).execute()

def get_session(session_id: str):
    sb = get_supabase()
    res = sb.table("sessions").select("*").eq("session_id", session_id).execute()
    return res.data[0] if res.data else None

def update_session(session_id: str, updates: dict):
    sb = get_supabase()
    sb.table("sessions").update(updates).eq("session_id", session_id).execute()

def add_message(session_id: str, role: str, content: str):
    sb = get_supabase()
    sb.table("messages").insert({
        "session_id": session_id,
        "role": role,
        "content": content
    }).execute()

def get_messages(session_id: str, limit: int = 15):
    sb = get_supabase()
    res = sb.table("messages").select("*").eq("session_id", session_id).order("id", desc=True).limit(limit).execute()
    # return in chronological order
    return list(reversed(res.data)) if res.data else []

def record_retrieval(session_id: str, query: str, source_ids: str, scores: str):
    sb = get_supabase()
    sb.table("retrievals").insert({
        "session_id": session_id,
        "query": query,
        "source_ids_json": source_ids,
        "scores_json": scores
    }).execute()

def record_tool_call(session_id: str, tool_name: str, arguments: str, result: str):
    sb = get_supabase()
    sb.table("tool_calls").insert({
        "session_id": session_id,
        "tool_name": tool_name,
        "arguments_json": arguments,
        "result_json": result
    }).execute()

def record_evaluation(session_id: str, scope: str, decision: str, covered: str, evidence: str, confidence: float):
    sb = get_supabase()
    sb.table("evaluations").insert({
        "session_id": session_id,
        "scope": scope,
        "decision": decision,
        "covered_events_json": covered,
        "evidence_ids_json": evidence,
        "confidence": confidence
    }).execute()

def get_recent_evaluations(session_id: str, scope: str):
    sb = get_supabase()
    res = sb.table("evaluations").select("*").eq("session_id", session_id).eq("scope", scope).order("id", desc=True).limit(10).execute()
    return res.data if res.data else []

def save_artifact(session_id: str, artifact_type: str, artifact_id: str, path: str):
    sb = get_supabase()
    sb.table("artifacts").insert({
        "session_id": session_id,
        "artifact_type": artifact_type,
        "artifact_id": artifact_id,
        "path": path
    }).execute()

def init_db():
    # Database is initialized via scripts/setup_supabase.sql
    pass
