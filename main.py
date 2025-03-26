from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from article_scraper import scrape_all_feeds, scrape_one_feed, get_cached_articles

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/articles")
def fetch_articles():
    return get_cached_articles()

@app.get("/refresh-articles")
def refresh_articles():
    return scrape_all_feeds()

@app.get("/refresh-one")
def refresh_one(source: str = Query(..., description="Source name like 'npr', 'conversation', 'american_conservative'")):
    return scrape_one_feed(source)
