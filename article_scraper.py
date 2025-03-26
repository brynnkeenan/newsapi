# Updated article_scraper.py to use readability-lxml for main article extraction
import feedparser
import requests
from bs4 import BeautifulSoup
from readability import Document

CHARACTER_THRESHOLD = 5156

article_cache = {}
seen_urls = set()  # Track previously served article URLs

def get_npr_article():
    feed = feedparser.parse('https://feeds.npr.org/1001/rss.xml')
    if not feed.entries:
        return {'source': 'NPR', 'title': 'No articles found', 'url': '', 'text': ''}

    best_article = None
    longest_text = ""

    for entry in feed.entries:
        url = entry.link
        if url in seen_urls:
            continue

        try:
            r = requests.get(url)
            doc = Document(r.text)
            title = doc.short_title()
            html = doc.summary()
            text = BeautifulSoup(html, "html.parser").get_text()
        except Exception:
            continue

        if len(text) >= CHARACTER_THRESHOLD:
            seen_urls.add(url)
            return {'source': 'NPR', 'title': title, 'url': url, 'text': text}

        if len(text) > len(longest_text):
            longest_text = text
            best_article = {'source': 'NPR', 'title': title, 'url': url, 'text': text}

    if best_article:
        seen_urls.add(best_article["url"])
    return best_article or {'source': 'NPR', 'title': 'No qualifying article found', 'url': '', 'text': ''}

def get_the_conversation_article():
    feed = feedparser.parse('https://theconversation.com/us/articles.atom')
    if not feed.entries:
        return {'source': 'The Conversation', 'title': 'No articles found', 'url': '', 'text': ''}

    best_article = None
    longest_text = ""

    for entry in feed.entries:
        url = entry.link
        if url in seen_urls:
            continue

        try:
            r = requests.get(url)
            doc = Document(r.text)
            title = doc.short_title()
            html = doc.summary()
            text = BeautifulSoup(html, "html.parser").get_text()
        except Exception:
            continue

        if len(text) >= CHARACTER_THRESHOLD:
            seen_urls.add(url)
            return {'source': 'The Conversation', 'title': title, 'url': url, 'text': text}

        if len(text) > len(longest_text):
            longest_text = text
            best_article = {'source': 'The Conversation', 'title': title, 'url': url, 'text': text}

    if best_article:
        seen_urls.add(best_article["url"])
    return best_article or {'source': 'The Conversation', 'title': 'No qualifying article found', 'url': '', 'text': ''}

def get_conservative_article():
    feed = feedparser.parse('https://www.theamericanconservative.com/feed/')
    if not feed.entries:
        return {'source': 'The American Conservative', 'title': 'No articles found', 'url': '', 'text': ''}

    best_article = None
    longest_text = ""

    for entry in feed.entries:
        title = entry.title
        url = entry.link
        if url in seen_urls:
            continue

        try:
            r = requests.get(url)
            doc = Document(r.text)
            html = doc.summary()
            text = BeautifulSoup(html, "html.parser").get_text()
        except Exception:
            continue

        if len(text) >= CHARACTER_THRESHOLD:
            seen_urls.add(url)
            return {'source': 'The American Conservative', 'title': title, 'url': url, 'text': text}

        if len(text) > len(longest_text):
            longest_text = text
            best_article = {'source': 'The American Conservative', 'title': title, 'url': url, 'text': text}

    if best_article:
        seen_urls.add(best_article["url"])
    return best_article or {'source': 'The American Conservative', 'title': 'No qualifying article found', 'url': '', 'text': ''}

def scrape_all_feeds():
    global article_cache
    article_cache = {
        "npr": get_npr_article(),
        "conversation": get_the_conversation_article(),
        "american_conservative": get_conservative_article()
    }
    return article_cache

def scrape_one_feed(source_name):
    if source_name == "npr":
        result = get_npr_article()
    elif source_name == "conversation":
        result = get_the_conversation_article()
    elif source_name == "american_conservative":
        result = get_conservative_article()
    else:
        return {"error": "Invalid source name"}

    article_cache[source_name] = result
    return {source_name: result}

def get_cached_articles():
    return article_cache if article_cache else {"error": "No articles cached yet"}