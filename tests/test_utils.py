from utils import * 
import pytest 

@pytest.fixture
def sample_timestamp():
    return "2018-12-26 18:11:08.509654"

class TestUtils:

    @pytest.mark.parametrize(
    "timestamp, expected",
    [
        pytest.param("2018-12-26 18:11:08.000000", "2018-12-26 18:11:00.000000", id="simple_seconds"),
        pytest.param("2018-12-26 18:11:08.509654", "2018-12-26 18:11:00.000000", id="microseconds"),
        pytest.param("2018-12-26 18:11:59.000000", "2018-12-26 18:11:00.000000", id="edge_case_end_minute"),
        pytest.param("2018-12-26 18:11:00.000000", "2018-12-26 18:11:00.000000", id="edge_case_exact_minute"),
    ]
)

    def test_timestamp_flooring(self, timestamp, expected):
        """Check minute flooring using different edge cases"""
        unix = timestamp_to_unix(timestamp)
        floor = floor_to_minutes(unix)
        floored_timestamp = unix_to_timestamp(floor)

        assert floored_timestamp == expected

    def test_timestamp_roundtrip(self, sample_timestamp):
        unix = timestamp_to_unix(sample_timestamp)
        result = unix_to_timestamp(unix)
        assert sample_timestamp == result
 
    def test_unix_to_timestamp_output_format(self, sample_timestamp):
        unix = timestamp_to_unix(sample_timestamp)
        result = unix_to_timestamp(unix, output=True)
        assert result == "2018-12-26 18:11:08" #output should not include microseconds
 
    def test_unix_to_timestamp_full_format(self, sample_timestamp):
        unix = timestamp_to_unix(sample_timestamp)
        result = unix_to_timestamp(unix, output=False)
        assert result == sample_timestamp #should include microseconds
 
    def test_floor_to_minutes_already_on_minute(self):
        unix = timestamp_to_unix("2018-12-26 18:11:00.000000")
        assert floor_to_minutes(unix) == unix #exact minute should 