# -*- coding: utf-8 -*-
"""
Test Generation Module

This module contains tests for the IDGenerator class, focusing on simple ID generation and bulk generation. It ensures that the generated IDs meet the expected format, are unique, and can be generated concurrently.

Tests:
    - test_id_is_the_correct_length: Verifies that the generated ID has the correct length.
    - test_generate_proper_type: Checks that the generated ID and bulk IDs are of the correct type.
    - test_id_uses_correct_characters: Ensures that the generated ID uses the correct set of characters.
    - test_ids_are_unique_and_correct_format: Verifies that generated IDs are unique and match the expected format.
    - test_ids_are_unique_generated_in_bulk: Checks that bulk-generated IDs are unique.
    - test_concurrent_bulk_generation: Tests the concurrent generation of bulk IDs.

Dependencies:
    - pytest: For running the tests.
    - concurrent.futures.ThreadPoolExecutor: For testing concurrent ID generation.
    - identity.generation.IDGenerator: The class being tested.
    - identity.constants.ID_CHARACTERS: The set of characters used for encoding IDs.
"""

import re
import pytest
from concurrent.futures import ThreadPoolExecutor
from identity.generation import IDGenerator
from identity.constants import ID_CHARACTERS

# Regular expression to check the format of the generated IDs
format_check = re.compile("^[" + ID_CHARACTERS + "]{7}$")
filename = "tests/counters/token_generation_counter.txt"

@pytest.fixture
def id_gen():
    """
    Pytest fixture to create an instance of IDGenerator for testing.

    Returns:
        IDGenerator: An instance of IDGenerator initialized with a test counter file.
    """
    return IDGenerator(filename=filename)

def test_id_is_the_correct_length(id_gen):
    """
    Tests that the generated ID has the correct length.

    Args:
        id_gen (IDGenerator): The IDGenerator instance for testing.
    """
    with open(filename, "w", encoding="utf-8") as file:
        file.write("0")

    assert len(id_gen.generate()) == 7

def test_generate_proper_type(id_gen):
    """
    Tests that the generated ID and bulk IDs are of the correct type.

    Args:
        id_gen (IDGenerator): The IDGenerator instance for testing.
    """
    bulk_ids = id_gen.generate_bulk()
    assert isinstance(id_gen.generate(), str)
    assert isinstance(bulk_ids, list)
    assert isinstance(bulk_ids[0], str)

def test_id_uses_correct_characters(id_gen):
    """
    Tests that the generated ID uses the correct set of characters.

    Args:
        id_gen (IDGenerator): The IDGenerator instance for testing.
    """
    generated_id = id_gen.generate()
    assert format_check.match(generated_id) is not None

def test_ids_are_unique_and_correct_format(id_gen):
    """
    Tests that generated IDs are unique and match the expected format.

    Args:
        id_gen (IDGenerator): The IDGenerator instance for testing.
    """
    ids = set()
    generated_count = 0
    while generated_count < 22000:
        generated_id = id_gen.generate()
        generated_count += 1
        assert generated_id not in ids
        ids.add(generated_id)
        assert format_check.match(generated_id) is not None

def test_ids_are_unique_generated_in_bulk(id_gen):
    """
    Tests that bulk-generated IDs are unique.

    Args:
        id_gen (IDGenerator): The IDGenerator instance for testing.
    """
    generated_ids = set()
    generated_count = 0
    while generated_count < 100:
        generated_ids.update(id_gen.generate_bulk(1000))
        generated_count += 1
        assert len(generated_ids) == generated_count * 1000

def test_concurrent_bulk_generation(id_gen):
    """
    Tests the concurrent generation of bulk IDs.

    Args:
        id_gen (IDGenerator): The IDGenerator instance for testing.
    """
    generated_ids = set()
    bulk_args = [250] * 200

    def consumer_function(ids):
        return list(ids)

    with ThreadPoolExecutor(max_workers=9) as pool:
        generators = list(pool.map(id_gen.generate_bulk, bulk_args))
        ids = list(pool.map(consumer_function, generators))

        for chunk in ids:
            generated_ids.update(chunk)

    assert len(generated_ids) == 50000  # 5000000
