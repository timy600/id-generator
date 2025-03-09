# -*- coding: utf-8 -*-
"""
Generation Module

This module provides the core functionality for generating unique IDs. It manages the ID generation process, including handling the counter, encoding IDs, and expanding the ID length when necessary. The module ensures thread safety and persists the counter state to a file.

Classes:
    IDGenerator: Manages the generation of unique IDs, including counter management, encoding, and length expansion.

Functions:
    No standalone functions are defined in this module.
"""

import threading
import itertools
import atexit
from .constants import ID_CHARACTERS
from .regex_formator import RegexFormator

class IDGenerator:
    """
    A class to manage the generation of unique IDs. It handles counter management, encoding,
    and length expansion to ensure unique IDs are generated efficiently.

    Attributes:
        id_characters (str): The set of characters used for encoding IDs.
        encoding_base (int): The base used for encoding IDs, derived from the length of id_characters.
        filename (str): The path to the file storing the counter value.
        batch_size (int): The size of the preallocated batch for ID generation.
        lock (threading.Lock): A lock to ensure thread safety when updating the counter.
        counter (int): The current counter value for ID generation.
        local_counter (itertools.count): A thread-local counter for batch allocation.
        alerts (list): A list to store alert messages.
        regex_formator (RegexFormator): An instance to manage the ID length format.
        id_length (int): The current length of the IDs.
        max_ids (int): The maximum number of IDs for the current length.

    Methods:
        _save_counter_on_exit(): Ensures the counter is saved when the program exits.
        _load_counter(): Loads the counter value from the file.
        _save_counter(value): Saves the counter value to the file.
        _allocate_batch(): Allocates a new batch range for a thread.
        _expend_length_id(): Increases the length of the IDs.
        _base34_encode(num): Encodes a number into the current base.
        generate(): Generates a unique ID.
        generate_bulk(num): Generates multiple unique IDs efficiently.
        _send_alert(message): Sends an alert or logs a warning.
    """

    def __init__(
        self,
        filename="id_counter.txt",
        batch_size=1000,
        id_characters=ID_CHARACTERS,
        filename_length="identity/id_length.txt",
    ):
        """
        Initializes the IDGenerator with the necessary parameters for ID generation.

        Args:
            filename (str): The path to the file storing the counter value. Default is "id_counter.txt".
            batch_size (int): The size of the preallocated batch for ID generation. Default is 1000.
            id_characters (str): The set of characters used for encoding IDs. Default is ID_CHARACTERS.
            filename_length (str): The path to the file storing the ID length. Default is "identity/id_length.txt".
        """
        self.id_characters = id_characters
        self.encoding_base = len(id_characters)
        self.filename = filename
        self.batch_size = batch_size
        self.lock = threading.Lock()
        self.counter = self._load_counter()
        self.local_counter = itertools.count(self.counter)
        self.alerts = []

        self.regex_formator = RegexFormator(filename_length=filename_length)
        self.id_length = self.regex_formator.load_length()
        self.max_ids = self.encoding_base**self.id_length - 1

        atexit.register(self._save_counter_on_exit)

        if self.counter > 0.9 * self.max_ids:
            self._send_alert("Approaching ID limit")

    def _save_counter_on_exit(self):
        """Ensures the counter is saved when the program exits."""
        with self.lock:
            self._save_counter(int(next(self.local_counter)))

    def _load_counter(self):
        """
        Loads the counter value from the file.

        Returns:
            int: The counter value read from the file. Returns 0 if the file is not found or invalid.
        """
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                return int(file.read().strip())
        except (FileNotFoundError, ValueError):
            return 0

    def _save_counter(self, value):
        """
        Saves the counter value to the file.

        Args:
            value (int): The counter value to be saved.

        Raises:
            FileNotFoundError: If the file specified by filename does not exist.
        """
        try:
            with open(self.filename, "w", encoding="utf-8") as file:
                file.write(str(value))
        except FileNotFoundError:
            raise FileNotFoundError(f"The file {self.filename} was not found.")

    def _allocate_batch(self):
        """
        Allocates a new batch range for a thread, avoiding locks for each ID.

        Returns:
            itertools.count: A new counter starting from the allocated batch range.
        """
        with self.lock:
            start = self.counter
            self.counter += self.batch_size
            self._save_counter(self.counter)
        return itertools.count(start)

    def _expend_length_id(self):
        """Increases the length of the IDs and updates the maximum IDs value."""
        self.id_length += 1
        self.regex_formator.update_length(self.id_length)
        self.max_ids = self.encoding_base**self.id_length - 1
        self.current_counter = 0

    def _base34_encode(self, num):
        """
        Encodes a number into the current base using the specified characters.

        Args:
            num (int): The number to be encoded.

        Returns:
            str: The encoded ID as a string.
        """
        res = []
        while num:
            num, remainder = divmod(num, self.encoding_base)
            res.append(self.id_characters[remainder])
        return "".join(res[::-1]).zfill(self.id_length)

    def generate(self):
        """
        Generates a unique ID.

        Returns:
            str: The generated unique ID.
        """
        try:
            id_num = next(self.local_counter)
        except StopIteration:
            self.local_counter = self._allocate_batch()
            id_num = next(self.local_counter)

        if id_num == int(self.max_ids * 0.9):
            self._send_alert("Approaching ID limit")

        if id_num % self.batch_size == 0:
            self._save_counter(id_num)

        new_id = self._base34_encode(id_num)

        if id_num == int(self.max_ids):
            self._send_alert("Expending the length of ID")
            self._expend_length_id()

        return new_id

    def generate_bulk(self, num=1):
        """
        Generates multiple unique IDs efficiently.

        Args:
            num (int): The number of IDs to generate. Default is 1.

        Returns:
            list: A list of generated unique IDs.
        """
        ids = [self.generate() for _ in range(num)]
        self._save_counter(next(self.local_counter))
        return ids

    def _send_alert(self, message):
        """
        Sends an alert or logs a warning.

        Args:
            message (str): The alert message to be logged.
        """
        self.alerts.append(message)
        print(f"ALERT: {message}")
