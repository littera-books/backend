import string
import random

ascii_table = string.ascii_letters + string.digits
ran_list = [random.choice(ascii_table) for _ in range(8)]
ran_str = ''.join(ran_list)
