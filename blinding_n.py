
VALUES_TO_ENCRYPT = [2, 3]

def get_messages_to_encrypt() -> list[int]:
    return VALUES_TO_ENCRYPT

def blind_n(encryped: list, e: int) -> int:
    from math import gcd
    assert len(encryped) == 2
    c1, c2 = encryped
    a, b = VALUES_TO_ENCRYPT
    return gcd(a**e - c1, b**e - c2)


if __name__ == "__main__":
    from .basic_rsa import encrypt, gen_keys
    key = gen_keys(2**10)
    print(f"original n: {key.n}")

    # one way to blindly get N is to encrypt -1
    print("Encrypting -1")
    c = encrypt(-1, key)
    N = c+1
    print("Recovered modulus N, distance from actual N:", abs(key.n - N))


    print("-"*20)
    print("Encrypting 2 messages")
    enc = [encrypt(m, key) for m in get_messages_to_encrypt()]
    N = blind_n(enc, key.e)
    print("Recovered modulus N, distance from actual N:", abs(key.n - N))

    if abs(key.n - N) != 0:
        print(f"found N: {N}")
