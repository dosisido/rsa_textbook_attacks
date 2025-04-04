from typing import Union
from math import gcd

class CommonPrimes:
    modulus = set()

    def __init__(self, modulus: set[int] = None):
        if modulus is not None:
            self.modulus = set(modulus)
        else:
            self.modulus = set()

    def try_factorize(self, N: int) -> Union[list[int], None]:
        self.modulus.add(N)

        for mod in self.modulus:
            if mod == N: continue

            g = gcd(N, mod)
            if g > 1 and g < N:
                return [g, N // g]

        return None

def main():
    from Crypto.Util.number import getPrime
    import random

    primes = [getPrime(10) for _ in range(100)]

    common_primes = CommonPrimes()
    for _ in range(1000):
        p = random.choice(primes)
        q = random.choice(primes)
        if p == q: continue

        n = p * q
        common_primes.try_factorize(n)

    p = random.choice(primes)
    q = random.choice(primes)
    n = p * q
    a = common_primes.try_factorize(n)
    print(p, q, a)
    assert a is not None and p in a and q in a
    print(a)

if __name__ == "__main__":
    main()