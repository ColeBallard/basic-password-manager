import base64

from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2

class PCrypt:
    def __init__(self, key) -> None:
        self.key = key

    def derive_key(self, pin):
        # Derive a 256-bit key using the provided pin
        salt = b'\x00'*16  # Static salt; in a real-world scenario, use a random salt
        self.key = PBKDF2(pin, salt, dkLen=32, count=1000000)

    def encrypt_data(self, data):
        if self.key == None:
            return data

        # Prepare data for encryption (AES requires 16-byte blocks)
        data = data.encode('utf-8')
        pad = 16 - len(data) % 16
        data += bytes([pad] * pad)

        # Encrypt data
        cipher = AES.new(self.key, AES.MODE_CBC)
        ct_bytes = cipher.encrypt(data)
        iv = cipher.iv

        # Encode the encrypted data and IV to base64
        iv = base64.b64encode(iv).decode('utf-8')
        ct = base64.b64encode(ct_bytes).decode('utf-8')
        return iv, ct

    def decrypt_data(self, iv, ct):
        # Decode the base64 encoded iv and encrypted data
        iv = base64.b64decode(iv)
        ct = base64.b64decode(ct)

        # Decrypt the data
        cipher = AES.new(self.key, AES.MODE_CBC, iv=iv)
        pt = cipher.decrypt(ct)

        # Remove padding
        pad = pt[-1]
        pt = pt[:-pad]

        return pt.decode('utf-8')