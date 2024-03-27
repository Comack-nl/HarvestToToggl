import sys
import requests

from dotenv import dotenv_values

config = dotenv_values('.env')

endpoints = {
    'time_entries': 'https://api.harvestapp.com/v2/time_entries'
}


def get_entries(start_date, end_date):
    headers = {
        'Authorization': f'Bearer {config.get("HARVEST_TOKEN")}',
        'Harvest-Account-Id': f'{config.get("HARVEST_ACCOUNT_ID")}',
        'User-Agent': 'HarvestToToggl (info@comack.nl)',
    }

    try:
        response = requests.get(
            endpoints.get('time_entries'),
            headers=headers,
            params={
                'from': start_date,
                'to': end_date
            }
        )
        response.raise_for_status()

        return response.json()
    except requests.exceptions.RequestException as e:
        print('An error occurred: ', e)
        sys.exit(1)
