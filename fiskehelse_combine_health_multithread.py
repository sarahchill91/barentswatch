# Usage: python fiskehelse_combine_health_multithread.py --id client_id --secret client_secret

import requests
import itertools
import pydantic
import datetime
from datetime import date
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional
import csv
import argparse

from pprint import pprint
from authentication import get_token
from pydantic import BaseModel
from fiskehelse_localitiesfishhealth import get_fishhealth_localities
from findweeks import find_weeks

parser = argparse.ArgumentParser()# Add an argument
parser.add_argument('--id', type=str, required=True)
parser.add_argument('--secret', type=str, required=True)
parser.add_argument('--start_date', type=str, required=True)
parser.add_argument('--end_date', type=str, required=True)
parser.add_argument('--output_path', type=str, required=True)

args = parser.parse_args()

token = get_token(args.id, args.secret)

all_weeks = find_weeks(args.start_date,args.end_date) # [1:] to exclude first week.

class persitehealth(BaseModel): 
	avgAdultFemaleLice: Optional[float]
	hasCleanerfishDeployed: bool
	hasIla: bool
	hasMechanicalRemoval: bool
	hasPd: bool
	hasReportedLice: bool
	hasSalmonoids: bool
	hasSubstanceTreatments: bool
	inFilteredSelection: bool
	isFallow: bool
	isOnLand: bool
	isSlaughterHoldingCage: bool
	lat: float
	lon: float
	localityNo: int
	localityWeekId: int
	municipality: str
	municipalityNo: int
	name: str

class health_class(BaseModel):
	localities: list[persitehealth]
	week: int
	year: int


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
				for persitehealth in output.localities:
					csvwriter.writerow([output.year, output.week, persitehealth.localityNo,persitehealth.name,persitehealth.hasSalmonoids,persitehealth.municipality,persitehealth.municipalityNo,persitehealth.lat,persitehealth.lon,persitehealth.isSlaughterHoldingCage,persitehealth.isOnLand,persitehealth.hasIla,persitehealth.hasPd,persitehealth.hasReportedLice,persitehealth.avgAdultFemaleLice,persitehealth.hasMechanicalRemoval,persitehealth.hasCleanerfishDeployed,persitehealth.isFallow])
					
runner()
	
	