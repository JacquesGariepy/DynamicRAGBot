import re
from cryptography.fernet import Fernet

class DataProtection:
    def __init__(self, encryption_key):
        self.cipher_suite = Fernet(encryption_key)

    def detect_sensitive_data(self, text):
        patterns = {
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'credit_card': r'\b(?:\d{4}[-\s]?){3}\d{4}\b',
            'phone_number': r'\b\+?[\d\s-]{10,}\b'
        }

        sensitive_data = {}
        for data_type, pattern in patterns.items():
            matches = re.findall(pattern, text)
            if matches:
                sensitive_data[data_type] = matches

        return sensitive_data

    def encrypt_sensitive_data(self, text):
        sensitive_data = self.detect_sensitive_data(text)
        for data_type, items in sensitive_data.items():
            for item in items:
                encrypted = self.cipher_suite.encrypt(item.encode()).decode()
                text = text.replace(item, f"[ENCRYPTED_{data_type.upper()}:{encrypted}]")
        return text

    def decrypt_sensitive_data(self, text):
        pattern = r'\[ENCRYPTED_(\w+):([^\]]+)\]'
        matches = re.findall(pattern, text)
        for data_type, encrypted in matches:
            decrypted = self.cipher_suite.decrypt(encrypted.encode()).decode()
            text = text.replace(f"[ENCRYPTED_{data_type}:{encrypted}]", decrypted)
        return text