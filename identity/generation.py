# -*- coding: utf-8 -*-

import random
import threading
import itertools
import atexit

from .constants import ID_CHARACTERS


class IDGenerator:
    def __init__(
            self,
            filename="id_counter.txt",
            batch_size=1000,
            id_characters=ID_CHARACTERS
        ):
        self.id_characters = id_characters
        self.encoding_base = len(id_characters)
        self.filename = filename
        self.batch_size = batch_size  # Preallocated batch size
        self.lock = threading.Lock()
        self.counter = self._load_counter()
        self.local_counter = itertools.count(self.counter)  # Thread-local batch counter

        atexit.register(self._save_counter_on_exit)
    
    def _save_counter_on_exit(self):
        """Ensures the counter is saved when the program exits."""
        with self.lock:
            self._save_counter(next(self.local_counter))  # Save the latest counter

    def _load_counter(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                return int(file.read().strip())
        except FileNotFoundError:
            return 0

    def _save_counter(self, value):
        """Saves the last allocated counter to the file"""
        try:
            with open(self.filename, "w", encoding="utf-8") as file:
                file.write(str(value))
                # return int(file.read().strip())
        except FileNotFoundError:
            # return 1_000_000  # Start from a high number to ensure 7-char length
            raise FileNotFoundError

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
            num, remainder = divmod(num, self.encoding_base)
            res.append(self.id_characters[remainder])
        return "".join(res[::-1]).zfill(7)

    def generate(self):
        """Generates a unique 7-character ID"""
        try:
            id_num = next(self.local_counter)
        except StopIteration:
            self.local_counter = self._allocate_batch()
            id_num = next(self.local_counter)

        return self._base34_encode(id_num)

    def generate_bulk(self, num=1):
        """Generates 'n' unique IDs efficiently"""
        return [self.generate() for _ in range(num)]
