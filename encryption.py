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

    def generate_keys(self):
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        self.public_key = self.private_key.public_key()

        # Save the private key to a file
        with open("private_key.pem", "wb") as f:
            f.write(
                self.private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                    encryption_algorithm=serialization.NoEncryption()
                )
            )

        # Save the public key to a file
        with open("public_key.pem", "wb") as f:
            f.write(
                self.public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                )
            )

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

    def encrypt_data(self, data):
        # Hash the data first to ensure consistent encryption output
        hashed_data = self.hash_data(data)
        encrypted = self.public_key.encrypt(
            hashed_data.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return encrypted

    def decrypt_data(self, encrypted_data):
        decrypted = self.private_key.decrypt(
            encrypted_data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return decrypted.decode()
