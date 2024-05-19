from Crypto.PublicKey import RSA
from Crypto.Util.number import bytes_to_long, long_to_bytes
from Crypto.Util.number import getPrime, inverse, GCD
from basic_rsa import print_key, encrypt, decrypt
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

STR_PAD = 20

def run_until_pass(func):
    def wrapper(*args, **kwargs):
        while True:
            try:
                return func(*args, **kwargs)
            except ValueError:
                pass
    return wrapper

@run_until_pass
def gen_keys(bits, e = 65537):
    half_bits = bits // 2

    p = getPrime(half_bits)
    q = getPrime(half_bits)

    while p == q:
        q = getPrime(half_bits)

    n = p * q

    phi = (p - 1) * (q - 1)

    if GCD(e, phi) != 1:
        raise ValueError("e and phi are not coprime")

    d = inverse(e, phi)

    key = RSA.construct((n, e, d, p, q))

    return key

def bytes_to_bits(b):
    if isinstance(b, bytes):
        b = int.from_bytes(b, byteorder='big')
    return ''.join(['1' if bit == '1' else '0' for bit in bin(b)[2:].zfill(8)])

def print_bounds(bounds):
    print("[" + str(bounds[0]) + "," + str(bounds[1]) + "]")

def main():
    MESSAGE = bytes.fromhex("00a0")
    # key = gen_keys(12, e=17)
    key = RSA.construct((2491, 17, 985, 47, 53))
    # print_key(key)

    def oracle(ciphertext):
        c = int.from_bytes(ciphertext,byteorder='big')
        dec = decrypt(c, key)

        binary_str = bytes_to_bits(dec)
        print(
            "Oracle received:".ljust(STR_PAD),
            str(binary_str[::-1] + f"\033[34m{binary_str[-1]}\033[0m").ljust(9 + 13),
            "|",
            str(dec).rjust(4)
        )

        # può restituire 1 perché il messaggio è moltiplicato modulo n
        # nel momento in cui 2m supera n il risultato è 2m % n = 2m - n
        # essendo n sempre dispari, 2m sarà sempre pari e 2m - n sarà sempre dispari

        lsb =  dec % 2
        return lsb
    
    # -------------------------------------------------------

    c = encrypt(MESSAGE, key)

    print(
        "Original message:".ljust(STR_PAD),
        str(bytes_to_bits(MESSAGE)).ljust(13),
        "|",
        str(bytes_to_long(MESSAGE)).rjust(4)
    )
    print(
        "Ciphertext:".ljust(STR_PAD),
        str(bytes_to_bits(long_to_bytes(c))).ljust(13),
        "|",
        str(c).rjust(4)
    )
    
    m = decrypt(c, key)
    m = long_to_bytes(m).hex()
    print(f"{m= }")


    bounds = (0, key.n)

    c = c
    for _ in range(key.n.bit_length()):
    # while bounds[1] - bounds[0] > 1:
        c = (pow(2, key.e, key.n) * c) % key.n

        bit = oracle(long_to_bytes(c))
        # print(f"Received bit: {bit}")

        if  bit == 0:
            bounds = (bounds[0], (bounds[1] + bounds[0]) // 2)
        else:
            bounds = ((bounds[1] + bounds[0]) // 2, bounds[1])
        # print_bounds(bounds)


    print("Bounds:", end=" ")
    print_bounds(bounds)
    print(f"Original message: {bytes_to_long(MESSAGE)}")
    for bound in range(bounds[0], bounds[1]+1):
        print(int.to_bytes(bound, length=2, byteorder='big').hex())
        

    pass

if __name__ == "__main__":
    main()