"""
Utility functions for encryption and decryption of task and budget data.

This module mirrors the behaviour of the original ``core/utils.py`` from
the Tkinter implementation.  It uses Fernet symmetric encryption to
protect the JSON payloads saved to disk.  A unique encryption key is
generated once and stored in ``key.key``.  Subsequent calls to
``load_key`` will reuse the same key so that previously saved data can
be decrypted.
"""

import json
import os
from cryptography.fernet import Fernet

# Name of the file storing the encryption key
KEY_FILE = "key.key"


def load_key() -> bytes:
    """Load an existing encryption key or generate a new one.

    If the key file does not exist, a new key is generated and
    persisted.  The key is returned as bytes.
    """
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
        return key
    else:
        with open(KEY_FILE, "rb") as f:
            return f.read()


def encrypt_data(data: list[dict], key: bytes) -> bytes:
    """Encrypt a Python list of dictionaries using Fernet.

    The list is first JSON‑serialised before encryption.  The caller
    must provide the key.
    """
    f = Fernet(key)
    payload = json.dumps(data).encode("utf-8")
    return f.encrypt(payload)


def decrypt_data(enc_data: bytes, key: bytes) -> list[dict]:
    """Decrypt an encrypted payload back into a list of dictionaries.

    If decryption fails or the payload does not decode to valid JSON,
    an exception will be raised.
    """
    f = Fernet(key)
    payload = f.decrypt(enc_data)
    return json.loads(payload.decode("utf-8"))