
def egcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = egcd(b % a, a)
        return g, x - (b // a) * y, y

def chinese_remainder(A: list, M:list):
    from functools import reduce
    
    sum = 0
    n = reduce(lambda a,b: a*b, M)
    for a, m in zip(A,M):
            Mi = n//m
            sum+= a * Mi * egcd(Mi, m)[1]
            mul_inv(Mi, m)
    return sum % n


def mul_inv(a, b):
    g, x, y = egcd(a, b)
    if g != 1:
        raise Exception('Modular inverse does not exist')
    else:
        return x % b

