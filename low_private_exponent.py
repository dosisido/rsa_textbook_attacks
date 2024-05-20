from basic_rsa import gen_keys, print_key
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from owiener import attack as wiener_attack


def main():
    
    key = gen_keys(100, d=17)
    print_key(key)

    found_d = wiener_attack(key.e, key.n)
    print("Found d:", found_d)


if __name__ == "__main__":
    main()