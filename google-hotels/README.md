# Google Hotels API in 2026: Compare Hotel Prices Across Booking Sites with Python

Pick a hotel on Google Hotels and look at the list of booking sites under it. The same room, for the same nights, often costs very different amounts depending on where you book. When I ran the example below for three nights in Lisbon, one hotel ranged from **€307 to €678** across 23 sites.

That spread is exactly what revenue managers, travel apps and deal hunters want to track. But Google has no public Google Hotels API. This post shows how to get Google Hotels data, including the offer from every booking site, into Python.

*Disclosure: I built the scraper used in the example.*

## What Google Hotels gives you

For any city and dates, Google Hotels lists properties with:

- the lowest nightly price and the total for the stay, taxes and fees included;
- star class, guest rating and number of reviews;
- photos, coordinates and nearby places with travel times;
- and, on each hotel's page, **the offer from every booking site Google compares**: Booking.com, Expedia, Agoda, Trip.com, the hotel's own website and many smaller sites.

Like Google Flights, the page arrives with its data embedded as JSON, and the dates, guests and currency are encoded in a protocol buffer in the URL. That means you can read it without a browser, but you have to reproduce that encoding exactly and follow each hotel's page to get the per-site offers.

## Step by step: rate shopping in Python

### 1. Get an Apify token

Create a free Apify account, open **Settings → API & Integrations**, and copy your API token. Apify's free plan includes $5 of monthly credit.

```bash
export APIFY_TOKEN="your-token-here"
pip install apify-client
```

### 2. Find the cheapest booking site for every hotel

```python
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
```

Part of the real output, totals in euros for three nights:

```
Hotel Portugal - Portugal Boutique Hotel  4.7  cheapest  272.80 on Portugal Boutique  (highest 492.87 on Tripening Hotels, 26 sites)
Pestana Rua Augusta                       4.8  cheapest  324.51 on Vio.com            (highest 455.97 on Tripening Hotels, 17 sites)
Hotel da Baixa                            4.8  cheapest  420.59 on momondo.com        (highest 574.06 on Tripening Hotels, 33 sites)
LX Boutique Hotel                         4.3  cheapest  248.36 on KAYAK.com          (highest 389.22 on Qantas Hotels, 27 sites)
Heritage Lisboa Plaza Hotel - Avenida     4.5  cheapest  307.21 on Stayforlong.com    (highest 678.39 on BusinessHotels.com, 23 sites)
```

Two things stand out. The cheapest site changes from hotel to hotel, and sometimes it is the hotel's own website. Twenty hotels with every booking site's offer cost about $0.016 here: $0.40 per 1,000 hotels plus $0.40 per 1,000 hotels with booking-site offers.

## What you get for each hotel

```json
{
  "name": "Hôtel Villa Sorel",
  "hotelClass": 3,
  "overallRating": 4.3,
  "reviewsCount": 274,
  "ratePerNight": 83.52,
  "totalRate": 167.04,
  "taxesAndFees": 24.61,
  "currency": "USD",
  "checkInTime": "3:00 PM",
  "latitude": 48.8354461,
  "longitude": 2.2429921,
  "nearbyPlaces": [
    {
      "name": "Aéroport de Paris-Charles de Gaulle",
      "transportations": [
        { "mode": "taxi", "duration": "36 min" },
        { "mode": "public transport", "duration": "1 hr 21 min" }
      ]
    }
  ],
  "bookingSources": [
    { "source": "Hôtel Villa Sorel", "totalRate": 167.04, "bookingUrl": "https://www.google.com/travel/lodging/clk?..." },
    { "source": "Agoda", "totalRate": 196.01, "bookingUrl": "https://www.google.com/travel/lodging/clk?..." }
  ]
}
```

## Ideas for using it

- **Rate shopping for a hotel:** run it daily for your city and dates and watch what competitors charge on each site.
- **Price comparison apps:** show travelers every site's price, not just the lowest one.
- **Market research:** compare star class, ratings and prices between neighborhoods or cities.
- **Deal alerts:** flag hotels whose price on one site is far below the others.

## Things to watch out for

- **Phrase searches the way Google understands them:** `hotels in Lisbon` or `vacation rentals in Lisbon`. Some phrasings, like `Lisbon apartments`, make Google show a regular web search instead of hotel results.
- **Some hotels have no price.** That means no site has availability for your dates and guests; the hotel is still returned.
- **Prices include taxes and fees** unless the field name says otherwise, and they move constantly. Treat each run as a snapshot.

## Wrapping up

If you need hotel prices from Google Hotels on a schedule, with the offer from every booking site, the [Google Hotels Scraper](https://apify.com/famed_bonobo/google-hotels-scraper) does it without servers or browsers. If you need a field that's missing, open an issue on its page.

---

*This article was written with the help of an AI assistant. The example code was run before publishing, and the output shown is real.*
