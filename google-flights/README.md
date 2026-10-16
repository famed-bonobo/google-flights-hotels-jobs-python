# Google Flights API in 2026: How to Get Flight Prices from Google Flights with Python

Google Flights is the fare search most travelers trust: it compares airlines and booking sites, and it tells you whether today's price is low, typical or high for the route. Developers want that data for fare alerts, travel apps, route research and AI travel assistants.

There is no official way to get it. Google shut down its flight search API, QPX Express, in 2018, and nothing replaced it. This post shows what Google Flights actually sends to your browser, the options you have, and a working Python example that pulls every flight for several routes, with Google's price insights.

*Disclosure: I built the scraper used in the example. I'll also point to the open-source alternative so you can choose.*

## What's inside a Google Flights page

You don't need a browser to read Google Flights. The results page arrives with the flight data already embedded as JSON inside the HTML, and the search itself is described by a `tfs=` parameter in the URL. That parameter is a base64-encoded protocol buffer holding the airports, dates, passengers, cabin and number of stops.

The open-source project [fast-flights](https://github.com/AWeirdDev/flights) reverse-engineered that protocol buffer and is a great starting point if you want to build your own. The hard parts are everything around it:

- **Busy routes sometimes come back empty or with an error block.** You need to detect that and retry, otherwise you silently miss data.
- **Prices are per trip, not per person.** For a round trip with two adults, the price Google shows next to an outbound flight is the total for both travelers and both directions.
- **Price insights live in a separate block** and only make sense together with the route and dates.
- **At scale you need proxies and maintenance** whenever Google shifts its data layout.

## Your options

| Option | Effort | Cost | Good for |
|---|---|---|---|
| fast-flights (open source) | Medium | Free + your infrastructure | Hobby projects, full control |
| SERP API services | Low | Usually a monthly plan | Teams already using one |
| Apify actor (below) | Very low | $0.05 per 1,000 flights, pay as you go | Scheduled fare tracking, no servers |
| REST API on RapidAPI (same data) | Very low | 200 requests free, then from $9.99/month | Apps that need an answer in seconds, from any language |

## Step by step: several routes in a few lines of Python

### 1. Get an Apify token

Create a free Apify account, open **Settings → API & Integrations**, and copy your API token. Apify's free plan includes $5 of monthly credit.

```bash
export APIFY_TOKEN="your-token-here"
pip install apify-client
```

### 2. Search every origin against every destination

```python
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
```

This is the real output from running it:

```
JFK-LIS: 33 flights, cheapest $628 (TP 210, 0 stop(s)); Google says prices are typical, typical $420-$1550
JFK-MAD: 91 flights, cheapest $564 (TP 210 + TP 1014, 1 stop(s)); Google says prices are typical, typical $385-$1600
BOS-LIS: 61 flights, cheapest $692 (EI 132 + EI 482, 1 stop(s)); Google says prices are typical, typical $500-$1850
BOS-MAD: 65 flights, cheapest $450 (IB 346, 0 stop(s)); Google says prices are typical, typical $390-$1900
```

Four routes, 250 flights, about one cent.

## What you get for each flight

```json
{
  "origin": "SJO",
  "destination": "MIA",
  "tripType": "round_trip",
  "price": 761,
  "airlines": ["Avianca"],
  "stops": 1,
  "totalDurationMinutes": 530,
  "departureDateTime": "2026-12-10T01:50",
  "arrivalDateTime": "2026-12-10T11:40",
  "layovers": [{ "airport": "BOG", "city": "Bogotá", "durationMinutes": 155 }],
  "segments": [
    {
      "flightNumber": "AV 693",
      "aircraft": "Airbus A320",
      "legroom": "28 in",
      "departureDateTime": "2026-12-10T01:50",
      "arrivalDateTime": "2026-12-10T05:05"
    }
  ],
  "co2EmissionsKg": 640.0,
  "priceInsights": {
    "lowestPrice": 761,
    "typicalPriceLow": 490,
    "typicalPriceHigh": 980,
    "priceLevel": "typical"
  }
}
```

Times are local to each airport. The price level follows Google's own rule: below the typical range is "low", above it is "high".

## Building a fare alert

Google Flights publishes a price history for one-way searches. Turn on `includePriceHistory` and every flight carries the route's lowest price for each of the last several weeks (61 days in my tests). A simple daily alert:

1. Schedule the scraper once a day on Apify for your routes.
2. Read `priceInsights.priceLevel` from the results.
3. Notify yourself when it says `low`, or when `lowestPrice` drops below the last 30 days of the history.

Apify can call a webhook when each run finishes, so the whole alert needs no server of your own.

## Things to watch out for

- **Use airport codes, not cities.** `JFK`, not `New York`.
- **Round trips list outbound flights.** The price is for the whole trip, but return options depend on the outbound flight you pick, just like on Google's first results page.
- **Price history is only for one-way searches.** Google doesn't publish it for round trips.
- **Prices move.** Treat results as a snapshot and re-run before acting on a fare.

## Wrapping up

If you want full control and don't mind maintaining it, start from fast-flights. If you want flight data on a schedule without running anything yourself, the [Google Flights Scraper](https://apify.com/famed_bonobo/google-flights-scraper) does it for $0.05 per 1,000 flights. If you would rather call a plain REST endpoint from your own app, the same data (plus return flights, booking options and a 330-day price calendar) is available as the [Google Travel Data API on RapidAPI](https://rapidapi.com/famed-bonobo-famed-bonobo-default/api/google-travel-data), with a free tier of 200 requests. If something you need is missing, open an issue on either page.

---

*This article was written with the help of an AI assistant. The example code was run before publishing, and the output shown is real.*
