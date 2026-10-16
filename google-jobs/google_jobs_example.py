"""Fetch Google Jobs listings for a few searches and save them to a CSV file.

Requires: pip install apify-client
Set your Apify API token in the APIFY_TOKEN environment variable first.
"""

import csv
import os

from apify_client import ApifyClient

SEARCHES = ['data analyst jobs in Chicago', 'registered nurse jobs Houston']
OUTPUT_FILE = 'google_jobs.csv'

client = ApifyClient(os.environ['APIFY_TOKEN'])
run = client.actor('famed_bonobo/google-jobs-scraper').call(
    run_input={'queries': SEARCHES, 'maxJobsPerQuery': 30, 'country': 'us', 'language': 'en'},
)
jobs = list(client.dataset(run.default_dataset_id).iterate_items())

with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['search', 'title', 'company', 'location', 'salary', 'posted', 'apply_url'])
    for job in jobs:
        first_option = job['applyOptions'][0] if job['applyOptions'] else {}
        writer.writerow([
            job['query'], job['title'], job['company'], job['location'],
            job['salary'], job['postedAgo'], first_option.get('directUrl') or first_option.get('url'),
        ])

print(f'Saved {len(jobs)} jobs to {OUTPUT_FILE}')
