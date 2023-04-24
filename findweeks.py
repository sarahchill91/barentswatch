# Usage: python findweeks.py --id client_id --secret client_secret

import datetime
from datetime import date
import argparse

def find_weeks(start_date,end_date):
    l = []
    start_date = date.fromisoformat(start_date)
    end_date = date.fromisoformat(end_date)
    for i in range((end_date-start_date).days + 1):
        yearweek = (start_date+datetime.timedelta(days=i)).isocalendar()[:2] # e.g. (2011, 52)
        l.append(yearweek)
    return sorted(set(l))


if __name__== "__main__":
	parser = argparse.ArgumentParser()# Add an argument
	parser.add_argument('--start_date', type=str, required=True)
	parser.add_argument('--end_date', type=str, required=True)
	args = parser.parse_args()
	start_date = '2023-01-01'
	end_date = '2023-09-06'
	print(find_weeks(start_date,end_date)) # [1:] to exclude first week.
