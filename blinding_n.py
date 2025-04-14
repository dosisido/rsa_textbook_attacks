
class blinding_n():
    VALUES_TO_ENCRYPT = [2, 3]

    def get_messages_to_encrypt(self) -> list[int]:
        return self.VALUES_TO_ENCRYPT

    def blind_n(self, encryped: list, e: int) -> int:
        from math import gcd
        assert len(encryped) == 2
        c1, c2 = encryped
        a, b = self.VALUES_TO_ENCRYPT
        return gcd(a**e - c1, b**e - c2)
    
    @staticmethod
    def minus_one_encrypted(c: int):
        return c+1


if __name__ == "__main__":
    from rsa_textbook_attacks.basic_rsa import encrypt, gen_keys
    key = gen_keys(2**10)
    # print(f"original n: {key.n}")
    attack = blinding_n()

    # one way to blindly get N is to encrypt -1
    print("Encrypting -1")
    N = attack.minus_one_encrypted(encrypt(-1, key))
    print("Recovered modulus N, distance from actual N:", abs(key.n - N))


    print("-"*20)
    print("Encrypting 2 messages")
    attack.VALUES_TO_ENCRYPT = [5, 9]
    enc = [encrypt(m, key) for m in attack.get_messages_to_encrypt()]
    N = attack.blind_n(enc, key.e)
    print("Recovered modulus N, distance from actual N:", abs(key.n - N))

    if abs(key.n - N) != 0:
        print(f"found N: {N}")
