from Crypto.PublicKey import RSA
from rsa_textbook_attacks.basic_rsa import encrypt, decrypt
from rsa_textbook_attacks.tools import modular_multiplication
from Crypto.Util.number import long_to_bytes


# def get_messages_to_encrypt(enc_flag: int, key: RSA.RsaKey) -> int:
#     return (pow(2, key.e, key.n) * enc_flag) % key.n

def get_messages_to_encrypt(enc_flag: int, key: RSA.RsaKey) -> int:
    return modular_multiplication(pow(2, key.e, key.n), enc_flag, key.n)

def blind_message(encrypted: int, n: int) -> int:
    inv_2 = pow(2, -1, n)
    return encrypted * inv_2 % n



def main():
    from secret import message
    key = RSA.generate(1024)

    # this is done on the server
    enc_flag = encrypt(message, key)


    # let's suppose i can decript anyting besides the flag
    c = get_messages_to_encrypt(enc_flag, key)
    two_m = decrypt(c, key)
    m = blind_message(two_m, key)


    print("Decrypted message:", long_to_bytes(m).decode())



if __name__ == "__main__":
    main()