import string
import random  # replace par secrets pour la secu

class Utils:

    chars = string.ascii_letters + "1234567890" + string.digits + "-_"

    @staticmethod
    def ur_safe_key(key_prefix: str = None, key_len: int = 2):

        if type(key_len) is not int:
            raise TypeError(f"key_len got {type(key_len)} instead of an int")
        if type(key_prefix) is not str and key_prefix is not None:
            raise TypeError(f"key_prefix got {type(key_prefix)} instead of a str")

        return f'{key_prefix + "." if key_prefix is not None else ""}' + "".join(random.choice(Utils.chars) for _ in range(key_len))
