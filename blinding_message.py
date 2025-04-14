from Crypto.PublicKey import RSA
from rsa_textbook_attacks.basic_rsa import encrypt, decrypt
from rsa_textbook_attacks.tools import modular_multiplication
from Crypto.Util.number import long_to_bytes


class blinding_message():
    BASE = 2
    def get_messages_to_encrypt(self, enc_flag: int, key: RSA.RsaKey) -> int:
        return modular_multiplication(pow(self.BASE, key.e, key.n), enc_flag, key.n)

    def blind_message(self, encrypted: int, n: int) -> int:
        inv = pow(self.BASE, -1, n)
        return encrypted * inv % n



def main():
    key = RSA.generate(1024)

    enc_flag = encrypt(b"flag{dosisido}", key)

    # let's suppose i can decript anyting besides the flag
    attack = blinding_message()
    c = attack.get_messages_to_encrypt(enc_flag, key)
    two_m = decrypt(c, key)
    m = attack.blind_message(two_m, key.n)


    print("Decrypted message:", long_to_bytes(m).decode())



if __name__ == "__main__":
    main()