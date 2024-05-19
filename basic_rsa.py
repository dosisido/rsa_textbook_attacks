from Crypto.PublicKey import RSA
from Crypto.Util.number import long_to_bytes, bytes_to_long
from secret import message
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def encrypt(message: bytes, key: RSA.RsaKey):
    return pow(bytes_to_long(message), key.e, key.n)

def decrypt(cipher: int, key: RSA.RsaKey):
    return pow(cipher, key.d, key.n)

def print_key(key):
    print(f"n: {key.n}")
    print(f"e: {key.e}")
    print(f"d: {key.d}")
    print(f"p: {key.p}")
    print(f"q: {key.q}")

def main():
    
    key = RSA.generate(2**11)

    # print(key.export_key())
    # print(key.publickey().export_key())


    cipher = encrypt(message, key)
    print(f"{long_to_bytes(cipher).hex()= }")

    plain = decrypt(cipher, key)
    print(f"{long_to_bytes(plain).decode()= }")


    pass

if __name__ == "__main__":
    main()