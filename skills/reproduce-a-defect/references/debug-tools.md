# Narrow a failing test

From a disposable checkout, pass the actual runner and an ordered list of test files to the [pollution locator](../scripts/find_polluter.py). It runs each file separately and tests for the first appearance of a previously absent path after each successful run. Use the same setup, order and environment as the failing suite. Runner failures or timeouts are inconclusive. Interactions requiring the same process may need a custom runner that replays prefixes.

```sh
python3 "$EXECUTION_SKILL/scripts/find_polluter.py" --watch stray.json --runner python3 --arg=-m --arg=pytest --arg=-q -- tests/test_read.py tests/test_write.py
```

Exit codes are 0 for no observed pollution, 1 for an observed producer and 2 for invalid input or a failed trial. The helper leaves the artifact for inspection.

## Wait on the condition

For asynchronous state with an observable completion signal, poll a fast probe for that signal, bound the wait and name the expected event in the timeout. Use a fixed delay only for a real timing requirement, and start its clock after the triggering event.

```python
import time


def wait_for(probe, description, timeout=2.0, interval=0.01):
    """Return the first probe result that is not None, or raise at the bound."""
    deadline = time.monotonic() + timeout
    while (value := probe()) is None:
        if time.monotonic() >= deadline:
            raise TimeoutError(f"timed out after {timeout}s waiting for {description}")
        time.sleep(interval)
    return value
```

Zero and `False` are valid results.
