from Crypto.PublicKey import RSA
from Crypto.Util.number import long_to_bytes, bytes_to_long
from secret import message
from primefac import introot
from basic_rsa import encrypt, decrypt
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def main():
    key = RSA.generate(2**10, e=3)

    cipher = encrypt(message, key)

    decoded = introot(cipher, key.e)
    print(f"{decoded= }")
    print(f"{long_to_bytes(decoded).decode()= }")

    pass

if __name__ == "__main__":
    main()