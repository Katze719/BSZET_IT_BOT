import pdfplumber
import re
from collections import defaultdict
from datetime import datetime

def is_today(date_str):
    """Check if the given date string is today's date."""
    date_format = '%d.%m.%Y'
    date_obj = datetime.strptime(date_str, date_format).date()
    return date_obj == datetime.today().date()

def clean_line(line):
    """Remove consecutive dots while keeping date dots intact."""
    # Replace sequences of dots (more than 2) with a single space
    cleaned_line = re.sub(r'\.{2,}', ' ', line)
    return cleaned_line.strip()

def parse_schedule(pdf_path):
    schedule_data = defaultdict(list)

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue

            # Extract relevant lines
            lines = text.splitlines()
            current_class = None
            current_date = None
            current_normal_date = None
            current_normal_day = None

            for line in lines:
                cleaned_line = clean_line(line)

                if cleaned_line.startswith("B_"):
                    current_class = cleaned_line
                elif re.match(r'\b(Mo|Di|Mi|Do|Fr|Sa|So)\b \d{2}\.\d{2}\.\d{4}', cleaned_line):
                    current_date = cleaned_line
                elif re.search(r'\bfällt aus\b|\bRaumänderung\b|\bverlegt\b|\bganze Klasse\b|\bAufgaben\b', cleaned_line):
                    if current_class and current_date:
                        # Extract individual details by splitting on spaces
                        details = cleaned_line.split()
                        if len(details[0]) > 2:
                            current_normal_date = details[0]
                            current_normal_day = details[1]
                            details_dict = {
                                'date': details[0] if len(details) > 0 else '',
                                'day': details[1] if len(details) > 1 else '',
                                'position': details[2][0] if len(details) > 2 else '',
                                'teacher': details[3] if len(details) > 3 else '',
                                'subject': details[4] if len(details) > 4 else '',
                                'room': details[5] if len(details) > 5 else '',
                                'notification': details[7] if len(details) > 7 else '',
                                'substitution': details[8] if len(details) > 8 else '',
                                'class': current_class,
                                'full_info': cleaned_line
                            }
                        else :
                            details_dict = {
                                'date': current_normal_date,
                                'day': current_normal_day,
                                'position': details[0][0] if len(details) > 0 else '',
                                'teacher': details[1] if len(details) > 1 else '',
                                'subject': details[2] if len(details) > 2 else '',
                                'room': details[3] if len(details) > 3 else '',
                                'notification': details[5] if len(details) > 5 else '',
                                'substitution': details[6] if len(details) > 6 else '',
                                'class': current_class,
                                'full_info': cleaned_line
                            }
                        schedule_data[current_class].append(details_dict)

    return schedule_data

# Replace this path with the location of the uploaded PDF
pdf_path = './1142140749861888041.pdf'
schedule_data = parse_schedule(pdf_path)

# Printing the parsed data in a more readable format
for class_name, events in schedule_data.items():
    print(f"Class: {class_name}")
    for event in events:
        print(f"  Date: {event['date']}, Details: {event}")
        pass

