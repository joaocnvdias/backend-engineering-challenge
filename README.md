# Backend Engineering Challenge

A command line tool that reads a stream of translation events and outputs, for every minute, the moving average delivery time over the last X minutes.

## Prerequisites

- Python 3.7+
- Install dependencies:
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
## How to Run
In the root directory, paste the following command to the terminal:
```
python -m unbabel_cli --input_file <path> --window_size <int>
```
Where following are **mandatory parameters:**
- ```--input_file:``` The location of the input file, including its name and suffix. It must be a .jsonl file. 
- ```--window_size:``` The size of the time window being considered to compute the average translation time. Must be an integer $>=1$.

**Example:**
```
python -m unbabel_cli --input_file data/events.jsonl --window_size 10
```
And the following are **optional parameters:**
- ```--output_file_location:``` The location of the output file created by the application, including its name and suffix. It must be a .jsonl file. If a directory is stated and it doesn't already exist, the application will create it and dump the output file there. **DEFAULT:** *data/output.jsonl*
- ```--ignore_invalid_line:``` If added to the command line, the application will ignore lines in the input file that raise errors, like lines without json objects or without the necessary keys ('timestamp' and 'duration') and skip them during computation. The default state is to pause the application when we encounter such errors.

**Example including optional parameters:**
```
python -m unbabel_cli --input_file data/events.jsonl --window_size 10 --output_file_location data/output_example.jsonl --ignore_invalid_line
```

## How to Test
With the virtual environment active, from the root directory:
```
pytest tests/ -v
```

Tests are organised by module (`test_utils.py`, `test_event_parser.py`, `test_window.py`) plus an end-to-end test (`test_main.py`).


## Further Reading
`SOLUTION.md` covers the key architecture decisions, including the time boundary convention used by the sliding window and the reasoning behind it.