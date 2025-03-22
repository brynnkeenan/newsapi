import feedparser
import requests
from bs4 import BeautifulSoup

def get_npr_article():
    feed = feedparser.parse('https://feeds.npr.org/1001/rss.xml')
    if not feed.entries:
        return {'source': 'NPR', 'title': 'No articles found', 'url': '', 'text': ''}

    entry = feed.entries[0]
    url = entry.link
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        title = soup.find('h1').text.strip()
        content = soup.find('article') or soup.find('div', class_='storytext')
        text = '\n\n'.join(p.text for p in content.find_all('p')) if content else entry.summary
    except Exception:
        title = entry.title
        text = entry.summary

    return {'source': 'NPR', 'title': title, 'url': url, 'text': text}

def get_the_conversation_article():
    feed = feedparser.parse('https://theconversation.com/us/articles.atom')
    if not feed.entries:
        return {'source': 'The Conversation', 'title': 'No articles found', 'url': '', 'text': ''}

    entry = feed.entries[0]
    url = entry.link
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    title = soup.find('h1').text.strip()
    content = soup.find('div', {'id': 'article-body'})
    text = '\n\n'.join(p.text for p in content.find_all('p')) if content else "No content found."
    return {'source': 'The Conversation', 'title': title, 'url': url, 'text': text}

def get_conservative_article():
    feed = feedparser.parse('https://www.theamericanconservative.com/feed/')
    if not feed.entries:
        return {'source': 'The American Conservative', 'title': 'No articles found', 'url': '', 'text': ''}

    entry = feed.entries[0]
    url = entry.link
    title = entry.title
    html_content = entry.get("content", [{}])[0].get("value", "") or entry.get("summary", "")
    soup = BeautifulSoup(html_content, 'html.parser')
    paragraphs = soup.find_all("p")
    text = '\n\n'.join(p.text.strip() for p in paragraphs if p.text and not p.text.lower().startswith("the post "))
    return {'source': 'The American Conservative', 'title': title, 'url': url, 'text': text}
