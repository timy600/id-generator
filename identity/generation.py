# -*- coding: utf-8 -*-

import random

from .constants import ID_CHARACTERS


def generate():
    return "".join(random.choices(ID_CHARACTERS, k=7))


def generate_bulk(n=1):
    new_ids = set()
    while len(new_ids) < n:
        new_id = generate()
        new_ids.add(new_id)
    return list(new_ids)
