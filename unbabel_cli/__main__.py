from event_parser import parse_from_cli, validate_args, iter_translation_events, validate_input_lines, iter_and_filter_events
from window import iter_sliding_window_loop
from utils import save_results_to_file

def main():

    args = parse_from_cli()
    validate_args(args)
    translation_events = iter_translation_events(file_location=args.input_file)
    validate_input_lines(translation_events)
    filtered_events = iter_and_filter_events(events=translation_events)
    averages = iter_sliding_window_loop(window_size= args.window_size, filtered_events=filtered_events)
    save_results_to_file(output_path=args.output_file_location, results= averages)

if __name__ == "__main__":
    main()