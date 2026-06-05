import argparse
import json
from collections import deque
from utils import timestamp_to_unix, floor_to_minutes

def parse_from_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", type=str, help="Input file location with translation events")
    parser.add_argument("--window_size", type=int, help="Temporal window size for computing average delivery time")
    return parser.parse_args()

def load_translation_events(file_location: str) -> list:
    translation_events = []

    with open(file_location, "r", encoding="utf-8") as f:
        for line in f:
            event = json.loads(line)
            translation_events.append(event) #keeps order

    return translation_events

def filter_events_list(events_list: list) -> list:
    wanted_keys = ["timestamp", "duration"]
    filtered_events_list = deque({key: event_dict[key] for key in wanted_keys} for event_dict in events_list)

    for event_dict in filtered_events_list:
        event_dict["timestamp"] = timestamp_to_unix(event_dict["timestamp"])

    return filtered_events_list, floor_to_minutes(filtered_events_list[0]["timestamp"]), floor_to_minutes(filtered_events_list[-1]["timestamp"]) 