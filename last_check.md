## General

### Subprocess: windows vs. linux
Change in test_restarting_counter.py
PYTHONPATH with semiu colons

Not checked on linux though

### Requirements with versions

## Missing

**PermissionError** for the counters handling

**Thread safety**: Ensure that all critical sections are properly locked. For example, in _expend_length_id, you modify id_length and max_ids without a lock, which could lead to race conditions.

**Batch Allocation**: When allocating a batch, you increment the counter and save it. However, if the program crashes before saving, you could lose IDs. Consider saving the counter before incrementing it.
I decided to prefer loosing a bit of few ids but still have a clean counter.

**Counter Reset**: If the counter reaches max_ids, I  reset it to 0 and increase the ID length. It's ok but no garanty the transition is thread safe

``` python
def _allocate_batch(self):
    with self.lock:
        start = self.counter
        self._save_counter(start + self.batch_size)  # Save before incrementing
        self.counter += self.batch_size
    return itertools.count(start)
```

**Alert system**: 
So far it's just a print, it would be integrated into whatever log and monitoring system the app uses. 

## Pytest

``` shell
python -m coverage xml -o coverage.xml

python -m coverage report --omit=*/tests/test_*

python -m pytest .  --log-cli-level 20
```
