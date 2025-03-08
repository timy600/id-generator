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
