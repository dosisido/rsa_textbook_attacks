from typing import Union
from Crypto.PublicKey import RSA
from Crypto.Util.number import long_to_bytes, bytes_to_long
from Crypto.Util.number import getPrime, inverse
from math import gcd
some_primes = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]


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
        index = 0
        while True:
            try:
                return func(*args, **kwargs)
            except ValueError as e:
                if index >= len(some_primes):
                    raise e
                e = some_primes[index]
                if "e" in kwargs:
                    raise ValueError("Impossible to find a key with the given parameters")
                kwargs["e"] = e
                index += 1
                pass
    return wrapper

@run_until_pass
def gen_keys(key: Union[int, list[int]], e = 65537, d = None) -> RSA.RsaKey:
    if isinstance(key, int):
        half_bits = key // 2

        p = getPrime(half_bits)
        q = getPrime(half_bits)

        while p == q:
            q = getPrime(half_bits)
    
    if isinstance(key, list) and len(key) == 2:
        p, q = key
        assert p != q
        

    n = p * q
    phi = (p - 1) * (q - 1)

    if d is None:
        if gcd(e, phi) != 1:
            raise ValueError("e and phi are not coprime")

        d = inverse(e, phi)
    else:
        e = inverse(d, phi)
        if gcd(e, phi) != 1:
            raise ValueError("e and phi are not coprime")

    key = RSA.construct((n, e, d, p, q))

    return key

def main():
    from secret import message
    
    # key = RSA.generate(2**11)

    # cipher = encrypt(message, key)
    # print(f"{long_to_bytes(cipher).hex()= }")

    # plain = decrypt(cipher, key)
    # print(f"{long_to_bytes(plain).decode()= }")

    key = gen_keys([3, 11])
    print_key(key)


if __name__ == "__main__":
    main()