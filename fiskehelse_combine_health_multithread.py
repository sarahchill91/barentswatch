# Usage: python3 fiskehelse_combine_health_multithread.py --id client_id --secret client_secret --start_date yyyy-mm-dd --end_date yyyy-mm-dd --output_path full_path

import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import csv
import argparse

from authentication import get_token
from fiskehelse_localitiesfishhealth import get_fishhealth_localities, health_class, persitehealth_class
from findweeks import find_weeks


parser = argparse.ArgumentParser()# Add an argument
parser.add_argument('--id', type=str, required=True)
parser.add_argument('--secret', type=str, required=True)
parser.add_argument('--start_date', type=str, required=True)
parser.add_argument('--end_date', type=str, required=True)
parser.add_argument('--output_path', type=str, required=True)

args = parser.parse_args()

token = get_token(args.id, args.secret)
all_weeks = find_weeks(args.start_date,args.end_date)[1:] # [1:] to exclude first week.


output_file_name = 'health.csv'
output_file = "/".join([args.output_path,output_file_name])
print('printing output to ' + output_file)
	
# Get the health data				
def runner():
	threads= []
	with open(output_file, 'w', newline='') as csvfile:
		csvwriter = csv.writer(csvfile)
		csvwriter.writerow(["year","week","localityNo","name","hasSalmonoids","municipality","municipalityNo","lat","lon","isSlaughterHoldingCage","isOnLand", \
		"hasIla", "hasPd","hasReportedLice","avgAdultFemaleLice","hasMechanicalRemoval","hasCleanerfishDeployed","isFallow"])
		with ThreadPoolExecutor(max_workers=20) as executor:
			for year_week in all_weeks:
				year = year_week[0]
				week = year_week[1]
				print(year_week)
				threads.append(executor.submit(get_fishhealth_localities, token, year,week))
			for task in as_completed(threads):
				output = health_class(**task.result())
				for persitehealth_class in output.localities:
					csvwriter.writerow([output.year, output.week, persitehealth_class.localityNo,persitehealth_class.name,persitehealth_class.hasSalmonoids,persitehealth_class.municipality,persitehealth_class.municipalityNo,persitehealth_class.lat,persitehealth_class.lon,persitehealth_class.isSlaughterHoldingCage,persitehealth_class.isOnLand,persitehealth_class.hasIla,persitehealth_class.hasPd,persitehealth_class.hasReportedLice,persitehealth_class.avgAdultFemaleLice,persitehealth_class.hasMechanicalRemoval,persitehealth_class.hasCleanerfishDeployed,persitehealth_class.isFallow])
					
runner()
	
	