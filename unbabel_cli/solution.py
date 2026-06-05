from collections import deque

def sliding_window_loop(starting_minute, final_minute, window_size, filtered_events):
    window_size_unix = window_size*60
    current = starting_minute
    sliding_window = deque()

    while current <= final_minute+60: #ends on the minute after the final event, by design
        while filtered_events and filtered_events[0]["timestamp"]>=current-window_size_unix and filtered_events[0]["timestamp"]<current: #only check first event because they are ordered
            sliding_window.append(filtered_events[0])
            filtered_events.popleft() #once an event is inside the window, they will not enter it again
        while sliding_window and (sliding_window[0]["timestamp"] < current-window_size_unix or sliding_window[0]["timestamp"] >= current): 
            sliding_window.popleft()
        current += 60
  