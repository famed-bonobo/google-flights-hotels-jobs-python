"""Compare hotel prices across booking sites for one city and stay, and show where each hotel is cheapest.

Requires: pip install apify-client
Set your Apify API token in the APIFY_TOKEN environment variable first.
"""

import os

from apify_client import ApifyClient

client = ApifyClient(os.environ['APIFY_TOKEN'])
run = client.actor('famed_bonobo/google-hotels-scraper').call(
    run_input={
        'queries': ['hotels in Lisbon'],
        'checkInDate': '2026-12-10',
        'checkOutDate': '2026-12-13',
        'adults': 2,
        'maxResultsPerQuery': 20,
        'includeBookingSources': True,
        'currency': 'EUR',
    },
)
hotels = list(client.dataset(run.default_dataset_id).iterate_items())

for hotel in hotels:
    offers = [offer for offer in hotel.get('bookingSources') or [] if offer['totalRate']]
    if not offers:
        continue
    cheapest = min(offers, key=lambda offer: offer['totalRate'])
    priciest = max(offers, key=lambda offer: offer['totalRate'])
    print(
        f"{hotel['name'][:40]:40} {hotel['overallRating'] or '-':>4}  "
        f"cheapest {cheapest['totalRate']:>7.2f} on {cheapest['source'][:18]:18} "
        f"(highest {priciest['totalRate']:.2f} on {priciest['source'][:18]}, {len(offers)} sites)"
    )
