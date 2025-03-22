from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from article_scraper import get_npr_article, get_the_conversation_article, get_conservative_article

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
    return [
        get_npr_article(),
        get_the_conversation_article(),
        get_conservative_article()
    ]
