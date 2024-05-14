import pdfplumber
import re
from collections import defaultdict
from datetime import datetime, timedelta

def is_today(date_str):
    """Check if the given date string is today's date."""
    date_format = '%d.%m.%Y'
    date_obj = datetime.strptime(date_str, date_format).date()
    return date_obj == datetime.today().date()

def is_tomorrow(date_str):
    """Check if the given date string is tomorrow's date."""
    date_format = '%d.%m.%Y'
    date_obj = datetime.strptime(date_str, date_format).date()
    return date_obj == (datetime.today().date() + timedelta(days=1))

def clean_line(line):
    """Remove unnecessary characters and spaces."""
    cleaned_line = re.sub(r'\.{2,}', ' ', line)  # Replace multiple dots with a single space
    return cleaned_line.strip()

def parse_table(pdf_path):
    schedule_data = defaultdict(list)
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue
            
            # Split text into lines
            lines = text.splitlines()
            current_class = None
            current_date = None
            current_normal_date = None
            current_normal_day = None
            
            for line in lines:
                cleaned_line = clean_line(line)
                
                # Match lines that look like class headers
                class_match = re.match(r'^([A-Z_]+\s*\d+/\d+)', cleaned_line)
                if class_match:
                    current_class = class_match.group(1)
                elif re.match(r'^\b(Mo|Di|Mi|Do|Fr|Sa|So)\b \d{2}\.\d{2}\.\d{4}', cleaned_line):
                    current_date = cleaned_line.split()  # Split to get date and day
                elif "VLehrer Kürzel" in cleaned_line:
                    continue  # Skip header line
                elif current_class and current_date:
                    details = re.split(r'\s{2,}', cleaned_line)  # Split on multiple spaces
                    try:
                        int(details[0])
                    except ValueError:
                        current_normal_date = details[0]
                        current_normal_day = details[1]
                        details = details[2:]

                    if len(details) >= 5:
                        details_dict = {
                            'date': current_normal_date,
                            'day': current_normal_day,
                            'position': details[0][0],
                            'teacher': details[1],
                            'subject': details[2],
                            'room': details[3],
                            'class': details[4],
                            'info': details[5] if len(details) > 5 else '',
                        }
                        schedule_data[current_class].append(details_dict)
    
    event_list = [event for data in schedule_data.values() for event in data]

    i = 0
    while i < len(event_list) - 1:
        current_event = event_list[i]
        next_event = event_list[i + 1]
        if (current_event['date'] == next_event['date'] and
            current_event['day'] == next_event['day'] and
            current_event['teacher'] == next_event['teacher'] and
            current_event['subject'] == next_event['subject'] and
            current_event['room'] == next_event['room'] and
            current_event['class'] == next_event['class']):

            event_list[i]['hours'] = current_event['position'] + '-' + next_event['position']
            del event_list[i + 1]

        else:
            if 'hours' not in event_list[i]:
                event_list[i]['hours'] = current_event['position']
            i += 1
                
    return event_list
