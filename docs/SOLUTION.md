## Problem Definition

This project is focused on building a command line interface that parses a stream of events and produces, for every minute, the moving average of the translation delivery time for the last X minutes, where X is defined by the user. 

This program receives as an input a JSONL file where it's assumed that the events are ordered by timestamp ascending. The input file has the following structure: 

```
{"timestamp": "2018-12-26 18:11:08.509654","translation_id": "5aa5b2f39f7254a75aa5","source_language": "en","target_language": "fr","client_name": "airliberty","event_name": "translation_delivered","nr_words": 30, "duration": 20}
{"timestamp": "2018-12-26 18:15:19.903159","translation_id": "5aa5b2f39f7254a75aa4","source_language": "en","target_language": "fr","client_name": "airliberty","event_name": "translation_delivered","nr_words": 30, "duration": 31}
{"timestamp": "2018-12-26 18:23:19.903159","translation_id": "5aa5b2f39f7254a75bb3","source_language": "en","target_language": "fr","client_name": "taxi-eats","event_name": "translation_delivered","nr_words": 100, "duration": 54}
```

And outputs a JSONL file with the ```average\_delivery\_time``` for each minute, starting at the minute of the first event and **ending in the minute after the last event**. This results in the following format:

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
## Proposed Solution 

### Time Domain Definiton
Firstly, we must note that, for each timestamp present in the output, we must consider all of the events that belong in the time domain of $\text{current\_minute} - X \space \text{to} \space \text{current\_minute}$, where $X$ is the window size defined by the user in the application call. 

We must define if the outer limits of this interval are inclusive or not. This is important for the cases where the translation events are recorded at a timestamp that falls exactly on a minute boundary, that is with no seconds or milliseconds. In such cases, whether that event belongs to the current window or the next is determined solely by the boundary convention, which can produce different outputs.

**Decision:** The time domain adopted in this solution is ```[current_minute - X; current_minute[```. The project specification does not contain an example that unambiguously distinguishes between conventions, as no event in the sample data falls on an exact minute boundary. Therefore we adopt this convention because it better aligned with the input/output example provided in the project description. Take the following input example:

```
{"timestamp": "2018-12-26 18:11:00.000000","translation_id": "5aa5b2f39f7254a75aa5","source_language": "en","target_language": "fr","client_name": "airliberty","event_name": "translation_delivered","nr_words": 30, "duration": 20}
{"timestamp": "2018-12-26 18:15:00.000000","translation_id": "5aa5b2f39f7254a75aa4","source_language": "en","target_language": "fr","client_name": "airliberty","event_name": "translation_delivered","nr_words": 30, "duration": 31}
{"timestamp": "2018-12-26 18:23:00.000000","translation_id": "5aa5b2f39f7254a75bb3","source_language": "en","target_language": "fr","client_name": "taxi-eats","event_name": "translation_delivered","nr_words": 100, "duration": 54}
```
- With ```[current_minute - X; current_minute[```, an event at exactly `18:11:00` falls outside the first window `[18:01, 18:11[`, producing an average of 0, which is consistent with the example provided by the project design team. Furthermore, for the last entry in the output, the same could be said, as long as the last timestamp is the minute after the last translation event. 

**NOTE:** Had we adopted ```]current_minute - X; current_minute]```, the first event would fall inside the first window `]18:01, 18:11]`, therefore being included in the average of `18:11:00`. 

### Average Delivery Time Calculation

For the solution of this project, we decided to opt for sliding window solution, where for each interval of ```[current_minute - X; current_minute[``` we check which translation events were active in this window and compute their average duration.

To efficiently track which events belong to the current window, this solution uses a double ended queue from Python's `collections` module, a **deque**. This is more efficient than using a normal list because, since the events are ordered in time, we always want to operate in a FIFO way. Popping the first element of a list has a time complexity of O(n), while popping the left element of a deque has a time complexity of O(1), since it has pointers to both the first and last element in the queue.

At each minute tick, events are appended to the right of the deque as they are processed. Events that have fallen outside the window, that is, whose timestamps are older than `current_minute - window_size` are evicted from the left (due to them being ordered in the file).

To further improve performance, we use two accumulators `window_sum` and `window_count` to compute the average delivery time. When an event enters the window, its duration is added to `window_sum` and `window_count` is incremented and when an event is evicted, its duration is subtracted and `window_count` is decremented. The average at any minute is then just `window_sum / window_count`, making each tick O(1), which is way better than having to iterate through the sliding window at each minute to compute the sum (O(n)).

#### Memory Efficiency: Generator Pipeline

Rather than loading the entire input file into memory, the application processes events one at a time through a **generator pipeline**. This makes sure that we have a memory complexity of O(1) regarding the events being loaded, and the biggest strain in memory will be the active events in the sliding window.

Considering these time and memory efficient techniques, this application is ready to work with the provided trivial example, but also has the ability to scale to bigger files. 