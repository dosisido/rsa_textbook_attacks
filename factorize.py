import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from Crypto.Util.number import getPrime, getRandomInteger
from factordb.factordb import FactorDB
from gmpy2 import next_prime, isqrt


n_length = 30



def factor_db(n):
    f = FactorDB(n)
    f.connect()
    factor_list = f.get_factor_list()
    if len(factor_list) == 1:
        print("No factors found, or the number is prime.")
        return None
    factor_list.sort()
    return tuple(factor_list)


def fermat(n):
    a = isqrt(n)
    b = a
    b2 = pow(a,2) - n

    # print("a= "+str(a))
    # print("b= " + str(b))

    # print("b2=" + str(b2))
    # print("delta-->" + str(pow(b, 2) - b2 % n)+"\n-----------")
    # print("iterate")

    i = 0
    while True:
        if b2 == pow(b,2):
            # print("found at iteration "+str(i))
            break
        else:
            a+= 1
            b2= pow(a, 2) - n
            b = isqrt(b2)
        i+=1
    #     print("iteration="+str(i))
    #     print("a= " + str(a))
    #     print("b= " + str(b))
    # print("b2 =" + str(b2))
    # print("delta-->" + str(pow(b, 2) - b2 % n) + "\n-----------")

    p = a+b
    q = a-b

    factor_list = [int(p), int(q)]
    factor_list.sort()
    return tuple(factor_list)


def main():
    p1 = getPrime(n_length)
    p2 = getPrime(n_length)
    n = p1 * p2


    print("FactorDb: ")
    print(factor_db(n))

    print('-'*10)

    print("Fermat: ")
    print(fermat(n))
    
    pass

if __name__ == "__main__":
    main()