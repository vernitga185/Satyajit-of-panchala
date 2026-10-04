import os
import json
import hashlib
import base64
import logging
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

logger = logging.getLogger(__name__)

# ------------------------------------------------------------------
# CANONICAL ARTIFACT SERIALIZATION
# Single source of truth for how artifacts are ordered and encoded
# into key material. Used identically at generation AND redemption.
# ------------------------------------------------------------------

def canonicalize_artifacts(artifacts) -> dict:
    """
    Defensively parse artifacts from any storage representation.
    Supabase may return JSON columns as a Python string (varchar/text)
    rather than a dict (jsonb). This function always returns a plain dict.
    """
    if isinstance(artifacts, str):
        try:
            artifacts = json.loads(artifacts)
        except Exception:
            artifacts = {}
    if not isinstance(artifacts, dict):
        artifacts = {}
    return artifacts

def artifact_material(artifacts) -> bytes:
    """
    Canonical serialization of artifact dict -> bytes for HKDF.
    Order: alpha:beta:gamma:delta
    Any missing artifact becomes an empty string (no padding).
    This is the ONLY place that defines the material format.
    """
    a_dict = canonicalize_artifacts(artifacts)
    a = a_dict.get("alpha", "")
    b = a_dict.get("beta", "")
    g = a_dict.get("gamma", "")
    d = a_dict.get("delta", "")
    return f"{a}:{b}:{g}:{d}".encode("utf-8")

# ------------------------------------------------------------------
# CANONICAL KEY DERIVATION
# Single function used both at generation and at /redeem.
# ------------------------------------------------------------------

def derive_satyajit_key(salt_b64: str, artifacts) -> bytes:
    """
    Canonical key derivation for Satyajit.
    
    Parameters
    ----------
    salt_b64 : str
        Base64-encoded 16-byte random salt, as stored in the session DB.
    artifacts : dict | str
        Artifact dict (or JSON string thereof) containing alpha/beta/gamma/delta.

    Returns
    -------
    bytes
        32-byte AES-256 key.
    """
    salt_bytes = base64.b64decode(salt_b64)
    material = artifact_material(artifacts)

    # Diagnostic logging (no secrets)
    logger.info(
        "[CRYPTO] derive_satyajit_key | salt_len=%d | salt_sha256=%.8s | "
        "material_sha256=%.8s | material_repr=%r",
        len(salt_bytes),
        hashlib.sha256(salt_bytes).hexdigest(),
        hashlib.sha256(material).hexdigest(),
        material.decode("utf-8"),
    )

    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt_bytes,
        info=b"ctf_key_derivation",
    )
    key = hkdf.derive(material)

    logger.info(
        "[CRYPTO] derived key sha256=%.8s",
        hashlib.sha256(key).hexdigest(),
    )
    return key

# ------------------------------------------------------------------
# ENCRYPT / DECRYPT  (no AAD on either side)
# ------------------------------------------------------------------

def encrypt_credential(key: bytes, plaintext: str) -> dict:
    """
    AES-256-GCM encrypt. Returns base64-encoded nonce and ciphertext.
    No AAD is used (None on both sides).
    """
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    ct = aesgcm.encrypt(nonce, plaintext.encode("utf-8"), None)
    result = {
        "nonce": base64.b64encode(nonce).decode("utf-8"),
        "ciphertext": base64.b64encode(ct).decode("utf-8"),
    }
    logger.info(
        "[CRYPTO] encrypt_credential | nonce=%s | ct_len=%d | ct_sha256=%.8s",
        result["nonce"],
        len(ct),
        hashlib.sha256(ct).hexdigest(),
    )
    return result

def decrypt_credential(key: bytes, nonce_b64: str, ct_b64: str) -> str:
    """
    AES-256-GCM decrypt. Raises InvalidTag on any tampering.
    No AAD (None on both sides, matching encrypt_credential).
    """
    # Strip any accidental whitespace the player might have copied
    nonce_b64 = nonce_b64.strip()
    ct_b64 = ct_b64.strip()

    aesgcm = AESGCM(key)
    nonce = base64.b64decode(nonce_b64)
    ct = base64.b64decode(ct_b64)

    logger.info(
        "[CRYPTO] decrypt_credential | nonce=%s | ct_len=%d | ct_sha256=%.8s",
        nonce_b64,
        len(ct),
        hashlib.sha256(ct).hexdigest(),
    )

    plaintext = aesgcm.decrypt(nonce, ct, None).decode("utf-8")
    logger.info("[CRYPTO] decrypt SUCCESS | plaintext_len=%d", len(plaintext))
    return plaintext

# ------------------------------------------------------------------
# HIGH-LEVEL HELPERS called from routes.py
# ------------------------------------------------------------------

def generate_final_credential(session_id: str, salt_b64: str, artifacts) -> dict:
    """
    Generate AES-GCM encrypted credential after all four artifacts are collected.
    Called once at L4 completion. Returns {"nonce": ..., "ciphertext": ...}.
    """
    try:
        key = derive_satyajit_key(salt_b64, artifacts)
        plaintext = f"CREDENTIAL_FOR_{session_id}"
        return encrypt_credential(key, plaintext)
    except Exception as exc:
        logger.error("[CRYPTO] generate_final_credential FAILED | %s: %s", type(exc).__name__, exc)
        return {"error": "Credential generation failed"}

def redeem_credential(session_id: str, salt_b64: str, artifacts,
                      nonce_b64: str, ct_b64: str) -> bool:
    """
    Verify player-supplied nonce + ciphertext.
    Returns True if decryption succeeds and plaintext matches session_id.
    Raises on any crypto failure (caller should convert to HTTP 400).
    """
    key = derive_satyajit_key(salt_b64, artifacts)
    plaintext = decrypt_credential(key, nonce_b64, ct_b64)
    expected = f"CREDENTIAL_FOR_{session_id}"
    match = expected in plaintext
    logger.info(
        "[REDEEM] session=%s | expected_in_plaintext=%s",
        session_id, match,
    )
    return match

# ------------------------------------------------------------------
# LEGACY SHIMS  (keep old names so nothing else breaks)
# ------------------------------------------------------------------

def derive_key(salt: bytes, material: bytes) -> bytes:
    """Legacy shim. Use derive_satyajit_key() for new code."""
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        info=b"ctf_key_derivation",
    )
    return hkdf.derive(material)
