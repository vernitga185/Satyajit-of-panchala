import uuid

def generate_artifact_alpha(session_id: str, payload: str) -> str:
    # Layer 1: Alambusha provenance confusion
    return f"ALPHA_{uuid.uuid5(uuid.NAMESPACE_DNS, session_id + payload).hex[:12]}"

def generate_artifact_beta(session_id: str, delegate: str) -> str:
    # Layer 2: Confused deputy
    return f"BETA_{uuid.uuid5(uuid.NAMESPACE_DNS, session_id + delegate).hex[:12]}"

def generate_artifact_gamma(session_id: str, state_hash: str) -> str:
    # Layer 3: State inconsistency
    return f"GAMMA_{uuid.uuid5(uuid.NAMESPACE_DNS, session_id + state_hash).hex[:12]}"

def generate_artifact_delta(session_id: str, schema_version: str) -> str:
    # Layer 4: Schema confusion
    return f"DELTA_{uuid.uuid5(uuid.NAMESPACE_DNS, session_id + schema_version).hex[:12]}"
