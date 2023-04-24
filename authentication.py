#Usage: python authentication.py --id client_id --secret client_secret

import requests
import argparse#

parser = argparse.ArgumentParser()# Add an argument
parser.add_argument('--id', type=str, required=True)
parser.add_argument('--secret', type=str, required=True)
args = parser.parse_args()

#credentials
config = {
	'client_id': args.id,
	'client_secret': args.secret,
	'token_url': 'https://id.barentswatch.no/connect/token',
	'api_base_url': 'https://www.barentswatch.no/bwapi'
}

def get_token():

  if not config['client_id']:
    raise ValueError('client_id must be set in credentials.py')

  if not config['client_secret']:
    raise ValueError('client_secret must be set in credentials.py')

  req = requests.post(config['token_url'],
    data={
        'grant_type': 'client_credentials',
        'client_id': config['client_id'],
        'client_secret': config['client_secret'],
        'scope': 'api'
    },
    headers={'content-type': 'application/x-www-form-urlencoded'})

  req.raise_for_status()
  print('Token request successful')
  return req.json()

 	
if __name__== "__main__":
  print(f"Requesting token from {config['token_url']}, using client_id {config['client_id']}.")
  token = get_token()
  print(token)