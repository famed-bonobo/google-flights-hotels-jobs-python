"""Find the cheapest flights on a few routes and show Google's price insights for each.

Requires: pip install apify-client
Set your Apify API token in the APIFY_TOKEN environment variable first.
"""

import os

from apify_client import ApifyClient

client = ApifyClient(os.environ['APIFY_TOKEN'])
run = client.actor('famed_bonobo/google-flights-scraper').call(
    run_input={
        'origins': ['JFK', 'BOS'],
        'destinations': ['LIS', 'MAD'],
        'departureDate': '2026-12-10',
        'returnDate': '2026-12-17',
        'adults': 1,
        'maxStops': '1',
        'currency': 'USD',
    },
)
flights = list(client.dataset(run.default_dataset_id).iterate_items())

routes = {}
for flight in flights:
    routes.setdefault((flight['origin'], flight['destination']), []).append(flight)

for (origin, destination), options in routes.items():
    cheapest = min((option for option in options if option['price']), key=lambda option: option['price'])
    insights = cheapest['priceInsights'] or {}
    numbers = ' + '.join(segment['flightNumber'] for segment in cheapest['segments'])
    print(
        f"{origin}-{destination}: {len(options)} flights, cheapest ${cheapest['price']} ({numbers}, "
        f"{cheapest['stops']} stop(s)); Google says prices are {insights.get('priceLevel')}, "
        f"typical ${insights.get('typicalPriceLow')}-${insights.get('typicalPriceHigh')}"
    )
