import argparse
import json
import os
from utils import timestamp_to_unix

def parse_from_cli() -> list:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", required = True, type=str, help="Input file location with translation events")
    parser.add_argument("--window_size", required = True, type=int, help="Temporal window size for computing average delivery time")

    parser.add_argument("--output_file_location", required= False, type=str, default="data/output1.jsonl" ,help = "Desired output file location and name, including file suffix (use .jsonl)")
    parser.add_argument("--ignore_invalid_line", required=False, action="store_true", help = "When passed, this flag makes the program ignore invalid lines in the input file instead of stopping at an error")
    return parser.parse_args()

def validate_args(args: list):
    if args.window_size <= 0:
        raise ValueError("window_size must be >= 1")

    if not os.path.exists(args.input_file):
        raise FileNotFoundError("Input file not found")
    
    with open(args.input_file, "r") as f: 
        if not any(line.strip() for line in f): #file is empty or only has newline chars
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