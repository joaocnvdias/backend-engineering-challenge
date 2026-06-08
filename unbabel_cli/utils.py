import datetime
import json
import os

def timestamp_to_unix(timestamp: str) -> float:
    """
    Convert a timestamp string to a Unix timestamp.
    The input timestamp is assumed to be in UTC and must follow the
    format ``YYYY-MM-DD HH:MM:SS.ffffff``, where ``ffffff`` represents
    microseconds.

    Args:
        timestamp (str): Timestamp string to convert.

    Returns:
        float: Unix timestamp representing the number of seconds since the Unix epoch (1970-01-01 00:00:00 UTC).
    """
    dt = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f") #%f represents microseconds
    return dt.replace(tzinfo=datetime.timezone.utc).timestamp() #assuming utc timezone to assure consistency in results between different machines

def unix_to_timestamp(unix: float, output = False) -> str:
    """
    Convert a Unix timestamp to a formatted UTC timestamp string.

    Args:
        unix (float): Unix timestamp in seconds since the Unix epoch.
        output (bool): If True, return the timestamp without microseconds.
                        If False, include microseconds in the output.

    Returns:
        str: Timestamp formatted without microseconds if output is True 
        and with microseconds if output is False.
    """
    dt = datetime.datetime.fromtimestamp(unix, tz=datetime.timezone.utc)
    if output: 
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    return dt.strftime("%Y-%m-%d %H:%M:%S.%f")

def floor_to_minutes(unix: float) -> float:
    """
    Round a Unix timestamp down to the start of its minute.
    """
    return int(unix) // 60 * 60   #do floor division to obtain last "whole" minute and then back to a valid unix value

def save_results_to_file(output_path: str, results):  

    dir_name = os.path.dirname(output_path)
    if dir_name: #if no dir is provided in args, just create file in root
        os.makedirs(dir_name, exist_ok=True)

    with open(output_path, 'w') as f:
        for result in results:
            result["date"] = unix_to_timestamp(unix=result["date"], output=True)
            f.write(json.dumps(result) + "\n")