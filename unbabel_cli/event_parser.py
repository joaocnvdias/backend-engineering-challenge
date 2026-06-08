import argparse
import json
from utils import timestamp_to_unix, floor_to_minutes

def parse_from_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", type=str, help="Input file location with translation events")
    parser.add_argument("--window_size", type=int, help="Temporal window size for computing average delivery time")
    return parser.parse_args()

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

def get_boundary_timestamps(events_list: list) -> tuple:
    return floor_to_minutes(events_list[0]["timestamp"]), floor_to_minutes(events_list[-1]["timestamp"]) 