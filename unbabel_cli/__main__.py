import argparse
import json

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", type=str, help="Input file location with translation events")
    parser.add_argument("--window_size", type=int, help="Temporal window size for computing average delivery time")
    args = parser.parse_args()

    input_file_name= args.input_file
    window_size = args.window_size
    translation_events = []

    with open(input_file_name, "r", encoding="utf-8") as f:
        for line in f:
            event = json.loads(line)
            translation_events.append(event) #keeps order

if __name__ == "__main__":
    main()


