from Crypto.PublicKey import RSA
from Crypto.Util.number import long_to_bytes, bytes_to_long
from secret import message
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def encrypt(message, key: RSA.RsaKey):
    return pow(bytes_to_long(message), key.e, key.n)

def decrypt(cipher, key: RSA.RsaKey):
    return pow(cipher, key.d, key.n)


def main():
    
    key = RSA.generate(2**11)

    # print(key.export_key())
    # print(key.publickey().export_key())
    # print(key.q)
    # print(key.p)
    # print(key.n)
    # print(key.e)


    cipher = encrypt(message, key)
    print(f"{long_to_bytes(cipher).hex()= }")

    plain = decrypt(cipher, key)
    print(f"{long_to_bytes(plain).decode()= }")


    pass

if __name__ == "__main__":
    main()