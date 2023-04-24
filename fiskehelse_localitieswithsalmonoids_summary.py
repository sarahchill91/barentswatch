# Usage: python fiskehelse_localitieswithsalmonoids_summary.py --id client_id --secret client_secret

import requests
from pprint import pprint
from authentication import get_token
from authentication import config
import argparse

def get_summary_localities(token):
  url = f"{config['api_base_url']}/v1/geodata/fishhealth/localitieswithsalmonoids"
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
  localities= get_summary_localities(token)
  pprint(localities)
