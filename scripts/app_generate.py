
import os
import sys
from pprint import pprint

p = os.path.abspath(".")
if p not in sys.path:
    sys.path.append(p)

from identity.generation import IDGenerator


def call_bulk_generation(num):
    id_gen = IDGenerator(filename="id_counter.txt")
    result = id_gen.generate_bulk(num)
    return result

if __name__ == "__main__":
    pprint(call_bulk_generation(1002))