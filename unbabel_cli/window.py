from collections import deque

def sliding_window_loop(starting_minute, final_minute, window_size, filtered_events):
    window_size_unix = window_size*60
    current_minute = starting_minute
    sliding_window = deque()
    window_sum = 0
    window_count = 0
    averages_list = []

    while current_minute <= final_minute+60: #ends on the minute after the final event, by design
        while filtered_events and filtered_events[0]["timestamp"]>=current_minute-window_size_unix and filtered_events[0]["timestamp"]<current_minute: #only check first event because they are ordered
            sliding_window.append(filtered_events[0])
            window_sum += filtered_events[0]["duration"]
            window_count += 1
            filtered_events.popleft() #once an event is inside the window, they will not enter it again
        while sliding_window and (sliding_window[0]["timestamp"] < current_minute-window_size_unix or sliding_window[0]["timestamp"] >= current_minute): 
            window_sum -= sliding_window[0]["duration"]
            window_count -= 1
            sliding_window.popleft()
        
        averages_list.append({"date": current_minute, "average_delivery_time": compute_average_delivery_time(window_sum=window_sum, window_count=window_count)})
        current_minute += 60
    return averages_list

def compute_average_delivery_time(window_sum, window_count):
    if window_count != 0:
        return window_sum/window_count
    else:
        return 0