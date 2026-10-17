# Google Trends in Python: compare more than 5 terms on one scale

Google Trends has no public API, and its page compares at most five terms. Worse, every comparison is rescaled so its highest point is 100, so values from two comparisons cannot be read against each other.

`google_trends_example.py` gets around both limits with the [Google Trends Scraper on Apify](https://apify.com/famed_bonobo/google-trends-scraper) (pay per result, $0.40 per 1,000 terms; Apify's free plan includes $5 of monthly credit).

## How the comparison works

The scraper splits your terms into groups of four, adds one anchor term to every group, and uses the anchor's level in each group to bring all groups onto the first group's scale. Checked against Google's own five-term comparison, the values differ by 0.03 points on average.

## Run it

```bash
pip install -r requirements.txt
export APIFY_TOKEN="your-apify-token"   # Apify Settings -> API & Integrations
python google_trends_example.py
```

## Good to know

- **Words are ambiguous.** A search for `rust` also counts people looking for the video game. Use the scraper's `suggestions` mode to find a topic id such as `/m/0dsbpg6` (Rust, the language) and use the ids as terms.
- **Values are relative**, from 0 to 100, not search counts.
- The scraper also returns interest by region, related queries with Breakout growth, and Google's Trending now list with news.

Disclosure: I maintain that scraper.
