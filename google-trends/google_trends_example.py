"""Compare many search terms on one Google Trends scale and print which grew or shrank most.

Requires: pip install apify-client
Set your Apify API token in the APIFY_TOKEN environment variable first.
"""

import os

from apify_client import ApifyClient

# Google compares at most 5 terms at once; "anchored" chains groups through the first term so any number share one scale.
TERMS = ['python', 'javascript', 'java', 'rust', 'golang', 'php', 'ruby', 'kotlin']
WEEKS_PER_YEAR = 52

client = ApifyClient(os.environ['APIFY_TOKEN'])
run = client.actor('famed_bonobo/google-trends-scraper').call(run_input={
    'terms': TERMS,
    'geos': ['US'],
    'timeRange': 'past5Years',
    'comparison': 'anchored',
    'anchorTerm': TERMS[0],
    'includeRegions': False,
    'includeRelatedQueries': False,
})
results = list(client.dataset(run.default_dataset_id).iterate_items())

print(f"{'term':<12} {'average':>8} {'peak':>5}  last year vs first year")
for result in sorted(results, key=lambda result: -result['summary']['average']):
    values = [point['value'] for point in result['timeline']]
    first_year = sum(values[:WEEKS_PER_YEAR]) / WEEKS_PER_YEAR
    last_year = sum(values[-WEEKS_PER_YEAR - 1:-1]) / WEEKS_PER_YEAR
    change = f'{(last_year / first_year - 1) * 100:+.0f} %' if first_year else 'n/a'
    print(f"{result['term']:<12} {result['summary']['average']:>8} {result['summary']['peakValue']:>5}  {change}")
