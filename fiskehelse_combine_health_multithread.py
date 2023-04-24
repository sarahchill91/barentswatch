# Usage: python fiskehelse_combine_health_multithread.py --id client_id --secret client_secret

import requests
import itertools
import pydantic
import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional
import csv

from pprint import pprint
from authentication import get_token
from authentication import config
from pydantic import BaseModel
from fiskehelse_localitiesfishhealth import get_fishhealth_localities


token = get_token()

# Gives all weeks - hardcoded in temporarily
start_week = 1
end_week = 52
start_year = 2015
end_year = 2023
all_years = list(range(start_year,end_year+1,1))
all_weeks = list(range(start_week,end_week+1,1))

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


# Get the health data				
def runner():
	threads= []
	with open('health.csv', 'w', newline='') as csvfile:
		csvwriter = csv.writer(csvfile)
		csvwriter.writerow(["year","week","localityNo","name","hasSalmonoids","municipality","municipalityNo","lat","lon","isSlaughterHoldingCage","isOnLand", \
		"hasIla", "hasPd","hasReportedLice","avgAdultFemaleLice","hasMechanicalRemoval","hasCleanerfishDeployed","isFallow"])
		with ThreadPoolExecutor(max_workers=20) as executor:
			for year, week in itertools.product(all_years, all_weeks):
				print(year, week)
				threads.append(executor.submit(get_fishhealth_localities, token, year,week))
			for task in as_completed(threads):
				output = health_class(**task.result())
				for persitehealth in output.localities:
					csvwriter.writerow([output.year, output.week, persitehealth.localityNo,persitehealth.name,persitehealth.hasSalmonoids,persitehealth.municipality,persitehealth.municipalityNo,persitehealth.lat,persitehealth.lon,persitehealth.isSlaughterHoldingCage,persitehealth.isOnLand,persitehealth.hasIla,persitehealth.hasPd,persitehealth.hasReportedLice,persitehealth.avgAdultFemaleLice,persitehealth.hasMechanicalRemoval,persitehealth.hasCleanerfishDeployed,persitehealth.isFallow])
					
runner()
	
	