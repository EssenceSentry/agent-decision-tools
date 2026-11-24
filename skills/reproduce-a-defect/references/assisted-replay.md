# Capture a manual boundary observation

Use the [assisted reproduction template](../assets/assisted_replay.py) when a real user's interaction is the only affordable way to observe the defect. First try the local fixture or a recorded example. If manual observation is justified, copy the template to a disposable directory, replace its sample steps and prompts with the exact case, and run `python3 assisted_replay.py` in an interactive terminal with the participant's agreement. The participant handles any account interaction themselves.

Each step waits for the participant. The final lines contain the observed yes/no and error category. Capture only the minimum nonsensitive observation. Compare the result with the predicted output and verify the same action after the change. An interrupted or incomplete replay supports no pass/fail verdict.

The prompt and capture functions come from Pocock's diagnosing-bugs package. This version uses a local fixture and asks for an error category. The upstream MIT license is included.
