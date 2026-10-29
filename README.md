# Google Flights, Hotels, Jobs, Trends and Maps data in Python

Working examples for getting data from Google Flights, Google Hotels, Google Jobs, Google Trends and Google Maps, which have no official public API or a limited one. Each folder has a short tutorial and a script you can run.

| Folder | What it does |
|---|---|
| [`google-flights/`](google-flights/) | Every flight for several routes, with Google's price insights (low / typical / high) |
| [`google-hotels/`](google-hotels/) | Compares each hotel's price across booking sites (Booking.com, Expedia, Agoda...) |
| [`google-jobs/`](google-jobs/) | Job listings with salary, description and direct apply links, saved to CSV |
| [`google-trends/`](google-trends/) | Compare more than 5 Google Trends terms on one scale |
| [`google-maps/`](google-maps/) | Every unclaimed business of a category within a radius, not only the first 150, saved to CSV |

**Google Trends without an account:** the free, open-source [trendscale](https://github.com/famed-bonobo/trendscale)
library compares any number of terms on one 0-100 scale from your own machine, and replaces pytrends with one import.

**Google Hotels without an account:** the free, open-source [google-hotels](https://github.com/famed-bonobo/google-hotels)
library reads Google Hotels from your own machine (search, every booking site's offer, price calendar, reviews), with
the same fields as the hosted scraper below.

## Quick start

```bash
pip install apify-client
export APIFY_TOKEN="your-apify-token"   # Apify Settings -> API & Integrations
python google-jobs/google_jobs_example.py
```

The scripts call these scrapers on Apify (pay per result, Apify's free plan includes $5 of monthly credit):

- [Google Flights Scraper](https://apify.com/famed_bonobo/google-flights-scraper)
- [Google Hotels Scraper](https://apify.com/famed_bonobo/google-hotels-scraper)
- [Google Jobs Scraper](https://apify.com/famed_bonobo/google-jobs-scraper)
- [Google Trends Scraper](https://apify.com/famed_bonobo/google-trends-scraper)
- [Google Maps Scraper](https://apify.com/famed_bonobo/google-maps-scraper)

Prefer a REST endpoint you can call from any language, with the answer in seconds? The flights and hotels data is also available as the [Google Travel Data API on RapidAPI](https://rapidapi.com/famed-bonobo-famed-bonobo-default/api/google-travel-data) (200 requests free).

Disclosure: I maintain those scrapers and that API. Issues and suggestions are welcome here or on each scraper's page.

## License

MIT
