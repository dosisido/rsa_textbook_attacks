from Crypto.PublicKey import RSA
from rsa_textbook_attacks.basic_rsa import encrypt
from rsa_textbook_attacks.tools import chinese_remainder


__E = 3


class HastadBroadcast():
    def attack(self, ciphers: list[int], mods: list[int]) -> int:
        from primefac import introot
        assert len(ciphers) == len(mods)
        res = chinese_remainder(ciphers, mods)
        dec_int = introot(res, len(ciphers))
        if dec_int is None:
            raise ValueError("Failed to find integer root, check inputs.")
        return dec_int


def main():
    from Crypto.Util.number import long_to_bytes


    print("Generating ciphers...", end="\r")
    ciphers = []
    mods = []
    for _ in range(__E):
        key = RSA.generate(2**11, e=__E)
        c = encrypt(b"flag{dosisido}", key)
        ciphers.append(c)
        mods.append(key.n)
    print("Generated ciphers")

    attack = HastadBroadcast()
    res = attack.attack(ciphers, mods)
    res = long_to_bytes(res).decode()
    print("Decrypted message:", res)

    pass

if __name__ == "__main__":
    main()