# Usage: python fiskehelse_vesselsiteweek.py --id client_id --secret client_secret  

import requests
from pprint import pprint
from authentication import get_token
from authentication import config
import argparse 

def get_week_vessel_summary(token, localityno, year, week):
  url = f"{config['api_base_url']}/v1/geodata/fishhealth/locality/{localityno}/vessel/{year}/{week}"
  headers ={
    'authorization': 'Bearer ' + token['access_token'],
    'content-type': 'application/json',
  }

  response = requests.get(url, headers=headers)
  response.raise_for_status()
  return response.json()

if __name__== "__main__":
	parser = argparse.ArgumentParser()# Add an argument
	parser.add_argument('--id', type=str, required=True)
	parser.add_argument('--secret', type=str, required=True)
	args = parser.parse_args()
	token = get_token(args.id,args.secret)
	vesselweeksummary= get_week_vessel_summary(token,'45135','2017','45')
	pprint(vesselweeksummary)
