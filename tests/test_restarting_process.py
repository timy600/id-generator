# -*- coding: utf-8 -*-
"""
Test Crashing Module

This module contains tests to ensure that the ID generation process does not produce duplicate IDs when the process is restarted. It verifies the robustness of the ID generation mechanism under crashing and restarting scenarios.
I barely touched this one.

Tests:
    - test_restarting_process_does_not_duplicate_ids: Ensures that restarting the ID generation process does not result in duplicate IDs.

Dependencies:
    - pytest: For running the tests.
    - subprocess: For managing the ID generation process.
    - os, sys, time: For environment setup and process management.
"""

import subprocess
import time
import os
import sys
import pytest

def test_restarting_process_does_not_duplicate_ids():
    """
    Tests that restarting the ID generation process does not produce duplicate IDs.

    This test simulates a crash by killing the ID generation process and then restarting it. It verifies that the IDs generated after the restart do not duplicate those generated before the crash.
    """
    ids = set()
    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"
    env["PYTHONPATH"] = (
        os.getcwd()
        + (";" if sys.platform == "win32" else ":")
        + env.get("PYTHONPATH", "")
    )

    python_command = "python" if sys.platform == "win32" else "/usr/bin/env python"
    generate_script_path = os.path.join("scripts", "generate.py")

    # Start the ID generation process
    process = subprocess.Popen(
        [python_command, "-u", generate_script_path], stdout=subprocess.PIPE, env=env
    )
    time.sleep(2)
    process.kill()

    # Collect IDs from the first run
    for incoming_id in process.stdout.readlines():
        incoming_id = incoming_id.strip()
        ids.add(incoming_id)

    # Restart the ID generation process
    process = subprocess.Popen(
        [python_command, "-u", generate_script_path], stdout=subprocess.PIPE, env=env
    )
    time.sleep(2)
    process.kill()

    # Collect IDs from the second run and check for duplicates
    for incoming_id in process.stdout.readlines():
        incoming_id = incoming_id.strip()
        assert incoming_id not in ids  # Ensure no duplicate IDs
        ids.add(incoming_id)

    # Ensure that at least two unique IDs were generated
    assert len(ids) > 1

def test_reset_values():
    filenames = [
        "tests/counters/token_generation_counter.txt",
        "tests/counters/token_performance_counter.txt",
        "tests/counters/token_restarting_counter.txt"
    ]
    for filename in filenames:
        with open(filename, "w", encoding="utf-8") as file:
            file.write("0")
    for filename in filenames:
        with open(filename, "r", encoding="utf-8") as file:
            assert int(file.read()) == 0

    length_filename = "identity/testing_id_length.txt"
    with open(length_filename, "w", encoding="utf-8") as file:
        file.write("7")
    with open(length_filename, "r", encoding="utf-8") as file:
        assert int(file.read()) == 7
