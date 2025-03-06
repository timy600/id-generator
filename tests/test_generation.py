# -*- coding: utf-8 -*-

import re
import pytest
from identity.generation import generate
from identity.constants import ID_CHARACTERS

format_check = re.compile('^[' + ID_CHARACTERS + ']{7}$')


def test_id_is_the_correct_length():
    assert len(generate()[0]) == 7


def test_generate_proper_type():
    assert type(generate()[0]) is str
    assert type(generate()) is list


def test_id_uses_correct_characters():
    generated_id = generate()
    check = re.compile('^[' + ID_CHARACTERS + ']+$')
    assert check.match(generated_id[0]) is not None


def test_ids_are_unique_and_correct_format():
    ids = set()
    for i in range(0, 10000):
        ids.add(generate()[0])
    assert len(ids) == 10000
    generated_count = 0
    while generated_count < 22000:
        generated_id = generate()
        generated_count += 1
        assert generated_id[0] not in ids
        ids.add(generated_id[0])
        assert format_check.match(generated_id[0]) is not None


def test_bulk_generation():
    ids = generate(10000)
    assert len(ids) == 10000


def test_ids_are_unique_generated_in_bulk():
    generated_ids = set()
    generated_count = 0
    while generated_count < 100:
        generated_ids.update(generate(1000))
        generated_count += 1
        assert len(generated_ids) == generated_count * 1000
