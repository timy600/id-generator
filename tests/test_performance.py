# -*- coding: utf-8 -*-

import re
import mock
from pprint import pprint
import pytest
from concurrent.futures import ThreadPoolExecutor
from identity.generation import IDGenerator

ID_CHARACTERS = "0ABCDEFG"
format_check = re.compile("^[" + ID_CHARACTERS + "]{7}$")
filename = "tests/counters/token_performance_counter.txt"


@pytest.mark.timeout(6000)
def test_generate_bulk_performance():
    """This test verifies bulk ID generation performance and format compliance."""
    with open(filename, "w", encoding="utf-8") as file:
        file.write("0")

    id_gen = IDGenerator(
        id_characters=ID_CHARACTERS,
        filename=filename
        )

    def bulk_generate(_):
        return id_gen.generate_bulk(209710)
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(bulk_generate, range(5)))

    all_ids = [id_ for batch in results for id_ in batch]  # Flatten results

    # Ensure all generated IDs match the expected format
    assert all(format_check.match(id_) for id_ in all_ids)


@pytest.mark.timeout(6000)
def test_alert_90_percent():
    """This test verifies that an alert is sent when reaching 90% of IDs permutations."""
    encoding_base = len(ID_CHARACTERS)
    id_length = 7
    limit_90 = (encoding_base**id_length) * 0.9
    workers = 2
    divmod(limit_90, workers)

    # Set the counter to 1887432, a bit before 90% of the max IDs
    with open(filename, "w", encoding="utf-8") as file:
        file.write(str(int(limit_90)-4))

    id_gen = IDGenerator(
        id_characters=ID_CHARACTERS,
        filename=filename
    )

    def bulk_generate(_):
        return [id_gen.generate() for _ in range(3)] # just enougth to pass the 90% mark

    with ThreadPoolExecutor(max_workers=workers) as executor:
        results = list(executor.map(bulk_generate, range(workers)))

    all_ids = [id_ for batch in results for id_ in batch]  # Flatten results
    for id_ in all_ids:
        print(f"[DEBUG] id_checked: {id_}")
        assert format_check.match(id_)

    # Check if the alert was sent
    assert "Approaching ID limit" in id_gen.alerts
    # Check the Debug by crashing with the next line:
    # assert "Approaching ID limit" not in id_gen.alerts