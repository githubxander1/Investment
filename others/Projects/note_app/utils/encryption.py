# utils/encryption.py
from cryptography.fernet import Fernet

def generate_key():
    """生成一个新的加密密钥"""
    return Fernet.generate_key()

def encrypt_data(data, key):
    """加密数据"""
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data.encode())
    return encrypted_data

def decrypt_data(encrypted_data, key):
    """解密数据"""
    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(encrypted_data).decode()
    return decrypted_data

# 示例
key = generate_key()
data = "This is a secret message"
encrypted_data = encrypt_data(data, key)
decrypted_data = decrypt_data(encrypted_data, key)
print(f"Original: {data}")
print(f"Encrypted: {encrypted_data}")
print(f"Decrypted: {decrypted_data}")