

def wiener_attack(e, n):
    from owiener import attack
    return attack(e, n)


def main():
    from basic_rsa import gen_keys, print_key
    
    key = gen_keys(100, d=17)
    print_key(key)

    d = wiener_attack(key.e, key.n)
    print("Found d:", d)


if __name__ == "__main__":
    main()