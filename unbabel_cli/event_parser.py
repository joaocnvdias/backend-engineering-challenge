import argparse
import json
import os
from utils import timestamp_to_unix

def parse_from_cli() -> list:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", type=str, help="Input file location with translation events")
    parser.add_argument("--window_size", type=int, help="Temporal window size for computing average delivery time")
    return parser.parse_args()

def validate_args(args: list):
    if args.window_size <= 0:
        raise ValueError("window_size must be >= 1")

    if not os.path.exists(args.input_file):
        raise FileNotFoundError("Input file not found")
    
    with open(args.input_file, "r") as f:
        if not any(line.strip() for line in f):
            raise ValueError("Input file is empty")

def iter_translation_events(file_location: str):

    with open(file_location, "r", encoding="utf-8") as f:
        for line in f:
            yield json.loads(line) #load event 1 by 1 

def iter_and_filter_events(events: list):

    for event in events: 
        yield {
            "timestamp": timestamp_to_unix(event["timestamp"]),
            "duration": event["duration"]
        }