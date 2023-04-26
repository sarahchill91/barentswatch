# Usage: python fiskehelse_detailedinfopersite.py --id client_id --secret client_secret  


import requests
from pprint import pprint
import argparse
from authentication import get_token, config
from pydantic import BaseModel
from typing import Optional


def get_detailed_info_per_week(token, localityId, year, week):
  url = f"{config['api_base_url']}/v1/geodata/fishhealth/locality/{localityId}/{year}/{week}"
  headers ={
    'authorization': 'Bearer ' + token['access_token'],
    'content-type': 'application/json',
  }

  response = requests.get(url, headers=headers)
  response.raise_for_status()
  return response.json()
  
  
class Organization_class(BaseModel):
    name: str
    organizationNo: Optional[str]  = None
    #Currently not storing all of the localities here as this seems to give a list of all other sites this operator works at
	#Also not storing the address of this company headquarters 
	
# Define a class for vessel data
class AquacultureLicense_class(BaseModel):
    capacity: float 
    expirationDate: Optional[str]  = None
    grantDate: str
    isGreen: bool
    licenseNo: str
    licensee: str
    productionType: str
    purpose: str
    species: list[str]
    unit: Optional[str]  = None
    localities: list[dict]
    #Currently not storing all of the localities here as this seems to give a list of all other sites this operator works at

class AquacultureRegister_class(BaseModel):
    aquaCultureUpdateTime: str
    capacity: float
    unit: str #I think this is a unit for capacity
    isGreen: bool
    lat: float
    licenses: list[AquacultureLicense_class]
    organizations: list[Organization_class]
    localityNo: int
    lon: float
    municipality: str
    municipalityNo: str
    name: str
    placement: str
    productionTypes: str
    purposes: str
    species: str
    speciesList: list[str]
    
class ProductionArea_class(BaseModel):
	id: int
	name: str
	
		
class LocalityWeek_class(BaseModel):
	id: int
	localityNo: int
	year: int
	week: int
	hasReportedLice: bool
	hasMechanicalRemoval: bool
	hasBathTreatment: bool
	hasInFeedTreatment: bool
	hasCleanerFishDeployed: bool
	isFallow: bool
	avgAdultFemaleLice: Optional[float]  = None
	avgMobileLice: Optional[float]  = None
	avgStationaryLice: Optional[float]  = None
	seaTemperature: Optional[float]  = None

    
class DetailedSiteInfo_class(BaseModel):
	aquaCultureRegister: Optional[AquacultureRegister_class]
	productionArea: Optional[ProductionArea_class]
	localityWeek: LocalityWeek_class
	#Currently this class ignores additional detail on fish escapes, export restructions, etc, sea temperature, ila production zones
	
if __name__== "__main__":
	parser = argparse.ArgumentParser()# Add an argument
	parser.add_argument('--id', type=str, required=True)
	parser.add_argument('--secret', type=str, required=True)
	args = parser.parse_args()
	token = get_token(args.id,args.secret)
	detailedsiteweeksummary= get_detailed_info_per_week(token,'13823','2017','45')
	pprint(detailedsiteweeksummary)
