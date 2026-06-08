from collections import deque
from utils import floor_to_minutes, unix_to_timestamp

def iter_sliding_window_loop(window_size, filtered_events):
    window_size_unix = window_size * 60 #we work with seconds
    current_minute = None
    sliding_window = deque()
    window_sum = 0
    window_count = 0
    last_event_timestamp = None

    for event in filtered_events: #from generator
        if current_minute is None: 
            current_minute = floor_to_minutes(event["timestamp"])

        while current_minute <= event["timestamp"]: 
            print(f"Event: {event}, minute: {unix_to_timestamp(current_minute)}, average: {compute_average_delivery_time(window_sum = window_sum, window_count=window_count)}")
            yield {                        
                "date": current_minute,
                "average_delivery_time": compute_average_delivery_time(window_sum = window_sum, window_count=window_count)
            }

            current_minute += 60 #event joins in the next minute

            while sliding_window and (sliding_window[0]["timestamp"] < current_minute-window_size_unix): #remove expired events; no need to worry with future condition
                window_sum -= sliding_window[0]["duration"]
                window_count -= 1
                sliding_window.popleft()

        sliding_window.append(event)
        window_sum += event["duration"]
        window_count += 1
        last_event_timestamp = event["timestamp"] #remember for final event

    if last_event_timestamp is not None:
        next_minute = floor_to_minutes(last_event_timestamp) + 60

        yield {
            "date": next_minute,
            "average_delivery_time": compute_average_delivery_time(window_sum=window_sum, window_count=window_count)
        }

def compute_average_delivery_time(window_sum: int, window_count: int) -> float:
    if window_count != 0:
        return window_sum/window_count
    else:
        return 0