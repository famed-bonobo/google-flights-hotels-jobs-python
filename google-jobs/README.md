# Google Jobs API in 2026: How to Get Google Jobs Listings with Python

Google Jobs is one of the best job datasets on the web. It merges postings from LinkedIn, Indeed, Glassdoor, ZipRecruiter, company career pages and hundreds of smaller boards into one search, with salaries, job types and apply links already extracted. If you are building a job board, tracking who is hiring, or studying salaries, it is the obvious source.

There is one problem: **Google has no public Google Jobs API.** This post explains why getting the data yourself is harder than it looks, what your options are, and how to pull Google Jobs listings into Python or a CSV in a few lines.

## TL;DR

- There is no official API. Google's old Cloud Talent Solution is for employers searching their *own* jobs, not for reading Google Jobs results.
- Scraping it yourself means dealing with a JavaScript wall, captchas, and pagination that only works inside a browser session.
- The quickest route is a ready-made scraper. Below I use the [Google Jobs Scraper on Apify](https://apify.com/famed_bonobo/google-jobs-scraper) from Python, which costs $1.50 per 1,000 jobs.

*Disclosure: I built that scraper. I'll explain the technical hurdles honestly so you can decide whether to build your own instead.*

## Why scraping Google Jobs yourself is hard

I spent a good while on this before publishing the scraper, and these were the walls I hit:

1. **The JavaScript wall.** Since 2025, a plain HTTP request to Google Search returns a page that asks you to enable JavaScript. No job cards, no data. Browser user agents, mobile user agents and even text browsers all get the same answer.
2. **Captchas on cloud IPs.** If you switch to a headless browser on a server, Google quickly shows its "unusual traffic" page. Datacenter IPs are flagged almost immediately.
3. **Pagination needs a session.** Google Jobs shows 10 jobs, then loads the next 10 through an internal endpoint that only answers inside a real browser session with Google's cookies. The classic `&start=10` parameter returns nothing.
4. **Obfuscated markup.** The CSS class names are random strings that change. Anything that relies on them breaks within weeks.

None of this is impossible, but it turns "get some job data" into an ongoing maintenance project.

## Your options

| Option | Effort | Cost | Notes |
|---|---|---|---|
| Build your own scraper | High, ongoing | Proxies + your time | You own it, you fix it every time Google changes |
| SERP API services | Low | Usually a monthly plan | Billed per search page |
| Apify actor (below) | Very low | $1.50 per 1,000 jobs, pay as you go | No monthly fee; Apify's free plan includes $5 of monthly credit |

## Step by step: Google Jobs to CSV in Python

### 1. Get an Apify token

Create a free Apify account, open **Settings → API & Integrations**, and copy your personal API token. Store it in an environment variable:

```bash
export APIFY_TOKEN="your-token-here"
```

### 2. Install the client

```bash
pip install apify-client
```

### 3. Run the scraper and save a CSV

```python
import csv
import os

from apify_client import ApifyClient

SEARCHES = ['data analyst jobs in Chicago', 'registered nurse jobs Houston']
OUTPUT_FILE = 'google_jobs.csv'

client = ApifyClient(os.environ['APIFY_TOKEN'])
run = client.actor('famed_bonobo/google-jobs-scraper').call(
    run_input={'queries': SEARCHES, 'maxJobsPerQuery': 30, 'country': 'us', 'language': 'en'},
)
jobs = list(client.dataset(run.default_dataset_id).iterate_items())

with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['search', 'title', 'company', 'location', 'salary', 'posted', 'apply_url'])
    for job in jobs:
        first_option = job['applyOptions'][0] if job['applyOptions'] else {}
        writer.writerow([
            job['query'], job['title'], job['company'], job['location'],
            job['salary'], job['postedAgo'], first_option.get('directUrl') or first_option.get('url'),
        ])

print(f'Saved {len(jobs)} jobs to {OUTPUT_FILE}')
```

Write your searches the way you would type them into Google: a role and a place. Set `country` to the country of the job market. A German search with `country: "us"` often returns nothing, while the same search with `country: "de"` works.

## What you get for each job

```json
{
  "query": "software engineer jobs in Austin",
  "title": "System Software Engineer - Performance",
  "company": "NVIDIA",
  "location": "Austin, TX",
  "via": "via LinkedIn",
  "postedAgo": "21 hours ago",
  "employmentType": "Full-time",
  "salary": null,
  "highlights": {
    "Qualifications": ["..."],
    "Benefits": ["..."],
    "Responsibilities": ["..."]
  },
  "description": "We are looking for a System Software Engineer ...",
  "applyOptions": [
    {
      "label": "Apply on LinkedIn",
      "directUrl": "https://www.linkedin.com/jobs/view/system-software-engineer-performance-at-nvidia-4478174889"
    },
    {
      "label": "Apply on Glassdoor",
      "directUrl": "https://www.glassdoor.com/job-listing/jv?jl=1010294318621"
    }
  ]
}
```

Two details worth knowing:

- **Direct apply links.** Google wraps every apply link in its own redirect. The scraper follows each redirect, so `directUrl` points at the job page itself on LinkedIn, Indeed, Glassdoor or the company site.
- **Salary is often missing.** Google only shows a salary when the posting includes one. In my test searches that was roughly one job in three.

## Getting more than 10 jobs per search

Google lists only 10 jobs per search, and its "load more" endpoint is out of reach without a browser session. The workaround is the same thing Google's own filter menu does: it adds words to your search, like "full time", "remote" or "in the last week", or a posting-date filter. Each filtered search returns a different set of 10.

The scraper runs your search with those filters automatically and drops duplicates. In one test, `registered nurse jobs Houston` went from 10 jobs to 163 unique jobs. Set `maxJobsPerQuery` to the number you need.

Expect around 30 seconds for the first 10 jobs and a few minutes for 100+, since each Google answer takes about half a minute through the proxy. For large volumes, schedule the run and let it work in the background.

## What it costs

Pricing is $1.50 per 1,000 jobs, with no monthly fee, and platform usage is included. A run with 100 jobs costs about $0.15. You can set a maximum charge per run, and the scraper stops cleanly when it reaches it.

## Wrapping up

If you need Google Jobs data once, any option works. If you need it every day, the maintenance burden is the real cost. Whatever you choose, match the country to the job market, and don't rely on salary data being present.

If you try the [Google Jobs Scraper](https://apify.com/famed_bonobo/google-jobs-scraper) and something is missing or broken, open an issue on its page. I read them.

---

*This article was written with the help of an AI assistant. The example code was run before publishing, and the numbers come from real test runs.*
