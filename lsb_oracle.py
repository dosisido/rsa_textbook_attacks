from rsa_textbook_attacks.basic_rsa import print_key, encrypt, decrypt, gen_keys
from Crypto.PublicKey import RSA
from collections.abc import Callable
from Crypto.Util.number import bytes_to_long, long_to_bytes
from typing import Union
import decimal


__BITS_LEAKED = 1
__PRINT = False
__STR_PAD = 20
if __name__ == "__main__":
    __oracle_key = gen_keys(1024)



def number_line(n: int, a: int, b: int) -> None:
    import shutil
    import sys
    # Get the width of the terminal window
    width, _ = shutil.get_terminal_size()
    
    bar_width = width

    # Scale the positions to fit the bar width
    scale = bar_width / n
    scaled_a = int(a * scale)
    scaled_b = int(b * scale)

    # Create the progress bar
    progress = [" "] * bar_width
    for i in range(scaled_a, scaled_b):
        # progress[i] = '\033[94m' + '=' + '\033[0m'
        progress[i] = '='

    # progress_line = "|" + "".join(progress) + "|"
    progress_line = "".join(progress)
    print(f"{progress_line}", end="\r")
    # sys.stdout.write(f"{progress_line}\r")
    # sys.stdout.flush()

def _bytes_to_bits(b: bytes) -> str:
    if isinstance(b, bytes):
        b = int.from_bytes(b, byteorder='big')
    return ''.join(['1' if bit == '1' else '0' for bit in bin(b)[2:].zfill(2**__BITS_LEAKED)])

def _int_to_bits(i: int) -> str:
    return ''.join(['1' if bit == '1' else '0' for bit in bin(i)[2:]])

def print_bounds(bounds: tuple[int, int]) -> None:
    print("[" + str(bounds[0]) + "," + str(bounds[1]) + "]")

def __oracle(ciphertext: int) -> int:
    dec = decrypt(ciphertext, __oracle_key)

    binary_str = _bytes_to_bits(dec)
    if __PRINT: print(
        "Oracle received:".ljust(__STR_PAD),
        str(binary_str[::-1] + f"\033[34m{binary_str[-1]}\033[0m").ljust(9 + 13),
        "|",
        str(dec).rjust(4)
    )

    # può restituire 1 perché il messaggio è moltiplicato modulo n
    # nel momento in cui 2m supera n il risultato è 2m % n = 2m - n
    # essendo n sempre dispari, 2m sarà sempre pari e 2m - n sarà sempre dispari

    lsb =  dec % (2 ** __BITS_LEAKED)
    return lsb


class LsbOracleAttack():
    BITS_LEAKED = 1
    PRINT = False

    panic_i_dont_have_e = None

    def get_messages_dont_have_e(self) -> int:
        return 2**self.BITS_LEAKED

    def set_enc_dont_have_e(self, enc: int) -> None:
        self.panic_i_dont_have_e = enc

    def attack(self, ciphertext: int, e: Union[int, None], N: int, dec_oracle: Callable[[int], int]) -> int:
        print(f"LSB oracle attack with {self.BITS_LEAKED} bits leaked")
        decimal.getcontext().prec = N.bit_length()
        bounds = (decimal.Decimal(0), decimal.Decimal(N))
        if not e and not self.panic_i_dont_have_e:
            raise ValueError("I don't have e, please provide it")
        if not e:
            const = self.panic_i_dont_have_e
        else:
            const = pow(2**self.BITS_LEAKED, e, N)

        # for i in range(N.bit_length() // (self.BITS_LEAKED)):
        i=-1
        while bounds[1]-bounds[0] > 1:
            i += 1
            if self.PRINT: print(i, bounds[1]-bounds[0])
            ciphertext = (const * ciphertext) % N

            bits = dec_oracle(ciphertext)
            bits = _int_to_bits(bits)

            bits = bits.rjust(self.BITS_LEAKED, '0')
            if self.PRINT: print(f"Received bits: {bits}")
            for bit in bits:
                bit = int(bit)
                if  bit == 0:
                    bounds = (bounds[0], (bounds[1] + bounds[0]) // 2)
                elif bit == 1:
                    bounds = ((bounds[1] + bounds[0]) // 2, bounds[1])
                else:
                    print(bits, bit, type(bits), type(bit), len(bits), len(bit))
                    raise ValueError("Invalid bit")
            
        print(f"Result forund in {i} iterations")
        return int(bounds[0])

if __name__ == "__main__":
    __PRINT = False
    __BITS_LEAKED = 2

    m = b"flag{dosisido}"
    c = encrypt(m, __oracle_key)
    attack = LsbOracleAttack()
    attack.BITS_LEAKED = __BITS_LEAKED
    attack.PRINT = __PRINT

    if __PRINT: print(
        "Original message:".ljust(__STR_PAD),
        str(_bytes_to_bits(m)).ljust(13),
        "|",
        str(bytes_to_long(m)).rjust(4)
    )
    if __PRINT: print(
        "Ciphertext:".ljust(__STR_PAD),
        str(_bytes_to_bits(long_to_bytes(c))).ljust(13),
        "|",
        str(c).rjust(4)
    )

    r = attack.attack(c, __oracle_key.e, __oracle_key.n, __oracle)
    print(f"Recovered message: {long_to_bytes(r)}")
    print(f"Distance: {abs(bytes_to_long(m) - r)}")

    # r = attack.attack(c, __oracle_key.e, __oracle_key.n, __oracle)
    # print(f"Recovered message: {long_to_bytes(r)}")