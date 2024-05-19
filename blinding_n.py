from Crypto.PublicKey import RSA
from basic_rsa import encrypt
from math import gcd
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))



def main():
    key = RSA.generate(2**10)

    # one way to blindly get N is to encrypt -1
    print("Encrypting -1")
    c = encrypt(-1, key)
    N = c+1
    print("Recovered modulus N, distance from actual N:", abs(key.n - N))


    print("-"*20)
    print("Encrypting 2 messages")
    c1 = encrypt(2, key)
    c2 = encrypt(3, key)
    N = gcd(2**key.e - c1, 3**key.e - c2)
    print("Recovered modulus N, distance from actual N:", abs(key.n - N))

    pass

if __name__ == "__main__":
    main()