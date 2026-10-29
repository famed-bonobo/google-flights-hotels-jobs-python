"""Find every dentist within 5 km of downtown Austin whose Google Maps listing nobody has claimed, and save them to CSV.

Unclaimed listings are businesses that never took control of their Google profile: useful prospects for local
marketing and SEO services. Requires: pip install apify-client
Set your Apify API token in the APIFY_TOKEN environment variable first.
"""

import csv
import os

from apify_client import ApifyClient

DOWNTOWN_AUSTIN = [-97.7431, 30.2672]  # GeoJSON order: longitude, latitude
RADIUS_KM = 5
OUTPUT_FILE = 'unclaimed_dentists.csv'

client = ApifyClient(os.environ['APIFY_TOKEN'])
run = client.actor('famed_bonobo/google-maps-scraper').call(
    run_input={
        'searchTerms': ['dentist'],
        'coverage': 'all',  # every place in the area, not only the first ~150 Google shows
        'customGeolocation': {'type': 'Point', 'coordinates': DOWNTOWN_AUSTIN, 'radiusKm': RADIUS_KM},
        'maxPlacesPerSearch': 1000,  # the default stops at 100
        'claimStatus': 'unclaimed',
    },
)
places = list(client.dataset(run.default_dataset_id).iterate_items())

with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['name', 'phone', 'website', 'address', 'rating', 'reviews', 'distance_km', 'google_maps_url'])
    for place in sorted(places, key=lambda place: place.get('distanceKm') or 0):
        writer.writerow([
            place['name'], place.get('phone'), place.get('website'), place.get('address'),
            place.get('rating'), place.get('reviewsCount'), place.get('distanceKm'), place.get('googleMapsUrl'),
        ])

print(f'Saved {len(places)} unclaimed dentists to {OUTPUT_FILE}')
