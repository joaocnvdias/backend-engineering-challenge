import datetime

def timestamp_to_unix(timestamp: str) -> float:
    dt = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f") #%f represents microseconds
    return dt.replace(tzinfo=datetime.timezone.utc).timestamp() #assuming utc timezone to assure consistency in results between different machines

def unix_to_timestamp(unix: float, output = False) -> str:
    dt = datetime.datetime.fromtimestamp(unix, tz=datetime.timezone.utc)
    if output: 
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    return dt.strftime("%Y-%m-%d %H:%M:%S.%f")

def floor_to_minutes(unix: float) -> float:
    return int(unix) // 60 * 60   #do floor division to obtain last "whole" minute and then back to a valid unix value