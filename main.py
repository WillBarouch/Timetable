import csv
import json
import os
import icalendar
from datetime import datetime, timedelta


def csv_to_json(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)

        headers = next(reader)
        days = headers[1:]

        schedule = []
        current_time = None
        current_lesson = None
        current_class = None
        current_teacher = None
        current_location = None

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


def json_to_ical(json_data, filename):
    global start_time_str, end_time_str
    cal = icalendar.Calendar()

    # Determine if the schedule is for week 2 by checking the filename
    is_week2 = 'week2' in filename.lower()

    # Adjust the start date based on the week
    base_date = datetime(2024, 7, 22)  # Monday of week 1
    if is_week2:
        base_date += timedelta(weeks=1)  # Offset by one week for week 2

    day_to_date = {
        'Monday': base_date,
        'Tuesday': base_date + timedelta(days=1),
        'Wednesday': base_date + timedelta(days=2),
        'Thursday': base_date + timedelta(days=3),
        'Friday': base_date + timedelta(days=4)
    }

    for item in json_data:
        event = icalendar.Event()
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

        event.add('dtstart', start_datetime)
        event.add('dtend', end_datetime)
        event.add('location', item['Location'])

        # Add a recurrence rule to repeat the event every second week
        until_date = base_date + timedelta(weeks=9)  # Two-week interval for four weeks
        event.add('rrule', {'freq': 'weekly', 'interval': 2, 'until': until_date})

        cal.add_component(event)

    with open(os.path.join("/home/willbarouch/", filename), 'wb') as f:
        f.write(cal.to_ical())


# Path to the CSV file
file_path = 'week1.csv'

# Convert and print the JSON data
schedule_data = csv_to_json(file_path)  # this is now a list of dictionaries
json_data = json.dumps(schedule_data, indent=4)  # convert to JSON string for printing
print(json_data)

# Convert the schedule data to iCal format
json_to_ical(schedule_data, os.path.basename(file_path).replace('.csv', '.ics'))  # pass the list of dictionaries
