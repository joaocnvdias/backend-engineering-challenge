from parser import parse_from_cli, load_translation_events
import datetime
from collections import deque

def clean_data(events_list: list) -> list:
    wanted_keys = ["timestamp", "duration"]
    filtered_events_list = deque({key: event_dict[key] for key in wanted_keys} for event_dict in events_list)

    for event_dict in filtered_events_list:
        event_dict["timestamp"] = timestamp_to_unix(event_dict["timestamp"])

    return filtered_events_list

def timestamp_to_unix(timestamp: str) -> float:
    dt = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f") #%f represents microseconds
    return dt.replace(tzinfo=datetime.timezone.utc).timestamp() #assuming utc timezone to assure consistency in results between different machines

def unix_to_timestamp(unix: float) -> str:
    dt = datetime.datetime.fromtimestamp(unix, tz=datetime.timezone.utc)
    return dt.strftime("%Y-%m-%d %H:%M:%S.%f")

def floor_to_minutes(unix: float) -> float:
    return int(unix) // 60 * 60   #do floor division to obtain last "whole" minute and then back to a valid unix value

def main():
    args = parse_from_cli()
    translation_events = load_translation_events(file_location=args.input_file)
    filtered_events = clean_data(events_list=translation_events)
    first_min = floor_to_minutes(filtered_events[0]["timestamp"])
    last_min = floor_to_minutes(filtered_events[-1]["timestamp"]) + 60
    window_size_unix = args.window_size*60


    current = first_min
    sliding_window = deque()
    while current <= last_min:
        for event in list(filtered_events): #cant iterate over deque if we change it mid loop
            if event["timestamp"]>=current-window_size_unix and event["timestamp"]<current:
                sliding_window.append(event)
                filtered_events.popleft()
            else: 
                break #since elements are ordered, if one is outside of the window the following should to 

        for event in list(sliding_window): 
            if event["timestamp"] < current-window_size_unix or event["timestamp"] >= current:
                sliding_window.popleft()
            else:
                break #if an event is inside the window, then the rest will also be 
        current += 60
  


if __name__ == "__main__":
    main()


