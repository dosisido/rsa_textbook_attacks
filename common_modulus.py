from Crypto.PublicKey import RSA
from Crypto.Util.number import long_to_bytes, bytes_to_long
from .basic_rsa import encrypt, decrypt
from math import gcd


def common_modulus_attack(cipher1:int, cipher2:int, e1:int , e2:int , n:int ):
    from egcd import egcd
    """ 
        finds the original message when it's encrypted with two different public keys with the same modulus

        egcd finds u,v such that u*e1 + v*e2 = 1

        then c1^u * c2^v = m^e1*u * m^e2*v = m^(e1*u+e2*v) = m
    """
    _, u, v = egcd(e1, e2)
    return pow(cipher1, u, n) * pow(cipher2, v, n) % n


def main():
    from secret import message
    key1 = RSA.generate(2**11)
    assert gcd(17, key1.n) == 1
    key2 = RSA.construct((key1.n, 17))

    enc1 = encrypt(message, key1)
    enc2 = encrypt(message, key2)

    dec = common_modulus_attack(enc1, enc2, key1.e, key2.e, key1.n)
    print(f"{long_to_bytes(dec).decode()= }")

    pass

if __name__ == "__main__":
    main()