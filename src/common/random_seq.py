import string
import random

ascii_table = string.ascii_letters + string.digits


def make_rand_seq():
    ran_list = [random.choice(ascii_table) for _ in range(8)]
    return ''.join(ran_list)
