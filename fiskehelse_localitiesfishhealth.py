# Usage: python fiskehelse_localitiesfishhealth.py --id client_id --secret client_secret
# Gets all data on fish health for one week - currently filtering to salmonoids only

import requests
from pprint import pprint
import argparse
from authentication import get_token
from authentication import config

def get_fishhealth_localities(token, year, week):
  # url = f"{config['api_base_url']}/v1/geodata/fishhealth/locality/{year}/{week}"
  url = f"{config['api_base_url']}/v1/geodata/fishhealth/locality/{year}/{week}?onlyWithSalmonoidLicense=true"
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
	localities= get_fishhealth_localities(token,'2023','14')
	pprint(localities)
