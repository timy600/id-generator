# -*- coding: utf-8 -*-
"""
RegexFormator Module

This module provides functionality to manage the length of IDs used in a system.
It includes methods to load the current length from a file and update it as needed.
This is particularly useful in scenarios where the ID length needs to be dynamically
adjusted based on certain conditions, such as reaching the maximum number of IDs
for a given length.

Classes:
    RegexFormator: Manages the length of IDs by loading and updating the length value from a file.

Functions:
    No standalone functions are defined in this module.
"""


class RegexFormator:
    """
    A class to manage the length of IDs by loading and updating the length value from a file.

    Attributes:
        filename_length (str): The path to the file containing the ID length. Default is "identity/id_length.txt".

    Methods:
        load_length(): Loads the ID length from the file.
        update_length(value): Updates the ID length in the file with a new value.
    """
    def __init__(
        self,
        filename_length="identity/id_length.txt",
    ):
        """
        Initializes the RegexFormator with the path to the file containing the ID length.

        Args:
            filename_length (str): The path to the file containing the ID length. Default is "identity/id_length.txt".
        """
        self.filename_length = filename_length

    def load_length(self):
        """
        Loads the ID length from the file.

        Returns:
            int: The ID length read from the file. Returns 7 if the file is not found.
        """
        try:
            with open(self.filename_length, "r", encoding="utf-8") as file:
                return int(file.read())
        except FileNotFoundError:
            return 7

    def update_length(self, value=8):
        """
        Updates the ID length in the file with a new value.

        Args:
            value (int): The new ID length to be written to the file. Default is 8.

        Raises:
            FileNotFoundError: If the file specified by filename_length does not exist.
        """
        try:
            with open(self.filename_length, "w", encoding="utf-8") as file:
                file.write(str(value))
        except FileNotFoundError:
            raise FileNotFoundError
