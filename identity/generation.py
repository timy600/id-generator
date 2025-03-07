# -*- coding: utf-8 -*-

import random
import threading
import itertools

from .constants import ID_CHARACTERS, BASE


def generate():
    """Generates a unique 7-character ID"""
    return "".join(random.choices(ID_CHARACTERS, k=7))


def generate_bulk(n=1):
    """Generates 'n' unique IDs efficiently"""
    return [generate() for _ in range(n)]


class IDGenerator:
    def __init__(self, filename='id_counter.txt', batch_size=1000):
        self.filename = filename
        self.batch_size = batch_size  # Preallocated batch size
        self.lock = threading.Lock()
        self.counter = self._load_counter()
        self.local_counter = itertools.count(self.counter)  # Thread-local batch counter
    # def __init__(self, filename='id_counter.txt'):
    #     self.filename = filename
    #     self.lock = threading.Lock()
    #     self.counter = self._load_counter()

    def _load_counter(self):
        try:
            with open(self.filename, 'r') as file:
                return int(file.read().strip())
        except FileNotFoundError:
            return 0

    # def _save_counter(self):
    #     with open(self.filename, 'w') as file:
    #         file.write(str(self.counter))
    #     # """Loads the last used counter from a file or starts from 1,000,000"""
    #     # try:
    #     #     with open(self.filename, 'r') as file:
    #     #         return int(file.read().strip())
    #     # except FileNotFoundError:
    #     #     return 1_000_000  # Start from a high number to ensure 7-char length

    def _save_counter(self, value):
        """Saves the last allocated counter to the file"""
        with open(self.filename, 'w') as file:
            file.write(str(value))

    def _allocate_batch(self):
        """Allocates a new batch range for a thread, avoiding locks for each ID"""
        with self.lock:
            start = self.counter
            self.counter += self.batch_size  # Allocate next batch
            self._save_counter(self.counter)  # Persist only after batch allocation
        return itertools.count(start)
    
    def _base34_encode(self, num):
        # performance: 76.97s, 77.15s, 93.02s, 94.02s, 88.63s
        """Encodes number into base34 (A-Z, 0-9, excluding I and O)"""
        res = []
        while num:
            num, remainder = divmod(num, BASE)
            res.append(ID_CHARACTERS[remainder])
        return ''.join(res[::-1]).zfill(7)

    def _base34_encode_str(self, num):
        # performance: 78.82s, 99.52s, 96.21s
        id_str = ''
        while num:
            id_str = ID_CHARACTERS[num % BASE] + id_str
            num //= BASE
        # Pad with leading zeros if necessary
        return id_str.zfill(7)

    def _generate(self):
        """Old version"""
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

    def generate(self):
        """Generates a unique 7-character ID"""
        try:
            id_num = next(self.local_counter)
        except StopIteration:
            self.local_counter = self._allocate_batch()
            id_num = next(self.local_counter)
        
        return self._base34_encode(id_num)
    

    def generate_bulk(self, n=1):
        """Generates 'n' unique IDs efficiently"""
        return [self.generate() for _ in range(n)]
