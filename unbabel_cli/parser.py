import argparse
import json

def parse_from_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", type=str, help="Input file location with translation events")
    parser.add_argument("--window_size", type=int, help="Temporal window size for computing average delivery time")
    return parser.parse_args()

def load_translation_events(file_location):
    translation_events = []

    with open(file_location, "r", encoding="utf-8") as f:
        for line in f:
            event = json.loads(line)
            translation_events.append(event) #keeps order
            
    return translation_events