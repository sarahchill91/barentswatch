# Usage: python fiskehelse_localitieswithsalmonoids_summary.py --id client_id --secret client_secret

import requests
from pprint import pprint
from authentication import get_token
from authentication import config

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
  token = get_token()
  localities= get_summary_localities(token)
  pprint(localities)
