# -*- coding: utf-8 -*-

import re
import pytest
from identity.generation import generate
from identity.constants import ID_CHARACTERS


def test_id_is_the_correct_length():
    assert len(generate()[0]) == 7


def test_generate_proper_type():
    assert type(generate()[0]) is str
    assert type(generate()) is list


def test_id_uses_correct_characters():
    generated_id = generate()
    check = re.compile('^[' + ID_CHARACTERS + ']+$')
    assert check.match(generated_id[0]) is not None


def test_ids_are_unique():
    ids = set()
    for i in range(0, 1000000):
        ids.add(generate()[0])
    assert len(ids) == 1000000


def test_bulk_generation():
    ids = generate(10000)
    assert len(ids) == 10000
