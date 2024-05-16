from egcd import egcd
from functools import reduce

def crt(A, M):
    sum = 0
    n = reduce(lambda a,b: a*b, M)
    for a, m in zip(A,M):
            Mi = n//m
            sum+= a * Mi * egcd(Mi, m)[1]
    return sum % n