from Crypto.PublicKey import RSA
from basic_rsa import encrypt, decrypt
from Crypto.Util.number import long_to_bytes
from secret import message
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))



def main():
    key = RSA.generate(2**10)

    # this is done on the server
    enc_flag = encrypt(message, key)

    # let's suppose i can decript anyting besides the flag
    c = 2**key.e * enc_flag % key.n
    two_m = decrypt(c, key)
    inv_2 = pow(2, -1, key.n)
    m = two_m * inv_2 % key.n

    print("Decrypted message:", long_to_bytes(m).decode())


if __name__ == "__main__":
    main()