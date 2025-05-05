from Crypto.PublicKey import RSA
from Crypto.Util.number import long_to_bytes
from rsa_textbook_attacks.basic_rsa import encrypt


class LowPublicExponent():
    def attack(self, cipher: int, e: int) -> int:
        from primefac import introot
        return introot(cipher, e)


def main():
    key = RSA.generate(2**10, e=3)
    attack = LowPublicExponent()

    cipher = encrypt(b"flag{dosisido}", key)

    decoded = attack.attack(cipher, key.e)
    print(f"{decoded= }")
    print(f"{long_to_bytes(decoded).decode()= }")

    pass

if __name__ == "__main__":
    main()