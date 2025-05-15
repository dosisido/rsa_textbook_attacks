from typing import Union
from math import gcd

class CommonPrimes:
    modulus = set()

    def __init__(self, modulus: set[int] = None):
        if modulus is not None:
            self.modulus = set(modulus)
        else:
            self.modulus = set()
    
    def add_modulus(self, vals: Union[int, list[int]]):
        if isinstance(vals, list):
            for n in vals: self.modulus.add(n)
        else:
            self.modulus.add(vals)

    def try_factorize(self, N: int) -> Union[list[int], None]:
        self.modulus.add(N)
        for mod in self.modulus:
            if mod == N: continue
            g = gcd(N, mod)
            if g > 1 and g < N:
                return [g, N // g]
        return None
    
    def export_primes(self) -> set[int]:
        primes = set()
        modulus = list(self.modulus)
        i = 0
        while i < len(modulus):
            n = modulus[i]
            found = False
            for j in range(len(modulus)):
                if i == j: continue
                m = modulus[j]
                g = gcd(n, m)
                if 1 < g < n and 1 < g < m:
                    primes.add(g)
                    n //= g
                    m //= g
                    primes.add(n)
                    primes.add(m)
                    modulus[i] = n
                    modulus[j] = m
                    found = True
                    break
            if n == 1:
                modulus.pop(i)
            else:
                if not found:
                    i += 1
        # Remove 1s and 0s, and any composites left
        primes |= {x for x in modulus if x > 1}
        return primes
    
            

def main():
    from Crypto.Util.number import getPrime
    import random

    primes = [getPrime(100) for _ in range(1000)]

    common_primes = CommonPrimes()
    for _ in range(len(primes)):
        p = random.choice(primes)
        q = random.choice(primes)
        if p == q: continue

        n = p * q
        common_primes.add_modulus(n)

    p = random.choice(primes)
    q = random.choice(primes)
    n = p * q
    fac = common_primes.try_factorize(n)
    print(p, q, fac)
    assert fac is not None and p in fac and q in fac

    print(common_primes.export_primes())
    primes = set(primes)
    assert all(x in primes for x in common_primes.export_primes())

if __name__ == "__main__":
    main()