# Google Flights, Hotels and Jobs data in Python

Working examples for getting data from Google Flights, Google Hotels and Google Jobs, which have no official public API. Each folder has a short tutorial and a script you can run.

| Folder | What it does |
|---|---|
| [`google-flights/`](google-flights/) | Every flight for several routes, with Google's price insights (low / typical / high) |
| [`google-hotels/`](google-hotels/) | Compares each hotel's price across booking sites (Booking.com, Expedia, Agoda...) |
| [`google-jobs/`](google-jobs/) | Job listings with salary, description and direct apply links, saved to CSV |
| [`google-trends/`](google-trends/) | Compare more than 5 Google Trends terms on one scale |

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

Prefer a REST endpoint you can call from any language, with the answer in seconds? The flights and hotels data is also available as the [Google Travel Data API on RapidAPI](https://rapidapi.com/famed-bonobo-famed-bonobo-default/api/google-travel-data) (200 requests free).

Disclosure: I maintain those scrapers and that API. Issues and suggestions are welcome here or on each scraper's page.

## License

MIT
