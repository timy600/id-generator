# -*- coding: utf-8 -*-
"""
Test Performance Module

This module contains performance tests for the IDGenerator class. It focuses on verifying the efficiency and correctness of bulk ID generation, ensuring alerts are sent when approaching limits, and handling the expansion of ID length when the maximum number of IDs is reached.

Tests:
    - test_generate_bulk_performance: Verifies the performance and format compliance of bulk ID generation.
    - test_alert_90_percent: Ensures an alert is sent when reaching 90% of ID permutations.
    - test_reaching_limit: Tests the behavior when the maximum number of IDs is reached and the ID length is expanded.

Dependencies:
    - pytest: For running the tests.
    - concurrent.futures.ThreadPoolExecutor: For testing concurrent ID generation.
    - identity.generation.IDGenerator: The class being tested.
"""

import re
import pytest
from concurrent.futures import ThreadPoolExecutor
from identity.generation import IDGenerator

# Define the set of characters and format check for the tests
ID_CHARACTERS = "0ABCDEFG"
format_check = re.compile("^[" + ID_CHARACTERS + "]{7}$")
filename = "tests/counters/token_performance_counter.txt"

@pytest.mark.timeout(6000)
def test_generate_bulk_performance():
    """
    Tests the performance and format compliance of bulk ID generation.

    This test ensures that bulk generation of IDs is efficient and that all generated IDs match the expected format.
    """
    with open(filename, "w", encoding="utf-8") as file:
        file.write("0")

    id_gen = IDGenerator(id_characters=ID_CHARACTERS, filename=filename)

    def bulk_generate(_):
        return id_gen.generate_bulk(209710)

    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(bulk_generate, range(5)))

    all_ids = [id_ for batch in results for id_ in batch]  # Flatten results

    # Ensure all generated IDs match the expected format
    assert all(format_check.match(id_) for id_ in all_ids)

@pytest.mark.timeout(6000)
def test_alert_90_percent():
    """
    Tests that an alert is sent when reaching 90% of ID permutations.

    This test verifies that the IDGenerator sends an alert when the number of generated IDs approaches 90% of the maximum possible IDs.
    """
    encoding_base = len(ID_CHARACTERS)
    id_length = 7
    limit_90 = (encoding_base**id_length) * 0.9
    workers = 2

    # Set the counter to a value just before 90% of the max IDs
    with open(filename, "w", encoding="utf-8") as file:
        file.write(str(int(limit_90) - 4))

    id_gen = IDGenerator(id_characters=ID_CHARACTERS, filename=filename)

    def bulk_generate(_):
        return [id_gen.generate() for _ in range(3)]  # Enough to pass the 90% mark

    with ThreadPoolExecutor(max_workers=workers) as executor:
        results = list(executor.map(bulk_generate, range(workers)))

    all_ids = [id_ for batch in results for id_ in batch]  # Flatten results
    for id_ in all_ids:
        print(f"[DEBUG] id_checked: {id_}")
        assert format_check.match(id_)

    # Check if the alert was sent
    assert "Approaching ID limit" in id_gen.alerts

@pytest.mark.timeout(6000)
def test_reaching_limit():
    """
    Tests the behavior when the maximum number of IDs is reached and the ID length is expanded.

    This test ensures that the IDGenerator correctly expands the ID length when the maximum number of IDs is reached and that the new IDs match the expected format.
    """
    encoding_base = len(ID_CHARACTERS)
    id_length = 7
    limit = encoding_base**id_length
    workers = 2

    # Set the counter to a value just before the maximum number of IDs
    with open(filename, "w", encoding="utf-8") as file:
        file.write(str(int(limit) - 4))
    filename_length = "identity/testing_id_length.txt"
    id_gen = IDGenerator(
        id_characters=ID_CHARACTERS, filename=filename, filename_length=filename_length
    )

    def bulk_generate(_):
        return [id_gen.generate() for _ in range(3)]  # Enough to pass the limit

    with ThreadPoolExecutor(max_workers=workers) as executor:
        results = list(executor.map(bulk_generate, range(workers)))

    all_ids = [id_ for batch in results for id_ in batch]  # Flatten results

    format_check_7 = re.compile("^[" + ID_CHARACTERS + "]{7}$")
    print(f"[DEBUG] first id_checked: {all_ids[0]}")
    assert format_check_7.match(all_ids[0])

    format_check_8 = re.compile("^[" + ID_CHARACTERS + "]{8}$")
    print(f"[DEBUG] second id_checked: {all_ids[-1]}")
    assert format_check_8.match(all_ids[-1])

    with open(filename_length, "r", encoding="utf-8") as file:
        assert int(file.read()) == 8

    for id_ in all_ids:
        print(f"[DEBUG] id_checked: {id_}")

    # Check if the alert was sent
    assert "Expending the length of ID" in id_gen.alerts
