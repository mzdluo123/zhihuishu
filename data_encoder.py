from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import base64

PUBLIC_KEY = 'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCxLG06GQbNz7D1zUzBg8XuOyCymWJc/406S5owPEnu+yTU+rzR+sV5HGE8+KL4SxVyAQjdNdpXQ2e0Z938ee096v509Jc1mGxeI8KQ8Y79WEA0fI8fFjkXRYD+CqDtkes7GYbJ4m7TuajqJioVz5uMOpltalEKnMRCNOR1C90b0wIDAQAB'
MAX_ENCRYPT_BLOCK = 117


def encode(data: str) -> str:
    key_bytes = base64.b64decode(PUBLIC_KEY)
    pri_key = RSA.importKey(key_bytes)
    cipher = PKCS1_v1_5.new(pri_key)
    byte_data = bytes(data, "utf-8")
    encrypted = bytes()


    for i in range(0, len(byte_data), MAX_ENCRYPT_BLOCK):
        encrypted += cipher.encrypt(byte_data[i: i + MAX_ENCRYPT_BLOCK])

    return str(base64.b64encode(encrypted), encoding="utf-8")
