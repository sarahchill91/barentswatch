#Usage: python authentication.py --id client_id --secret client_secret

import requests
import argparse

#credentials
config = {
	'token_url': 'https://id.barentswatch.no/connect/token',
	'api_base_url': 'https://www.barentswatch.no/bwapi'
}

def get_token(id, secret):

  req = requests.post(config['token_url'],
    data={
        'grant_type': 'client_credentials',
        'client_id': id,
        'client_secret': secret,
        'scope': 'api'
    },
    headers={'content-type': 'application/x-www-form-urlencoded'})

  req.raise_for_status()
  print('Token request successful')
  return req.json()

 	
if __name__== "__main__":
	parser = argparse.ArgumentParser()# Add an argument
	parser.add_argument('--id', type=str, required=True)
	parser.add_argument('--secret', type=str, required=True)
	args = parser.parse_args()
	print(f"Requesting token from {config['token_url']}.")
	token = get_token(args.id,args.token)
	print(token)