from Crypto.PublicKey import RSA
from rsa_textbook_attacks.basic_rsa import encrypt, decrypt
from rsa_textbook_attacks.tools import chinese_remainder, egcd

SIZE = 2**11
E = 3


def hastad_broadcast_attack(ciphers: list[int], mods: list[int]) -> bytes:
    from primefac import introot
    assert len(ciphers) == len(mods)
    res = chinese_remainder(ciphers, mods)
    dec_int = introot(res, len(ciphers))
    return dec_int


def main():
    from secret import message
    from Crypto.Util.number import long_to_bytes, bytes_to_long

    class WhatIKnow():
        def __init__(self, ciphertext, modulus, e):
            self.ciphertext = ciphertext
            self.modulus = modulus
            self.e = e
        def __str__(self):
            return f"modulus: {self.modulus}, e: {self.e}, ciphertext: {self.ciphertext}"

    def generates_ciphers() -> list[WhatIKnow]:
        ciphers = []
        for _ in range(E):
            key = RSA.generate(SIZE, e=E)
            t = WhatIKnow(encrypt(message, key), key.n, key.e)
            ciphers.append(t)
        return ciphers
    

    print("Generating ciphers...", end="\r")
    informations = generates_ciphers()
    print("Generated ciphers" + " "*20)

    ciphers = [i.ciphertext for i in informations]
    mods = [i.modulus for i in informations]

    res = hastad_broadcast_attack(ciphers, mods)
    res = long_to_bytes(res).decode()
    print("Decrypted message:", res)

    pass

if __name__ == "__main__":
    main()