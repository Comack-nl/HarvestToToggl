import argparse

from datetime import date
from converters.HarvestToToggl import convert
from utils import get_date_range


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # Allow passing of month and year. Use current as defaults
    parser = argparse.ArgumentParser(description='Convert Harvest entries to Toggl')
    parser.add_argument(
        '--year',
        help='Year to get entries for. Defaults to the current year',
        default=date.today().year,
        type=int
    )

    parser.add_argument(
        '--month',
        help='Month to get entries for. Defaults to the current month',
        default=date.today().month,
        type=int
    )

    parser.add_argument(
        '--day',
        help='Day to get entries for. If omitted, gets the entire month',
        default=0,
        type=int
    )

    parser.add_argument(
        '--dry',
        help='Whether to only retrieve and parse data',
        default=False,
        action='store_true'
    )

    results = parser.parse_args()

    dates = get_date_range(results.day, results.month, results.year)

    convert(dates, results.dry)
