# Google Flights, Hotels and Jobs data in Python

Working examples for getting data from Google Flights, Google Hotels and Google Jobs, which have no official public API. Each folder has a short tutorial and a script you can run.

| Folder | What it does |
|---|---|
| [`google-flights/`](google-flights/) | Every flight for several routes, with Google's price insights (low / typical / high) |
| [`google-hotels/`](google-hotels/) | Compares each hotel's price across booking sites (Booking.com, Expedia, Agoda...) |
| [`google-jobs/`](google-jobs/) | Job listings with salary, description and direct apply links, saved to CSV |

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

Disclosure: I maintain those scrapers. Issues and suggestions are welcome here or on each scraper's page.

## License

MIT
