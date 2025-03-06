# -*- coding: utf-8 -*-

import random

from .constants import ID_CHARACTERS


def generate():
    id = random.choices(ID_CHARACTERS, k=7)
    return "".join(id)
