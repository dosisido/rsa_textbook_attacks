
class BlindingN():
    values_to_encrypt = [2, 3]
    values_to_encrypt_no_e = [2, 3, 5]
    

    def random_values(self):
        import random
        from rsa_textbook_attacks.tools import small_primes
        self.values_to_encrypt = random.sample(small_primes, 2)

    def get_messages_to_encrypt(self) -> list[int]:
        return self.values_to_encrypt
    
    def get_messages_to_encrypt_no_e(self) -> list[int]:
        return self.values_to_encrypt_no_e + [x**2 for x in self.values_to_encrypt_no_e]

    def blind_n(self, encryped: list, e: int = 65537) -> int:
        """
        c1 = m1^e mod N  
        c2 = m2^e mod N  

        m1^e - c1 = 0 mod N = k1 * N  
        m2^e - c2 = 0 mod N = k2 * N  

        gcd(m1^e - c1, m2^e - c2) = gcd(k1 * N, k2 * N) = N
        """
        from math import gcd
        assert len(encryped) == 2
        c1, c2 = encryped
        a, b = self.values_to_encrypt
        return gcd(a**e - c1, b**e - c2)

    def blind_n_no_e(self, encryped: list) -> int:
        from math import gcd
        assert len(encryped) == (len(self.values_to_encrypt_no_e) * 2)
        c1, c2, c3, c4, c5, c6 = encryped
        N = gcd(gcd(c1**2 - c4, c2**2 - c5), c3**2 - c6)
        return N

    @staticmethod
    def minus_one_encrypted(c: int):
        return c+1


if __name__ == "__main__":
    from rsa_textbook_attacks.basic_rsa import encrypt, gen_keys
    key = gen_keys(2**10)
    # print(f"original n: {key.n}")
    attack = BlindingN()

    # one way to blindly get N is to encrypt -1
    print("Encrypting -1")
    N = attack.minus_one_encrypted(encrypt(-1, key))
    print("Recovered modulus N, distance from actual N:", abs(key.n - N))


    print("-"*20)
    print("Encrypting 2 messages")
    attack.random_values()
    enc = [encrypt(m, key) for m in attack.get_messages_to_encrypt()]
    N = attack.blind_n(enc, key.e)
    print("Recovered modulus N, distance from actual N:", abs(key.n - N))

    if abs(key.n - N) != 0:
        print(f"found N: {N}")
