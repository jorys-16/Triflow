import unittest
import os
from core.utils import load_key, encrypt_data, decrypt_data

class TestUtils(unittest.TestCase):
    def test_encryption_and_decryption(self):
        key = load_key()
        data = {"test": 123, "hello": "world"}
        enc = encrypt_data(data, key)
        dec = decrypt_data(enc, key)
        self.assertEqual(data, dec)

    def test_key_persistence(self):
        key1 = load_key()
        key2 = load_key()
        self.assertEqual(key1, key2)

if __name__ == "__main__":
    unittest.main()