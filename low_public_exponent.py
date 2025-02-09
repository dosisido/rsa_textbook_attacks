from Crypto.PublicKey import RSA
from Crypto.Util.number import long_to_bytes, bytes_to_long
from secret import message
from basic_rsa import encrypt, decrypt
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def low_public_exponent_attack(cipher, key):
    from primefac import introot
    return introot(cipher, key.e)


def main():
    key = RSA.generate(2**10, e=3)

    cipher = encrypt(message, key)

    decoded = low_public_exponent_attack(cipher, key)
    print(f"{decoded= }")
    print(f"{long_to_bytes(decoded).decode()= }")

    pass

if __name__ == "__main__":
    main()