from Crypto.PublicKey import RSA
from Crypto.Util.number import long_to_bytes, bytes_to_long
from secret import message
from basic_rsa import encrypt, decrypt
from tools import crt, egcd
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

SIZE = 2**12
E = 3

class WhatIKnow():
    def __init__(self, ciphertext, modulus, e):
        self.ciphertext = ciphertext
        self.modulus = modulus
        self.e = e
    def __str__(self):
        return f"modulus: {self.modulus}, e: {self.e}, ciphertext: {self.ciphertext}"

def generates_ciphers():
    ciphers = []
    for _ in range(E):
        key = RSA.generate(SIZE, e=E)
        t = WhatIKnow(encrypt(message, key), key.n, key.e)
        ciphers.append(t)
    return ciphers

def hastad_broadcast_attack(ciphers, mods):
    from primefac import introot
    assert len(ciphers) == len(mods)
    res = crt(ciphers, mods)
    dec_int = introot(res, len(ciphers))
    return long_to_bytes(dec_int)


def main():

    print("Generating ciphers...", end="\r")
    informations = generates_ciphers()
    print("Generated ciphers" + " "*20)

    ciphers = [i.ciphertext for i in informations]
    mods = [i.modulus for i in informations]

    res = hastad_broadcast_attack(ciphers, mods).decode()
    print("Decrypted message:", res)

    pass

if __name__ == "__main__":
    main()