import pytest
import json
from utils import *
from window import * 
from event_parser import * 

@pytest.fixture
def readme_events_file(tmp_path):
    events = [
        '{"timestamp": "2018-12-26 18:11:08.509654", "translation_id": "5aa5b2f39f7254a75aa5", "source_language": "en", "target_language": "fr", "client_name": "airliberty", "event_name": "translation_delivered", "nr_words": 30, "duration": 20}',
        '{"timestamp": "2018-12-26 18:15:19.903159", "translation_id": "5aa5b2f39f7254a75aa4", "source_language": "en", "target_language": "fr", "client_name": "airliberty", "event_name": "translation_delivered", "nr_words": 30, "duration": 31}',
        '{"timestamp": "2018-12-26 18:23:19.903159", "translation_id": "5aa5b2f39f7254a75bb3", "source_language": "en", "target_language": "fr", "client_name": "taxi-eats", "event_name": "translation_delivered", "nr_words": 100, "duration": 54}',
    ]
    file = tmp_path / "events.jsonl"
    file.write_text("\n".join(events))
    return str(file)
 

class TestMain:
    """
    Reproduces the README's expected output for window_size=10 with three events.
    """
 
    README_EXPECTED = [
        {"date": "2018-12-26 18:11:00", "average_delivery_time": 0},
        {"date": "2018-12-26 18:12:00", "average_delivery_time": 20},
        {"date": "2018-12-26 18:13:00", "average_delivery_time": 20},
        {"date": "2018-12-26 18:14:00", "average_delivery_time": 20},
        {"date": "2018-12-26 18:15:00", "average_delivery_time": 20},
        {"date": "2018-12-26 18:16:00", "average_delivery_time": 25.5},
        {"date": "2018-12-26 18:17:00", "average_delivery_time": 25.5},
        {"date": "2018-12-26 18:18:00", "average_delivery_time": 25.5},
        {"date": "2018-12-26 18:19:00", "average_delivery_time": 25.5},
        {"date": "2018-12-26 18:20:00", "average_delivery_time": 25.5},
        {"date": "2018-12-26 18:21:00", "average_delivery_time": 25.5},
        {"date": "2018-12-26 18:22:00", "average_delivery_time": 31},
        {"date": "2018-12-26 18:23:00", "average_delivery_time": 31},
        {"date": "2018-12-26 18:24:00", "average_delivery_time": 42.5}
    ]
 
    def test_readme_example_output_len(self, readme_events_file):
        window_size = 10
        filtered = iter_and_filter_events(iter_translation_events(readme_events_file))
        result = list(iter_sliding_window_loop(window_size, filtered))
        assert len(result) == len(self.README_EXPECTED)

    def test_readme_example_averages(self, tmp_path, readme_events_file):
        """Every average must exactly match the README's expected output."""
        window_size = 10
        output_path = tmp_path / "output.jsonl"

        filtered = iter_and_filter_events(iter_translation_events(readme_events_file))
        results = list(iter_sliding_window_loop(window_size, filtered))
        save_results_to_file(str(output_path), results)

        written_lines = output_path.read_text().strip().split("\n")
        result = [json.loads(line) for line in written_lines]

        assert result == self.README_EXPECTED