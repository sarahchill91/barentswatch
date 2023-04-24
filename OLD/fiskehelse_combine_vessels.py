# Usage: python fiskehelse_combine_vessels.py --id client_id --secret client_secret

import requests
import itertools
import pydantic
import datetime
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

# Gives all weeks
start_week = 1
end_week = 53
start_year = 2015
end_year = 2023
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
      shipRegisterVesselType: str
      shipRegisterVesselTypeNameNo: str
      shipRegisterVesselTypeNameEn: str

# Define a class for vessel data
class week_vessel_summary_class(BaseModel):
	anlysisBasedOnSurfaceArea: bool
	localityNo: int
	vesselVisits: list[vessels]
	weekIsAnalyzed: bool
	year: str

with open('vessels.csv', 'w', newline='') as csvfile:
	csvwriter = csv.writer(csvfile)
	csvwriter.writerow(["localityNo", "vesselName"])


# Get the vessel data
	for year, week in itertools.product(all_years, all_weeks):
		for locality in localities_dict:
		
			vesselweeksummary = get_week_vessel_summary(token, locality['localityNo'],year,week)
			
			output = week_vessel_summary_class(**vesselweeksummary)
			print(output.localityNo)
			if len(output.vesselVisits) == 0:
				csvwriter.writerow([output.localityNo, ''])
			else:
				for vesselvisits in output.vesselVisits:
					csvwriter.writerow([output.localityNo, vesselvisits.vesselName])
	
	