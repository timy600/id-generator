# -*- coding: utf-8 -*-

import re
import pytest
from concurrent.futures import ThreadPoolExecutor
from identity.generation import generate, generate_bulk, IDGenerator
from identity.constants import ID_CHARACTERS

format_check = re.compile('^[' + ID_CHARACTERS + ']{7}$')
id_gen = IDGenerator()


def test_id_is_the_correct_length():
    assert len(generate()) == 7
    assert len(id_gen.generate()) == 7

def test_generate_proper_type():
    assert type(id_gen.generate()) is str
    assert type(id_gen.generate_bulk()) is list
    assert type(id_gen.generate_bulk()[0]) is str


def test_id_uses_correct_characters():
    generated_id = id_gen.generate()
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
        generated_ids.update(id_gen.generate_bulk(1000))
        generated_count += 1
        assert len(generated_ids) == generated_count * 1000


def test_concurrent_bulk_generation():
    id_gen = IDGenerator()
    generated_ids = set()
    bulk_args = []
    for _ in range(0, 200):
        bulk_args.append(2500)

    def consumer_function(ids):
        return list(ids)

    with ThreadPoolExecutor(max_workers=9) as pool:
        generators = list(pool.map(id_gen.generate_bulk, bulk_args))
        ids = list(pool.map(consumer_function, generators))

        for chunk in ids:
            generated_ids.update(chunk)

    assert len(generated_ids) == 500000 #5000000
