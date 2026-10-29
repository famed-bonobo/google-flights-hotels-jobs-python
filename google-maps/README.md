# Google Maps in Python: every business in an area, not only the first 150

Google Maps shows only the most prominent places of a search; zoom out over a city and a search for "dentist" stops at a few dozen results. The Places API has the same ceiling (60 results per search) and charges per request.

`google_maps_example.py` uses the [Google Maps Scraper on Apify](https://apify.com/famed_bonobo/google-maps-scraper) (pay per result, $1.00 per 1,000 places; Apify's free plan includes $5 of monthly credit) to get every dentist within 5 km of downtown Austin whose listing the owner has never claimed, and saves them to a CSV file sorted by distance.

## How it finds every place

In *every place in the area* mode the scraper cuts the area into cells, searches each one, and splits the busy cells again until nothing new turns up. In a test on 3 km of central Chicago for "pizza", one search found 41 places and the full sweep found all 100.

## Run it

```bash
pip install -r requirements.txt
export APIFY_TOKEN="your-apify-token"   # Apify Settings -> API & Integrations
python google_maps_example.py
```

A test run on 28 October 2026 returned 100 unclaimed dentists within 5 km in about two minutes, each with phone, website when there is one, rating, reviews count and distance.

## Good to know

- **Unclaimed** means nobody has taken control of the business's Google profile: a common lead filter for local marketing and SEO services. Remove `claimStatus` to get every place.
- **Custom areas** can be a circle (as here) or any GeoJSON polygon, such as a postal code or a sales territory.
- The scraper stores business data only. It does not collect reviewers, review texts or owner profiles.

Disclosure: I maintain that scraper.
