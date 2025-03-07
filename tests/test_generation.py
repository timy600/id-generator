# -*- coding: utf-8 -*-

import re
import pytest
from concurrent.futures import ThreadPoolExecutor
from identity.generation import generate, generate_bulk, IDGenerator
from identity.constants import ID_CHARACTERS

format_check = re.compile('^[' + ID_CHARACTERS + ']{7}$')


@pytest.fixture
def id_gen():
    return IDGenerator()


def test_id_is_the_correct_length(id_gen):
    assert len(generate()) == 7
    assert len(id_gen.generate()) == 7


def test_generate_proper_type(id_gen):
    bulk_ids = id_gen.generate_bulk()
    assert isinstance(id_gen.generate(), str)
    assert isinstance(bulk_ids, list)
    assert isinstance(bulk_ids[0], str)


def test_id_uses_correct_characters(id_gen):
    generated_id = id_gen.generate()
    assert format_check.match(generated_id) is not None


def test_ids_are_unique_and_correct_format(id_gen):
    ids = set()
    generated_count = 0
    while generated_count < 22000:
        generated_id = id_gen.generate()
        generated_count += 1
        assert generated_id not in ids
        ids.add(generated_id)
        assert format_check.match(generated_id) is not None


def test_ids_are_unique_generated_in_bulk(id_gen):
    generated_ids = set()
    generated_count = 0
    while generated_count < 100:
        generated_ids.update(id_gen.generate_bulk(1000))
        generated_count += 1
        assert len(generated_ids) == generated_count * 1000


def test_concurrent_bulk_generation(id_gen):
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
