import base64, os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def encrypt(file_path: str) -> str:
    
    key = AESGCM.generate_key(bit_length=128)
    aesgcm = AESGCM(key)

    data = file_path.encode('utf-8')
    nonce = os.urandom(12)
    
    ## 生成隨機解密金鑰
    print(f"Nonce: {nonce.hex()}")

    ciphertext = aesgcm.encrypt(nonce, data, None)
    combined = nonce + ciphertext
    
    ## 印出加密後路徑
    print(f"Base64: {base64.urlsafe_b64encode(combined).decode('utf-8')}")

    return base64.urlsafe_b64encode(combined).decode('utf-8')

def decrypt(encoded: str, key: str) -> str:

    aesgcm = AESGCM(bytes.fromhex(key))
    combined = base64.urlsafe_b64decode(encoded)
    nonce, ciphertext = combined[:12], combined[12:]

    return aesgcm.decrypt(nonce, ciphertext, None).decode('utf-8')


# encrypt("D:\\path_example.json")