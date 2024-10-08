# Timetable to iCal Converter

This Python script converts timetable data from multiple CSV files into a single iCal format file.

## Installation

1. Clone the repository from GitHub:

```bash
git clone https://github.com/WillBarouch/Timetable.git
```

2. Navigate into the cloned repository:

```bash
cd Timetable
```

3. Install the required Python packages. This project requires `icalendar`, `argparse`, `csv`, `json`, and `os`. You can install these using pip:

```bash
pip install icalendar argparse
```

## Usage

The script takes three command line arguments:

- `-o` or `--output`: The output iCal file. This is where the resulting iCal file will be saved.
- `-s` or `--start`: The start date in YYYY-MM-DD format. This is the date of the first day of the first week of your timetable.
- `-e` or `--end`: The end date in YYYY-MM-DD format. This is the date of the last day of your timetable.

Here's an example of how to run the script:

```bash
python main.py -o schedule.ics -s 2024-10-07 -e 2024-12-09
```

This will process `week1.csv` and `week2.csv`, convert them to iCal format, and save the output in the `schedule.ics` file. The start date for the schedule is set to October 7, 2024, and the end date is set to December 9, 2024.

The script now combines all the events from the CSV files into a single iCalendar object before writing it to the output file.

Also included in the repository is `prompt.txt`, which contains a sample LLM prompt that can be used to convert a PDF timetable to CSV format.

## License

[MIT](https://choosealicense.com/licenses/mit/)