from parser import parse_from_cli, load_translation_events

def main():
    args = parse_from_cli()
    translation_events = load_translation_events(file_location=args.input_file)
    print(translation_events)
if __name__ == "__main__":
    main()


