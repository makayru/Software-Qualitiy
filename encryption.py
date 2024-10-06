from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
import base64
import hashlib

class RSAEncryption:
    # Hard-coded paths for the keys (Update these with your actual paths)
    PUBLIC_KEY_PATH = 'public_key.pem'
    PRIVATE_KEY_PATH = 'private_key.pem'

    @staticmethod
    def load_public_key():
        with open(RSAEncryption.PUBLIC_KEY_PATH, 'rb') as key_file:
            public_key = serialization.load_pem_public_key(
                key_file.read(),
                backend=default_backend()
            )
        return public_key
    
    @staticmethod
    def load_private_key():
        with open(RSAEncryption.PRIVATE_KEY_PATH, 'rb') as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None,
                backend=default_backend()
            )
        return private_key

    @staticmethod
    def hash_data(data):
        return hashlib.sha256(data.encode()).hexdigest()

    @staticmethod
    def encrypt_data(data: str) -> str:
        data = RSAEncryption.safe_encrypt(data)
        public_key = RSAEncryption.load_public_key()
        encrypted_data = public_key.encrypt(
            data.encode('utf-8'),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        # Encode the encrypted data in base64 for safe storage in databases
        return base64.b64encode(encrypted_data).decode('utf-8')

    def fix_base64_padding(data: str) -> str:
        """Ensure base64 string has correct padding."""
        return data + '=' * (-len(data) % 4)

    @staticmethod
    def decrypt_data(encrypted_data: str) -> str:
        private_key = RSAEncryption.load_private_key()
        # Fix base64 padding before decoding
        encrypted_data = RSAEncryption.fix_base64_padding(encrypted_data)
        encrypted_data_bytes = base64.b64decode(encrypted_data)
        decrypted_data = private_key.decrypt(
            encrypted_data_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return decrypted_data.decode('utf-8')

    def safe_encrypt(data):
        if data is None:
            data = 'None'  # Or any other default value
            return data
        
        return data