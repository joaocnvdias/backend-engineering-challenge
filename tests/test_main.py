import pytest
from collections import deque
from utils import *
from window import * 
from event_parser import * 

@pytest.fixture
def readme_events():
    return deque(
        [
            {
                "timestamp": "2018-12-26 18:11:08.509654",
                "translation_id": "5aa5b2f39f7254a75aa5",
                "source_language": "en", "target_language": "fr",
                "client_name": "airliberty", "event_name": "translation_delivered",
                "nr_words": 30, "duration": 20,
            },
            {
                "timestamp": "2018-12-26 18:15:19.903159",
                "translation_id": "5aa5b2f39f7254a75aa4",
                "source_language": "en", "target_language": "fr",
                "client_name": "airliberty", "event_name": "translation_delivered",
                "nr_words": 30, "duration": 31,
            },
            {
                "timestamp": "2018-12-26 18:23:19.903159",
                "translation_id": "5aa5b2f39f7254a75bb3",
                "source_language": "en", "target_language": "fr",
                "client_name": "taxi-eats", "event_name": "translation_delivered",
                "nr_words": 100, "duration": 54,
            }
        ]
    )
 

class TestMain:
    """
    Reproduces the README's expected output for window_size=10 with three events.
    """
 
    README_EXPECTED = [
        ("2018-12-26 18:11:00", 0),
        ("2018-12-26 18:12:00", 20),
        ("2018-12-26 18:13:00", 20),
        ("2018-12-26 18:14:00", 20),
        ("2018-12-26 18:15:00", 20),
        ("2018-12-26 18:16:00", 25.5),
        ("2018-12-26 18:17:00", 25.5),
        ("2018-12-26 18:18:00", 25.5),
        ("2018-12-26 18:19:00", 25.5),
        ("2018-12-26 18:20:00", 25.5),
        ("2018-12-26 18:21:00", 25.5),
        ("2018-12-26 18:22:00", 31),
        ("2018-12-26 18:23:00", 31),
        ("2018-12-26 18:24:00", 42.5),
    ]
 
    def test_readme_example_output_len(self, readme_events):
        filtered = filter_events_list(readme_events)
        starting_minute, final_minute = get_boundary_timestamps(events_list=filtered)
        result = sliding_window_loop(starting_minute, final_minute, window_size=10, filtered_events=filtered)
        assert len(result) == len(self.README_EXPECTED)
 
    def test_readme_example_averages(self, readme_events):
        """Every average must exactly match the README's expected output."""
        filtered = filter_events_list(readme_events)
        starting_minute, final_minute = get_boundary_timestamps(events_list=filtered)
        result = sliding_window_loop(starting_minute, final_minute, window_size=10, filtered_events=filtered)
 
        for i, (expected_date, expected_avg) in enumerate(self.README_EXPECTED):
            actual_date = unix_to_timestamp(result[i]["date"], output=True)
            actual_avg  = result[i]["average_delivery_time"]
 
            assert actual_date == expected_date, (
                f"Row {i}: expected date {expected_date}, got {actual_date}"
            )
            assert actual_avg == pytest.approx(expected_avg), (
                f"Row {i} ({expected_date}): expected avg {expected_avg}, got {actual_avg}"
            )