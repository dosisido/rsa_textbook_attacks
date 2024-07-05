from Crypto.PublicKey import RSA
from Crypto.Util.number import bytes_to_long, long_to_bytes
from basic_rsa import print_key, encrypt, decrypt, gen_keys
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from usefull.plotter import number_line
os.chdir(os.path.dirname(os.path.abspath(__file__)))

PRINT = False
STR_PAD = 20
BITS_LEAKED = 3

def bytes_to_bits(b):
    if isinstance(b, bytes):
        b = int.from_bytes(b, byteorder='big')
    return ''.join(['1' if bit == '1' else '0' for bit in bin(b)[2:].zfill(8)])

def int_to_bits(i):
    return ''.join(['1' if bit == '1' else '0' for bit in bin(i)[2:].zfill(BITS_LEAKED)])

def print_bounds(bounds):
    print("[" + str(bounds[0]) + "," + str(bounds[1]) + "]")

def main():
    MESSAGE = bytes.fromhex("48656c6c6f2c20776f726c642120646f73697369646f20726f6b73")
    # key = gen_keys(12, e=17)
    key = gen_keys(256)
    # print_key(key)

    def oracle(ciphertext):
        c = int.from_bytes(ciphertext,byteorder='big')
        dec = decrypt(c, key)

        binary_str = bytes_to_bits(dec)
        if PRINT: print(
            "Oracle received:".ljust(STR_PAD),
            str(binary_str[::-1] + f"\033[34m{binary_str[-1]}\033[0m").ljust(9 + 13),
            "|",
            str(dec).rjust(4)
        )

        # può restituire 1 perché il messaggio è moltiplicato modulo n
        # nel momento in cui 2m supera n il risultato è 2m % n = 2m - n
        # essendo n sempre dispari, 2m sarà sempre pari e 2m - n sarà sempre dispari

        lsb =  dec % (2 ** BITS_LEAKED)
        return lsb
    
    # -------------------------------------------------------

    c = encrypt(MESSAGE, key)

    if PRINT: print(
        "Original message:".ljust(STR_PAD),
        str(bytes_to_bits(MESSAGE)).ljust(13),
        "|",
        str(bytes_to_long(MESSAGE)).rjust(4)
    )
    if PRINT: print(
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
    for _ in range(key.n.bit_length() // BITS_LEAKED):
    # while bounds[1] - bounds[0] > 1:
        c = (pow(2**BITS_LEAKED, key.e, key.n) * c) % key.n

        bits = oracle(long_to_bytes(c))
        bits = int_to_bits(bits)
        print(f"Received bits: {bits}")

        for bit in bits[::]:
            bit = int(bit)
            if  bit == 0:
                bounds = (bounds[0], (bounds[1] + bounds[0]) // 2)
            elif bit == 1:
                bounds = ((bounds[1] + bounds[0]) // 2, bounds[1])
            else:
                print(bits, bit, type(bits), type(bit), len(bits), len(bit))
                raise ValueError("Invalid bit")
        # print_bounds(bounds)
        # number_line(key.n, bounds[0], bounds[1])


    print("Bounds:", end=" ")
    print_bounds(bounds)
    print(f"Original message: {bytes_to_long(MESSAGE)}")
    for bound in range(bounds[0], bounds[1]+1):
        # print(int.to_bytes(bound, length=len(MESSAGE), byteorder='big').hex())
        print(' ' * 18 + str(bound))
        

    pass

if __name__ == "__main__":
    main()