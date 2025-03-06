# -*- coding: utf-8 -*-

import re
import pytest
from identity.generation import generate, generate_bulk
from identity.constants import ID_CHARACTERS

format_check = re.compile('^[' + ID_CHARACTERS + ']{7}$')


def test_id_is_the_correct_length():
    assert len(generate()) == 7


def test_generate_proper_type():
    assert type(generate()) is str
    assert type(generate_bulk()) is list
    assert type(generate_bulk()[0]) is str


def test_id_uses_correct_characters():
    generated_id = generate()
    assert format_check.match(generated_id) is not None


def test_ids_are_unique_and_correct_format():
    ids = set()
    generated_count = 0
    while generated_count < 22000:
        generated_id = generate()
        generated_count += 1
        assert generated_id not in ids
        ids.add(generated_id)
        assert format_check.match(generated_id) is not None


def test_bulk_generation():
    ids = generate_bulk(10000)
    assert len(ids) == 10000


def test_ids_are_unique_generated_in_bulk():
    generated_ids = set()
    generated_count = 0
    while generated_count < 100:
        generated_ids.update(generate_bulk(1000))
        generated_count += 1
        assert len(generated_ids) == generated_count * 1000
