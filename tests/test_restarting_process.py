import subprocess
import time
import os
import sys

import pytest


def test_restarting_process_does_not_duplicate_ids():
    # filename = "tests/counters/token_restarting_counter.txt"
    # with open(filename, "w", encoding="utf-8") as file:
    #     file.write("0")
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

    process = subprocess.Popen(
        [python_command, "-u", generate_script_path], stdout=subprocess.PIPE, env=env
    )
    time.sleep(2)
    process.kill()
    for incoming_id in process.stdout.readlines():
        incoming_id = incoming_id.strip()
        ids.add(incoming_id)

    process = subprocess.Popen(
        [python_command, "-u", generate_script_path], stdout=subprocess.PIPE, env=env
    )
    time.sleep(2)
    process.kill()
    for incoming_id in process.stdout.readlines():
        incoming_id = incoming_id.strip()
        # Here's our duplicate check. Restarting the process should
        # not duplicate the ids we get from it.
        assert incoming_id not in ids
        ids.add(incoming_id)
    # And we should have got at least 2
    assert len(ids) > 1
