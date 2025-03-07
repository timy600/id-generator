import sys

from identity.generation import generate_bulk


while True:
    for _ in generate_bulk(10):
        sys.stdout.write(f"{_}\n")
