import json
import hashlib

from datetime import datetime, timedelta
from services.Harvest import get_entries
from services.Toggl import push_entries, get_project, get_existing_entries
from dotenv import dotenv_values

config = dotenv_values('.env')
file = open('mappings.json')
mappings = json.load(file)


def map_project(project_name: str):
    if project_name not in mappings['project']:
        return project_name

    return mappings['project'][project_name]


def map_entry_dates(entry):
    # Convert start time and calculate end time
    start_dt = datetime.fromisoformat(entry['created_at'])
    end_dt = start_dt + timedelta(hours=entry['hours'])

    return {
        'start': start_dt.isoformat(),
        'stop': end_dt.isoformat()
    }


def get_project_id_by_name(project_name):
    projects = get_project(project_name)

    return projects[0]['id'] if len(projects) > 0 else -1


def parse_entries(entries_to_parse):
    results = []

    for entry in entries_to_parse['time_entries']:

        # Convert start time and calculate end time
        start_dt = datetime.fromisoformat(entry['created_at'])
        end_dt = start_dt + timedelta(hours=entry['hours'])

        project = map_project(entry['project'].get('name'))

        parsed_entry = {
            'billable': entry['billable'],
            # 'client': entry['client'].get('name'),
            'description': entry['notes'],
            'workspace_id': int(config.get('TOGGL_WORKSPACE_ID')),
            'created_with': 'HarvestToToggl',
            'start': start_dt.isoformat(),
            'stop': end_dt.isoformat(),
            'project_id': get_project_id_by_name(project)
        }

        results.append(parsed_entry)

    return results


def create_hash_from_entry(entry):
    values = {
        'start': entry['start'],
        'stop': entry['stop'],
        'workspace_id': entry['workspace_id'],
        'project_id': entry['project_id'],
        'description': entry['description']
    }

    # Sanitize the data to ensure consistency
    hash_string = '-'.join(str(v).strip().lower().replace(' ', '-') for v in values.values())

    return hashlib.sha256(json.dumps(hash_string).encode('utf-8')).hexdigest()


def filter_existing(entries, daterange):
    if len(entries) == 0:
        return entries

    existing_entries = get_existing_entries(daterange[0], daterange[1] + timedelta(days=1))
    hashed_existing = [create_hash_from_entry(entry) for entry in existing_entries]

    return [entry for entry in entries if create_hash_from_entry(entry) not in hashed_existing]


def convert(daterange, dry=False):
    entries = get_entries(daterange[0], daterange[1])
    entries_count = len(entries['time_entries'])

    print(f'Found {entries_count} entries in Harvest')

    parsed_entries = parse_entries(entries)

    print(f'Parsed {len(parsed_entries)} entries')

    # Filter out pre-existing entries based on description and start/end date
    filtered_entries = filter_existing(parsed_entries, daterange)

    print(f'Filtered out {abs(len(parsed_entries) - len( filtered_entries ))} entries')

    if not dry:
        push_entries(filtered_entries)
