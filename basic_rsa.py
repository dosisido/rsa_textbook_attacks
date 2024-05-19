from typing import Union
from Crypto.PublicKey import RSA
from Crypto.Util.number import long_to_bytes, bytes_to_long
from Crypto.Util.number import getPrime, inverse, GCD
from secret import message
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def encrypt(message: Union[int, bytes], key: RSA.RsaKey):
    if isinstance(message, int):
        return pow(message, key.e, key.n)
    elif isinstance(message, bytes):
        return pow(bytes_to_long(message), key.e, key.n)
    else:
        raise TypeError("Invalid message type. Expected bytes or int.")

def decrypt(cipher: int, key: RSA.RsaKey):
    return pow(cipher, key.d, key.n)

def print_key(key):
    print(f"n: {key.n}")
    print(f"e: {key.e}")
    print(f"d: {key.d}")
    print(f"p: {key.p}")
    print(f"q: {key.q}")

def run_until_pass(func):
    def wrapper(*args, **kwargs):
        while True:
            try:
                return func(*args, **kwargs)
            except ValueError:
                pass
    return wrapper

@run_until_pass
def gen_keys(bits, e = 65537):
    half_bits = bits // 2

    p = getPrime(half_bits)
    q = getPrime(half_bits)

    while p == q:
        q = getPrime(half_bits)

    n = p * q

    phi = (p - 1) * (q - 1)

    if GCD(e, phi) != 1:
        raise ValueError("e and phi are not coprime")

    d = inverse(e, phi)

    key = RSA.construct((n, e, d, p, q))

    return key

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