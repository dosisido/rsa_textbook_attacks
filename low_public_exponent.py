from Crypto.PublicKey import RSA
from Crypto.Util.number import long_to_bytes, bytes_to_long
from .basic_rsa import encrypt, decrypt
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def low_public_exponent_attack(cipher: int, e: int):
    from primefac import introot
    return introot(cipher, e)


def main():
    from secret import message
    key = RSA.generate(2**10, e=3)

    cipher = encrypt(message, key)

    decoded = low_public_exponent_attack(cipher, key.e)
    print(f"{decoded= }")
    print(f"{long_to_bytes(decoded).decode()= }")

    pass

if __name__ == "__main__":
    main()