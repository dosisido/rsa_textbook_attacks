from Crypto.PublicKey import RSA
from basic_rsa import encrypt, decrypt
from Crypto.Util.number import long_to_bytes
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def get_messages_to_encrypt(enc_flag: int, key: RSA.RsaKey):
    return 2**key.e * enc_flag % key.n

def blind_message(encrypted: int, key: RSA.RsaKey):
    inv_2 = pow(2, -1, key.n)
    return encrypted * inv_2 % key.n



def main():
    from secret import message
    key = RSA.generate(2**10)

    # this is done on the server
    enc_flag = encrypt(message, key)


    # let's suppose i can decript anyting besides the flag
    c = get_messages_to_encrypt(enc_flag, key)
    two_m = decrypt(c, key)
    m = blind_message(two_m, key)


    print("Decrypted message:", long_to_bytes(m).decode())



if __name__ == "__main__":
    main()