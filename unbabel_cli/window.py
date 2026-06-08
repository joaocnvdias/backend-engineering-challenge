from collections import deque
from utils import floor_to_minutes

def iter_sliding_window_loop(window_size, filtered_events):
    """
    Lazily compute per-minute average delivery times using a sliding window.
    For each minute boundary, the function yields the average delivery duration 
    of all events whose timestamps fall within the previous ``window_size`` minutes. 

    Assumptions:
        - Events are in chronological order
        - An event is inside the window if its timestamp belongs in [current_minute-window_size; current_minute[
    
    Args:
        window_size (int): Size of the sliding window in minutes.
        filtered_events: Iterable of validated and filtered translation events sorted by timestamp.

    Yields:
        dict: A dictionary containing:
            - 'date': Unix timestamp representing the minute boundary.
            - 'average_delivery_time': Average duration of events within the current sliding window.
    """
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
            yield {                        
                "date": current_minute,
                "average_delivery_time": compute_average_delivery_time(window_sum = window_sum, window_count=window_count)
            }

            current_minute += 60 

            while sliding_window and (sliding_window[0]["timestamp"] < current_minute-window_size_unix): #remove expired events; no need to worry with future condition
                window_sum -= sliding_window[0]["duration"]
                window_count -= 1
                sliding_window.popleft()

        sliding_window.append(event) #event only joins after adding 1 min to current_minute
        window_sum += event["duration"]
        window_count += 1
        last_event_timestamp = event["timestamp"] #remember for final minute

    if last_event_timestamp is not None: #last minute
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