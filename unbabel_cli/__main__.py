from parser import parse_from_cli, load_translation_events, filter_events_list
from window import sliding_window_loop
from utils import unix_to_timestamp
import json

def main():

    args = parse_from_cli()
    translation_events = load_translation_events(file_location=args.input_file)
    filtered_events, starting_minute, final_minute = filter_events_list(events_list=translation_events)
    averages_list = sliding_window_loop(starting_minute=starting_minute, final_minute=final_minute, window_size= args.window_size, filtered_events=filtered_events)
    
    for item in averages_list:
        item["date"] = unix_to_timestamp(unix = item["date"], output= True)
        
    with open('data/output.jsonl', 'w') as outfile:
        for entry in averages_list:
            json.dump(entry, outfile)
            if entry != averages_list[-1]:
                outfile.write('\n') #keep requested output structure

if __name__ == "__main__":
    main()


