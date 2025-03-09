# -*- coding: utf-8 -*-

ID_CHARACTERS = "0123456789ABCDEFGHJKLMNPQRSTUVWXYZ"

class RegexFormator:
    def __init__(
            self,
            filename_length="identity/id_length.txt",
        ):
        self.filename_length = filename_length
        
    def load_length(self):
        try:
            with open(self.filename_length, "r", encoding="utf-8") as file:
                return int(file.read())
        except FileNotFoundError:
            return 7

    def update_length(self, value=8):
        try:
            with open(self.filename_length, "w", encoding="utf-8") as file:
                file.write(str(value))
        except FileNotFoundError:
            raise FileNotFoundError
