# Usage: python fiskehelse_combine_vessels_multithread.py --id client_id --secret client_secret

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
from fiskehelse_vesselsiteweek import get_week_vessel_summary
from fiskehelse_localitieswithsalmonoids_summary import get_summary_localities


token = get_token()

# Get a list of all salmonoid localities
localities_dict = get_summary_localities(token)

# Gives all weeks - hardcoded in temporarily
start_week = 1
end_week = 53
start_year = 2020
end_year = 2020
all_years = list(range(start_year,end_year+1,1))
all_weeks = list(range(start_week,end_week+1,1))

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
		

# Get the vessel data				
def runner():
	threads= []
	with open('vessels.csv', 'w', newline='') as csvfile:
		csvwriter = csv.writer(csvfile)
		csvwriter.writerow(["localityNo","anlysisBasedOnSurfaceArea","weekIsAnalyzed","mmsi", "vesselName","startTime","stopTime","shipType","isWellboat","shipRegisterVesselType","shipRegisterVesselTypeNameNo","shipRegisterVesselTypeNameEn"])
		with ThreadPoolExecutor(max_workers=20) as executor:
			for year, week in itertools.product(all_years, all_weeks):
				for locality in localities_dict:
					threads.append(executor.submit(get_week_vessel_summary, token, locality['localityNo'],year,week))
			for task in as_completed(threads):
				output = week_vessel_summary_class(**task.result())
				print(output.localityNo)
				if len(output.vesselVisits) > 0:
					for vesselvisits in output.vesselVisits:
						csvwriter.writerow([output.localityNo, output.anlysisBasedOnSurfaceArea, output.weekIsAnalyzed, vesselvisits.mmsi, vesselvisits.vesselName,vesselvisits.startTime,vesselvisits.stopTime,vesselvisits.shipType,vesselvisits.isWellboat,vesselvisits.shipRegisterVesselType,vesselvisits.shipRegisterVesselTypeNameNo,vesselvisits.shipRegisterVesselTypeNameEn])
					#else:
						#csvwriter.writerow([output.localityNo, output.anlysisBasedOnSurfaceArea, output.weekIsAnalyzed,"","","","","","","","",""])
					
runner()
	
	