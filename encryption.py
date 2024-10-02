from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import hashlib

class RSAEncryption:
    def __init__(self):
        self.private_key = None
        self.public_key = None
        self.load_keys()

    def load_keys(self):
        try:
            with open("private_key.pem", "rb") as f:
                self.private_key = serialization.load_pem_private_key(
                    f.read(),
                    password=None
                )

            with open("public_key.pem", "rb") as f:
                self.public_key = serialization.load_pem_public_key(f.read())
        except FileNotFoundError:
            self.generate_keys()

    def hash_data(self, data):
        return hashlib.sha256(data.encode()).hexdigest()

    def encrypt_data(self, data: str) -> bytes:
        # Encrypt the data using the public key
        encrypted = self.public_key.encrypt(
            data.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return encrypted

    def decrypt_data(self, encrypted_data: bytes) -> str:
        # Decrypt the data using the private key
        decrypted = self.private_key.decrypt(
            encrypted_data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return decrypted.decode('utf-8')