import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from Crypto.Util.number import getPrime



def factor_db(n):
    from factordb.factordb import FactorDB
    f = FactorDB(n)
    f.connect()
    factor_list = f.get_factor_list()
    if len(factor_list) == 1:
        print("No factors found, or the number is prime.")
        return None
    factor_list.sort()
    return tuple(factor_list)

def fermat(n):
    from gmpy2 import isqrt
    a = isqrt(n)
    b = a
    b2 = pow(a,2) - n

    i = 0
    while True:
        if b2 == pow(b,2):
            break
        else:
            a+= 1
            b2= pow(a, 2) - n
            b = isqrt(b2)
        i+=1

    p = a+b
    q = a-b

    factor_list = [int(p), int(q)]
    factor_list.sort()
    return tuple(factor_list)

def primefac_lib(n):
    from primefac import primefac, multifactor
    primes = []
    while n != 1:
        primes.append(multifactor(n)[0])
        n = n // primes[-1]
    primes.sort()
    return tuple(primes)

def main():
    n_length = 30
    p1 = getPrime(n_length)
    p2 = getPrime(n_length)
    n = p1 * p2

    originals_prime = [p1, p2]
    originals_prime.sort()
    print("Original primes: ")
    print(tuple(originals_prime))


    # print('-'*10)
    # print("FactorDb: ")
    # print(factor_db(n))

    # print('-'*10)
    # print("Fermat: ")
    # print(fermat(n))
    
    print('-'*10)
    print("Primefac: ")
    print(primefac_lib(n))

    pass

if __name__ == "__main__":
    main()