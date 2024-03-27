import sys

import requests
from dotenv import dotenv_values
from base64 import b64encode

config = dotenv_values('.env')
workspace_id = config.get('TOGGL_WORKSPACE_ID')
token = config.get('TOGGL_TOKEN')

endpoints = {
    'entries': 'https://api.track.toggl.com/api/v9/time_entries',
    'my_entries': 'https://api.track.toggl.com/api/v9/me/time_entries',
    'projects': f'https://api.track.toggl.com/api/v9/workspaces/{workspace_id}/projects'
}


def push_entries(entries_to_push):
    # Authenticate with Toggl
    headers = {
        'content-type': 'application/json',
        'Authorization': 'Basic %s' % b64encode(bytes(f'{token}:api_token', 'utf-8')).decode('ascii')
    }

    total = 0

    for entry in entries_to_push:
        try:
            response = requests.post(endpoints.get('entries'), json=entry, headers=headers)
            response.raise_for_status()

            if response.status_code == 200:
                total += 1

        except requests.exceptions.RequestException as e:
            print('An error occurred: ', e)
            sys.exit(1)

    print(f'Pushed {total} entries to Toggl')


def get_existing_entries(start_date, end_date):
    headers = {
        'content-type': 'application/json',
        'Authorization': 'Basic %s' % b64encode(bytes(f'{token}:api_token', 'utf-8')).decode('ascii')
    }

    try:
        response = requests.get(endpoints.get('my_entries'), params={
            'start_date': start_date,
            'end_date': end_date
        }, headers=headers)
        response.raise_for_status()

        return response.json()
    except requests.exceptions.RequestException as e:
        print('An error occurred: ', e)
        sys.exit(1)


def get_project(project_name):
    headers = {
        'content-type': 'application/json',
        'Authorization': 'Basic %s' % b64encode(bytes(f'{token}:api_token', 'utf-8')).decode('ascii')
    }

    try:
        response = requests.get(endpoints.get('projects'), headers=headers, params={'name': project_name})
        response.raise_for_status()

        return response.json()
    except requests.exceptions.RequestException as e:
        print('An error occurred: ', e)
        sys.exit(1)
