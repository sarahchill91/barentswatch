# Usage: python fiskehelse_combine_vessels_multithread.py --id client_id --secret client_secret

import requests
import itertools
import pydantic
import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional
import csv
import argparse

from pprint import pprint
from authentication import get_token
from authentication import config
from pydantic import BaseModel
from findweeks import find_weeks
from fiskehelse_vesselsiteweek import get_week_vessel_summary
from fiskehelse_localitieswithsalmonoids_summary import get_summary_localities


parser = argparse.ArgumentParser()# Add an argument
parser.add_argument('--id', type=str, required=True)
parser.add_argument('--secret', type=str, required=True)
parser.add_argument('--start_date', type=str, required=True)
parser.add_argument('--end_date', type=str, required=True)
parser.add_argument('--output_path', type=str, required=True)
args = parser.parse_args()

token = get_token(args.id, args.secret)

all_weeks = find_weeks(args.start_date,args.end_date) # [1:] to exclude first week.

# Get a list of all salmonoid localities
localities_dict = get_summary_localities(token)

# Define a class for vessel data
class vessels(BaseModel):
      mmsi: int
      vesselName: str
      startTime: datetime.datetime
      stopTime: Optional[datetime.datetime]
      shipType: int
      isWellboat: bool
      shipRegisterVesselType: Optional[str]
      shipRegisterVesselTypeNameNo: Optional[str]
      shipRegisterVesselTypeNameEn: Optional[str]

# Define a class for vessel data
class week_vessel_summary_class(BaseModel):
	anlysisBasedOnSurfaceArea: bool
	localityNo: int
	vesselVisits: list[vessels]
	weekIsAnalyzed: bool
	year: str
	

output_file_name = 'vessels.csv'
output_file = "/".join([args.output_path,output_file_name])
print('printing output to ' + output_file)	

# Get the vessel data				
def runner():
	threads= []
	with open(output_file, 'w', newline='') as csvfile:
		csvwriter = csv.writer(csvfile)
		csvwriter.writerow(["localityNo","anlysisBasedOnSurfaceArea","weekIsAnalyzed","mmsi", "vesselName","startTime","stopTime","shipType","isWellboat","shipRegisterVesselType","shipRegisterVesselTypeNameNo","shipRegisterVesselTypeNameEn"])
		with ThreadPoolExecutor(max_workers=20) as executor:
			for year_week in all_weeks:
				year = year_week[0]
				week = year_week[1]
				print(year_week)
				for locality in localities_dict:
					threads.append(executor.submit(get_week_vessel_summary, token, locality['localityNo'],year,week))
			for task in as_completed(threads):
				output = week_vessel_summary_class(**task.result())
				if len(output.vesselVisits) > 0:
					for vesselvisits in output.vesselVisits:
						csvwriter.writerow([output.localityNo, output.anlysisBasedOnSurfaceArea, output.weekIsAnalyzed, vesselvisits.mmsi, vesselvisits.vesselName,vesselvisits.startTime,vesselvisits.stopTime,vesselvisits.shipType,vesselvisits.isWellboat,vesselvisits.shipRegisterVesselType,vesselvisits.shipRegisterVesselTypeNameNo,vesselvisits.shipRegisterVesselTypeNameEn])
					#else:
						#csvwriter.writerow([output.localityNo, output.anlysisBasedOnSurfaceArea, output.weekIsAnalyzed,"","","","","","","","",""])
					
runner()
	
	