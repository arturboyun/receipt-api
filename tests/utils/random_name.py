import random
import string


def random_lower_string(length=20):
    return "".join(random.choice(string.ascii_lowercase) for _ in range(length))


def get_random_name():
    return random_lower_string(20)
