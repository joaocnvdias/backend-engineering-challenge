import pytest
from unittest.mock import patch
from event_parser import *

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

class TestCLIRaisesError:

    def test_negative_and_zero_window_size(self):
        """--window_size <= 0 should raise ValueError"""
        with patch("sys.argv", ["unbabel_cli", "--input_file", "events.jsonl", "--window_size", "-1"]):
            args = parse_from_cli()
            with pytest.raises(ValueError, match="window_size must be >= 1"):
                validate_args(args)

        with patch("sys.argv", ["unbabel_cli", "--input_file", "events.jsonl", "--window_size", "0"]):
            args = parse_from_cli()
            with pytest.raises(ValueError, match="window_size must be >= 1"):
                validate_args(args)
    
    def test_missing_input_file(self):
        """--input_file pointing to nonexistent file should raise FileNotFoundError"""
        with patch("sys.argv", ["unbabel_cli", "--input_file", "not_a_file_100_percent.jsonl", "--window_size", "10"]):
            args = parse_from_cli()
            with pytest.raises(FileNotFoundError, match= "Input file not found"):
                validate_args(args)

    def test_empty_input_file(self, tmp_path):
        """an empty file should raise a ValueError"""
        empty_file = tmp_path / "empty.jsonl"
        empty_file.write_text("")
        with patch("sys.argv", ["unbabel_cli", "--input_file", str(empty_file), "--window_size", "10"]):
            args = parse_from_cli()
            with pytest.raises(ValueError, match="Input file is empty"):
                validate_args(args)

    def test_empty_jsonl_file(self, tmp_path):
        """a file with only blank lines shouldbe treated as empty"""
        blank_file = tmp_path / "blank.jsonl"
        blank_file.write_text("\n\n\n")
        with patch("sys.argv", ["unbabel_cli", "--input_file", str(blank_file), "--window_size", "10"]):
            args = parse_from_cli()
            with pytest.raises(ValueError, match="Input file is empty"):
                validate_args(args)

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
        wanted_keys = ["timestamp", "duration"]
        event = next(filtered_event)

        assert list(event.keys()) == wanted_keys
    
    def test_input_file_invalid_format(self,tmp_path):
        invalid_events = [
            '{"timestamp": "2018-12-26 18:11:08.509654", "translation_id": "5aa5b2f39f7254a75aa5", "source_language": "en", "target_language": "fr", "client_name": "airliberty", "event_name": "translation_delivered", "nr_words": 30, "duration": 20}',
            '2',
            '{"timestamp": "2018-12-26 18:23:19.903159", "translation_id": "5aa5b2f39f7254a75bb3", "source_language": "en", "target_language": "fr", "client_name": "taxi-eats", "event_name": "translation_delivered", "nr_words": 100, "duration": 54}',
        ]
        file = tmp_path / "events.jsonl"
        file.write_text("\n".join(invalid_events))
        events = iter_translation_events(file)

        with pytest.raises(TypeError, match = "File includes invalid line, expected a JSON object"):
            list(iter_validate_input_lines(events = events, ignore_invalid= False))
    
    def test_input_file_invalid_key_timestamp(self,tmp_path):
        invalid_events = [
            '{"translation_id": "5aa5b2f39f7254a75aa5", "source_language": "en", "target_language": "fr", "client_name": "airliberty", "event_name": "translation_delivered", "nr_words": 30, "duration": 20}',
            '{"duration": 35}'
        ]
        file = tmp_path / "events.jsonl"
        file.write_text("\n".join(invalid_events))
        events = iter_translation_events(file)

        with pytest.raises(KeyError, match = "File includes a line with a JSON object without the 'timestamp' key"):
            list(iter_validate_input_lines(events = events, ignore_invalid= False))
    
    def test_input_file_invalid_key_duration(self,tmp_path):
        invalid_events = [
            '{"timestamp": "2018-12-26 18:11:08.509654", "translation_id": "5aa5b2f39f7254a75aa5", "source_language": "en", "target_language": "fr", "client_name": "airliberty", "event_name": "translation_delivered", "nr_words": 30}',
            '{"timestamp": "2018-12-26 18:23:19.903159", "translation_id": "5aa5b2f39f7254a75bb3", "source_language": "en", "target_language": "fr", "client_name": "taxi-eats", "event_name": "translation_delivered", "nr_words": 100}'
        ]
        file = tmp_path / "events.jsonl"
        file.write_text("\n".join(invalid_events))
        events = iter_translation_events(file)

        with pytest.raises(KeyError, match = "File includes a line with a JSON object without the 'duration' key"):
            list(iter_validate_input_lines(events = events, ignore_invalid= False))