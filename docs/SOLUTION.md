## Problem Definition

This project is focused on building a command line interface that parses a stream of events and produces, for every minute, the moving average of the translation delivery time for the last X minutes, where X is defined by the user. 

This program receives as an input a JSONL file where it's assumed that the events are ordered by timestamp ascending. The input file has the following structure: 

```
{"timestamp": "2018-12-26 18:11:08.509654","translation_id": "5aa5b2f39f7254a75aa5","source_language": "en","target_language": "fr","client_name": "airliberty","event_name": "translation_delivered","nr_words": 30, "duration": 20}
{"timestamp": "2018-12-26 18:15:19.903159","translation_id": "5aa5b2f39f7254a75aa4","source_language": "en","target_language": "fr","client_name": "airliberty","event_name": "translation_delivered","nr_words": 30, "duration": 31}
{"timestamp": "2018-12-26 18:23:19.903159","translation_id": "5aa5b2f39f7254a75bb3","source_language": "en","target_language": "fr","client_name": "taxi-eats","event_name": "translation_delivered","nr_words": 100, "duration": 54}
```

And outputs a JSONL file with the $\text{average\_delivery\_time}$ for each minute, starting at the minute of the first event and **ending in the minute after the last event**. This results in the following format:

```
{"date": "2018-12-26 18:11:00", "average_delivery_time": 0}
{"date": "2018-12-26 18:12:00", "average_delivery_time": 20}
{"date": "2018-12-26 18:13:00", "average_delivery_time": 20}
{"date": "2018-12-26 18:14:00", "average_delivery_time": 20}
{"date": "2018-12-26 18:15:00", "average_delivery_time": 20}
{"date": "2018-12-26 18:16:00", "average_delivery_time": 25.5}
{"date": "2018-12-26 18:17:00", "average_delivery_time": 25.5}
{"date": "2018-12-26 18:18:00", "average_delivery_time": 25.5}
{"date": "2018-12-26 18:19:00", "average_delivery_time": 25.5}
{"date": "2018-12-26 18:20:00", "average_delivery_time": 25.5}
{"date": "2018-12-26 18:21:00", "average_delivery_time": 25.5}
{"date": "2018-12-26 18:22:00", "average_delivery_time": 31}
{"date": "2018-12-26 18:23:00", "average_delivery_time": 31}
{"date": "2018-12-26 18:24:00", "average_delivery_time": 42.5}
```

The application call looks like this:

```
unbabel_cli --input_file events.json --window_size 10
```

## Proposed Solution 

### Time Domain Definiton
Firstly, we must note that, for each timestamp present in the output, we must consider all of the events that belong in the time domain of $\text{current\_minute} - X \space \text{to} \space \text{current\_minute}$, where $X$ is the window size defined by the user in the application call. 

We must define if the outer limits of this interval are inclusive or not. This is important for the cases where the translation events are recorded at a timestamp that falls exactly on a minute boundary, that is with no seconds or milliseconds. In such cases, whether that event belongs to the current window or the next is determined solely by the boundary convention, which can produce different outputs.

**Decision:** The time domain adopted in this solution is $[\text{current\_minute} - X; \text{current\_minute}[$. The project specification does not contain an example that unambiguously distinguishes between conventions, as no event in the sample data falls on an exact minute boundary. Therefore we adopt this convention because it better aligned with the input/output example provided in the project description. Take the following input example:

```
{"timestamp": "2018-12-26 18:11:00.000000","translation_id": "5aa5b2f39f7254a75aa5","source_language": "en","target_language": "fr","client_name": "airliberty","event_name": "translation_delivered","nr_words": 30, "duration": 20}
{"timestamp": "2018-12-26 18:15:00.000000","translation_id": "5aa5b2f39f7254a75aa4","source_language": "en","target_language": "fr","client_name": "airliberty","event_name": "translation_delivered","nr_words": 30, "duration": 31}
{"timestamp": "2018-12-26 18:23:00.000000","translation_id": "5aa5b2f39f7254a75bb3","source_language": "en","target_language": "fr","client_name": "taxi-eats","event_name": "translation_delivered","nr_words": 100, "duration": 54}
```
- With $[\text{current\_minute} - X;\text{current\_minute}[$, an event at exactly `18:11:00` falls outside the first window `[18:01, 18:11[`, producing an average of 0, which is consistent with the example provided by the project design team. Furthermore, for the last entry in the output, the same could be said, as long as the last timestamp is the minute after the last translation event. 

**NOTE:** Had we adopted $]\text{current\_minute} - X;\text{current\_minute}]$, the first event would fall inside the first window `]18:01, 18:11]`, therefore being included in the average of `18:11:00`. 

### Average Delivery Time Calculation