import argparse
import csv
import json
from datetime import datetime, timedelta
import icalendar
from uuid import uuid4


def csv_to_json(csv_path):
    with open(csv_path, 'r') as file:
        reader = csv.reader(file)

        headers = next(reader)
        days = headers[1:]

        schedule = []
        current_time = None
        current_lesson = None
        current_class = None
        current_teacher = None

        for row in reader:
            if row[0] == 'Time':
                current_time = row[1:]
            elif row[0] == 'Lesson':
                current_lesson = row[1:]
            elif row[0] == 'Class':
                current_class = row[1:]
            elif row[0] == 'Teacher':
                current_teacher = row[1:]
            elif row[0] == 'Location':
                current_location = row[1:]

                # After reading the location, add all the gathered data to schedule
                for i, day in enumerate(days):
                    if current_time[i] and current_lesson[i]:  # Ensure there's a time and a lesson
                        schedule.append({
                            "Time": current_time[i],
                            "Day": day,
                            "Lesson": current_lesson[i],
                            "Class": current_class[i],
                            "Teacher": current_teacher[i],
                            "Location": current_location[i]
                        })

    return schedule


def json_to_ical(json_temp, base_date_temp, end_date_temp):
    global end_time_str, start_time_str
    temp_cal = icalendar.Calendar()

    # Add required PRODID (ProgramID) and VERSION properties to the calendar
    temp_cal.add('prodid', '-//WillBarouch//Timetable//EN')
    temp_cal.add('version', '2.0')

    # Determine if the schedule is for week 2 by checking the filename
    is_week2 = 'week2' in file_path.lower()

    if is_week2:
        base_date_temp += timedelta(weeks=1)  # Offset by one week for week 2

    # Calculate the weekday of the start date (0 is Monday, 1 is Tuesday, ..., 6 is Sunday)
    start_weekday = base_date_temp.weekday()

    day_to_date = {
        'Monday': base_date_temp + timedelta(days=(0 - start_weekday) % 7),
        'Tuesday': base_date_temp + timedelta(days=(1 - start_weekday) % 7),
        'Wednesday': base_date_temp + timedelta(days=(2 - start_weekday) % 7),
        'Thursday': base_date_temp + timedelta(days=(3 - start_weekday) % 7),
        'Friday': base_date_temp + timedelta(days=(4 - start_weekday) % 7)
    }

    for item in json_temp:
        event = icalendar.Event()

        event.add('dtstamp', datetime.now())
        event.add('uid', str(uuid4()))
        event.add('summary', item['Lesson'])

        time_range = item['Time'][1:-1]  # remove the square brackets
        try:
            start_time_str, end_time_str = time_range.split(' - ')
        except ValueError:
            print(f"Invalid time range for {item['Lesson']} on {item['Day']}. Skipping.")
            print(f"Time range: {time_range}")

        start_time = datetime.strptime(start_time_str, '%H:%M').time()
        end_time = datetime.strptime(end_time_str, '%H:%M').time()

        date = day_to_date[item['Day']]

        start_datetime = datetime.combine(date, start_time)
        end_datetime = datetime.combine(date, end_time)

        # Ignore all lessons in week 1 prior to start date
        if start_datetime < base_date_temp:
            continue

        event.add('dtstart', start_datetime)
        event.add('dtend', end_datetime)
        event.add('location', item['Location'])

        event.add('rrule', {'freq': 'weekly', 'interval': 2, 'until': end_date_temp})

        temp_cal.add_component(event)

    return temp_cal


parser = argparse.ArgumentParser(description='Process CSV files and convert them to iCal format.')

# Add arguments to the parser
input_files = ['week1.csv', 'week2.csv']
parser.add_argument('-o', '--output', required=True, help='Output iCal file.')
parser.add_argument('-s', '--start', required=True, help='Start date in YYYY-MM-DD format.')
parser.add_argument('-e', '--end', required=True, help='End date in YYYY-MM-DD format.')

# Parse the command line arguments
args = parser.parse_args()

# Convert the start date to a datetime object
start_date = datetime.strptime(args.start, '%Y-%m-%d')
end_date = datetime.strptime(args.end, '%Y-%m-%d')

# Create a Calendar object
cal = icalendar.Calendar()

for file_path in input_files:
    # Convert and print the JSON data
    schedule_data = csv_to_json(file_path)  # this is now a list of dictionaries
    json_data = json.dumps(schedule_data, indent=4)  # convert to JSON string for printing

    # Convert the schedule data to iCal format and add it to the main calendar
    cal_temp = json_to_ical(schedule_data, start_date, end_date)
    for component in cal_temp.subcomponents:
        cal.add_component(component)

# Write the iCal file
with open(args.output, 'wb') as f:
    f.write(cal.to_ical())
