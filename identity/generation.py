# -*- coding: utf-8 -*-

import random
import threading

from .constants import ID_CHARACTERS, BASE


def generate():
    return "".join(random.choices(ID_CHARACTERS, k=7))


def generate_bulk(n=1):
    new_ids = set()
    while len(new_ids) < n:
        new_id = generate()
        new_ids.add(new_id)
    return list(new_ids)


class IDGenerator:
    def __init__(self, filename='id_counter.txt'):
        self.filename = filename
        self.lock = threading.Lock()
        self.counter = self._load_counter()

    def _load_counter(self):
        try:
            with open(self.filename, 'r') as file:
                return int(file.read().strip())
        except FileNotFoundError:
            return 0

    def _save_counter(self):
        with open(self.filename, 'w') as file:
            file.write(str(self.counter))

    def generate(self):
        with self.lock:
            self.counter += 1
            id_num = self.counter
            self._save_counter()

        # Convert the counter to a base-32 string
        id_str = ''
        while id_num:
            id_str = ID_CHARACTERS[id_num % BASE] + id_str
            id_num //= BASE

        # Pad with leading zeros if necessary
        return id_str.zfill(7)

    def generate_bulk(self, n=1):
        new_ids = set()
        while len(new_ids) < n:
            new_id = self.generate()
            new_ids.add(new_id)
        return list(new_ids)
