from Crypto.PublicKey import RSA
from basic_rsa import gen_keys, print_key
import sys
# sys.path.append('./rsa_wiener-attack')
# from RSAwienerHacker import hack_RSA as wiener_hack
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))


from Crypto.Util.number import inverse, long_to_bytes
import math

# Function to compute the continued fraction representation of e/N
def continued_fraction(e, N):
    cf = []
    while N:
        a = e // N
        cf.append(a)
        e, N = N, e - a * N
    return cf

# Function to compute the convergents of the continued fraction
def convergents(cf):
    convergents = []
    for i in range(len(cf)):
        num = 0
        den = 1
        for j in range(i, -1, -1):
            num, den = den, cf[j] * den + num
        convergents.append((num, den))
    return convergents

# Function to perform the Wiener attack
def wiener_attack(e, N):
    cf = continued_fraction(e, N)
    conv = convergents(cf)
    print(conv)
    for k, d in conv:
        if k == 0:
            continue
        # Check if the obtained k and d satisfy the equation
        phi_n = (e * d - 1) // k
        if (e * d - 1) % k != 0:
            continue
        # Solve the quadratic equation x^2 - (N - phi_n + 1)x + N = 0
        s = N - phi_n + 1
        discriminant = s * s - 4 * N
        if discriminant >= 0:
            t = int(math.isqrt(discriminant))
            if t * t == discriminant:
                # Roots are (s + t) / 2 and (s - t) / 2
                p = (s + t) // 2
                q = (s - t) // 2
                if p * q == N:
                    return d
    return None



def main():
    
    key = gen_keys(12, d=17)
    print_key(key)

    found_d = wiener_attack(key.e, key.n)
    print("Found d:", found_d)


if __name__ == "__main__":
    main()