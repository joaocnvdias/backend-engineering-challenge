import pytest
from collections import deque
from window import *
from event_parser import get_boundary_timestamps

@pytest.fixture
def filtered_events():
    events =[
        {'timestamp': 1545847868.509654, 'duration': 20}, 
        {'timestamp': 1545848119.903159, 'duration': 31}, 
        {'timestamp': 1545848599.903159, 'duration': 54}
        ]
    return iter(events)

@pytest.fixture
def exact_minutes_events():
    events = [
        {'timestamp': 1545847860.0, 'duration': 20},
        {'timestamp': 1545848100.0, 'duration': 31}, 
        {'timestamp': 1545848580.0, 'duration': 54}
        ]
    return iter(events)

@pytest.fixture
def expected_loop_output():
    return [
        {'date': 1545847860.0, 'average_delivery_time': 0}, 
        {'date': 1545847920.0, 'average_delivery_time': 20}, 
        {'date': 1545847980.0, 'average_delivery_time': 20}, 
        {'date': 1545848040.0, 'average_delivery_time': 20}, 
        {'date': 1545848100.0, 'average_delivery_time': 20}, 
        {'date': 1545848160.0, 'average_delivery_time': 25.5}, 
        {'date': 1545848220.0, 'average_delivery_time': 25.5}, 
        {'date': 1545848280.0, 'average_delivery_time': 25.5}, 
        {'date': 1545848340.0, 'average_delivery_time': 25.5}, 
        {'date': 1545848400.0, 'average_delivery_time': 25.5}, 
        {'date': 1545848460.0, 'average_delivery_time': 25.5}, 
        {'date': 1545848520.0, 'average_delivery_time': 31}, 
        {'date': 1545848580.0, 'average_delivery_time': 31}, 
        {'date': 1545848640.0, 'average_delivery_time': 42.5}
    ]
    
class TestWindow:

    def test_average(self):
        assert compute_average_delivery_time(window_sum=100, window_count=4) == 25.0

    def test_average_zero_count_returns_zero(self):
        """An empty window must return 0, not raise ZeroDivisionError."""
        assert compute_average_delivery_time(window_sum=0, window_count=0) == 0

    def test_output_rows_have_correct_keys(self, filtered_events):
        window_size = 10
        result = iter_sliding_window_loop(window_size, filtered_events)
        event = next(result)
        assert set(event.keys()) == {"date", "average_delivery_time"}

    def test_window_loop_length(self, filtered_events, expected_loop_output):
        """
        Output must cover every minute from starting_minute to final_minute+1 minute.
        """
        window_size = 10
        result = list(iter_sliding_window_loop(window_size, filtered_events))  #drain generator
        assert len(result) == len(expected_loop_output) 

    def test_loop_example_result(self, filtered_events, expected_loop_output):
        window_size = 10
        result = list(iter_sliding_window_loop(window_size, filtered_events))
        assert result == expected_loop_output
 
    def test_loop_exact_minutes_result(self, exact_minutes_events, expected_loop_output):
        """
        In this solution, exact minutes should not count for that minute.
        Example: Input: "timestamp": "2018-12-26 18:23:00.000000" belongs in Output: "date": "2018-12-26 18:13:00" but not in "2018-12-26 18:23:00"
        """
        window_size = 10
        result = list(iter_sliding_window_loop(window_size, exact_minutes_events))

        assert result == expected_loop_output

    def test_event_expires_after_window(self, filtered_events):
        """
        With window_size=1, an event at minute M must not appear at minute M+2.
        """
        window_size = 1
        result = iter_sliding_window_loop(window_size, filtered_events)
        i0 = next(result)
        i1 = next(result)
        i2 = next(result)
        #i0: 18:11 (0), i1: 18:12 (20), i2: 18:13 expired - 0      
        assert i0["average_delivery_time"] == 0 
        assert i1["average_delivery_time"] == 20
        assert i2["average_delivery_time"] == 0 