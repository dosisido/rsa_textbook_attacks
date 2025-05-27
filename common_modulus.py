from Crypto.PublicKey import RSA
from Crypto.Util.number import long_to_bytes, bytes_to_long
from rsa_textbook_attacks.basic_rsa import encrypt, decrypt
from math import gcd


class CommonModulus():
    @staticmethod
    def attack(c1:int, c2:int, e1:int , e2:int , n:int):
        """ 
        finds the original message when it's encrypted with two different public keys with the same modulus  
        egcd finds u,v such that u\*e1 + v\*e2 = 1  
        then c1^u \* c2^v = m^e1\*u \* m^e2\*v = m^(e1\*u+e2\*v) = m  
        """
        from egcd import egcd
        r, u, v = egcd(e1, e2)
        assert r == 1, "e1 and e2 are not coprime"
        return pow(c1, u, n) * pow(c2, v, n) % n


def main():
    key1 = RSA.generate(2**11)
    assert gcd(17, key1.n) == 1
    key2 = RSA.construct((key1.n, 17))

    message = b'flag{dosisido}'
    enc1 = encrypt(message, key1)
    enc2 = encrypt(message, key2)

    attack = CommonModulus()
    dec = attack.attack(enc1, enc2, key1.e, key2.e, key1.n)
    print(f"{long_to_bytes(dec).decode()= }")

    pass

if __name__ == "__main__":
    main()