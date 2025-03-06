# -*- coding: utf-8 -*-

import random

from .constants import ID_CHARACTERS


def generate(n=1):
    new_ids = set()
    while len(new_ids) < n:
        new_id = "".join(random.choices(ID_CHARACTERS, k=7))
        new_ids.add(new_id)
    return list(new_ids)
