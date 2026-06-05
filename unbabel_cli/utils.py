import datetime
import json

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

def save_results_to_file(file_name, results_list):
    for results_dict in results_list:
        results_dict["date"] = unix_to_timestamp(unix = results_dict["date"], output= True)
    
    file_location = "data/" + file_name + ".jsonl"
    with open(file_location, 'w') as f:
        for time_average in results_list:
            json.dump(time_average, f)
            if time_average != results_list[-1]:
                f.write('\n') #keep requested output structure