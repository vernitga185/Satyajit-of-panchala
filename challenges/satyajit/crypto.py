import os
import json
import base64
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def derive_key(salt: bytes, material: bytes) -> bytes:
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        info=b"ctf_key_derivation"
    )
    return hkdf.derive(material)

def encrypt_credential(key: bytes, plaintext: str) -> dict:
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    ct = aesgcm.encrypt(nonce, plaintext.encode(), None)
    return {
        "nonce": base64.b64encode(nonce).decode('utf-8'),
        "ciphertext": base64.b64encode(ct).decode('utf-8')
    }

def decrypt_credential(key: bytes, nonce_b64: str, ct_b64: str) -> str:
    aesgcm = AESGCM(key)
    nonce = base64.b64decode(nonce_b64)
    ct = base64.b64decode(ct_b64)
    return aesgcm.decrypt(nonce, ct, None).decode('utf-8')

def generate_final_credential(session_id: str, salt_b64: str, artifacts: dict) -> dict:
    # Requires artifacts alpha, beta, gamma, delta in specific order
    try:
        a = artifacts.get("alpha", "")
        b = artifacts.get("beta", "")
        g = artifacts.get("gamma", "")
        d = artifacts.get("delta", "")
        
        material = f"{a}:{b}:{g}:{d}".encode()
        salt = base64.b64decode(salt_b64)
        key = derive_key(salt, material)
        
        cred = f"CREDENTIAL_FOR_{session_id}"
        return encrypt_credential(key, cred)
    except Exception as e:
        return {"error": "Invalid artifacts"}
