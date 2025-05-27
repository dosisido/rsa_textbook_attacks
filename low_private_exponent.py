

from typing import Optional

class LowPrivateExponent():
    @staticmethod
    def wiener(e: int, n: int) -> Optional[int]:
        from owiener import attack
        return attack(e, n)

    @staticmethod
    def boneh_durfee():
        raise NotImplementedError("Launch the boneh_durfee.sage script")

def main():
    from rsa_textbook_attacks.basic_rsa import gen_keys, print_key
    attack = LowPrivateExponent()

    key = gen_keys(100, d=17)
    print_key(key)

    d = attack.wiener(key.e, key.n)
    print("Found d:", d)


if __name__ == "__main__":
    main()