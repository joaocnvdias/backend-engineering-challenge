import pytest
from event_parser import *
from utils import timestamp_to_unix

@pytest.fixture
def sample_event():
    return {
        "timestamp": "2018-12-26 18:11:08.509654",
        "translation_id": "A",
        "source_language": "en",
        "target_language": "fr",
        "client_name": "airliberty",
        "event_name": "translation_delivered",
        "nr_words": 30,
        "duration": 20
    }

class TestParser:

    def test_load_translation_events_preserves_data_structure(self, tmp_path):
        file = tmp_path / "events.json"

        file.write_text(
            '\n'.join([
                '{"timestamp": "2018-12-26 18:11:08.509654","translation_id": "5aa5b2f39f7254a75aa5","source_language": "en","target_language": "fr","client_name": "airliberty","event_name": "translation_delivered","nr_words": 30, "duration": 20}',
            ])
        )

        events = iter_translation_events(file)

        first = next(events) 
        assert isinstance(first, dict)
        assert first["timestamp"] == "2018-12-26 18:11:08.509654"
        assert first["duration"] == 20
    
    def test_load_translation_events_preserves_order(self, tmp_path):
        file = tmp_path / "events.json"

        file.write_text(
            '\n'.join([
                '{"timestamp": "2018-12-26 18:11:08.509654","translation_id": "5aa5b2f39f7254a75aa5","source_language": "en","target_language": "fr","client_name": "airliberty","event_name": "translation_delivered","nr_words": 30, "duration": 20}',
                '{"timestamp": "2018-12-26 18:15:19.903159","translation_id": "5aa5b2f39f7254a75aa4","source_language": "en","target_language": "fr","client_name": "airliberty","event_name": "translation_delivered","nr_words": 30, "duration": 31}'
            ])
        )

        events = iter_translation_events(file)
        first = next(events) 
        second = next(events)
        assert first["timestamp"] == "2018-12-26 18:11:08.509654"
        assert second["timestamp"] == "2018-12-26 18:15:19.903159"

    def test_unix_transformation_in_filtering(self, sample_event):
        filtered_event = iter_and_filter_events([sample_event])

        event = next(filtered_event)
        assert isinstance(event["timestamp"], float)
        assert event["timestamp"] == 1545847868.509654  # expected unix value

    def test_filtered_keys(self, sample_event):
        filtered_event = iter_and_filter_events([sample_event])        
        wanted_keys = {"timestamp", "duration"}
        event = next(filtered_event)

        assert list(event.keys()) == ["timestamp", "duration"]