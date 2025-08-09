import os
import json
from cryptography.fernet import Fernet

KEY_FILE = 'key.key'

def load_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, 'wb') as f:
            f.write(key)
    else:
        with open(KEY_FILE, 'rb') as f:
            key = f.read()
    return key

def encrypt_data(data, key):
    f = Fernet(key)
    return f.encrypt(json.dumps(data).encode())

def decrypt_data(enc_data, key):
    f = Fernet(key)
    return json.loads(f.decrypt(enc_data).decode())