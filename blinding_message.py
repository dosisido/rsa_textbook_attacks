from rsa_textbook_attacks.basic_rsa import encrypt, decrypt
from rsa_textbook_attacks.tools import modular_multiplication
from Crypto.Util.number import long_to_bytes


class BlindingMessage():
    BASE = 2

    def rand_base(self):
        import random
        from rsa_textbook_attacks.tools import small_primes
        self.BASE = random.choice(small_primes)

    def invert_base(self, n: int):
        self.BASE = pow(self.BASE, -1, n)

    def get_messages_to_encrypt(self, enc_flag: int, e: int, N:int) -> int:
        """ 
        c = m^e mod N  
        c' = (k^e) \* c mod N = (k \* m)^e mod N  
        km = c'^d mod N  
        """
        return modular_multiplication(pow(self.BASE, e, N), enc_flag, N)

    def blind_message(self, encrypted: int, n: int) -> int:
        inv = pow(self.BASE, -1, n)
        return encrypted * inv % n



def main():
    from Crypto.PublicKey import RSA
    key = RSA.generate(1024)

    enc_flag = encrypt(b"flag{dosisido}", key)

    # let's suppose i can decript anyting besides the flag
    attack = BlindingMessage()
    c = attack.get_messages_to_encrypt(enc_flag, key.e, key.n)
    two_m = decrypt(c, key)
    m = attack.blind_message(two_m, key.n)


    print("Decrypted message:", long_to_bytes(m).decode())



if __name__ == "__main__":
    main()