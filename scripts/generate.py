import sys

from identity.generation import IDGenerator

id_gen = IDGenerator(filename="tests/counters/token_restarting_counter.txt")
while True:
    for _ in id_gen.generate_bulk(10):
        sys.stdout.write(f"{_}\n")
