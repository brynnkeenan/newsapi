import feedparser
import requests
from bs4 import BeautifulSoup

CHARACTER_THRESHOLD = 5156

def get_npr_article():
    feed = feedparser.parse('https://feeds.npr.org/1001/rss.xml')
    if not feed.entries:
        return {'source': 'NPR', 'title': 'No articles found', 'url': '', 'text': ''}

    best_article = None
    longest_text = ""

    for entry in feed.entries:
        url = entry.link
        try:
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'html.parser')
            title = soup.find('h1').text.strip()
            content = soup.find('article') or soup.find('div', class_='storytext')
            text = '\n\n'.join(p.text for p in content.find_all('p')) if content else entry.summary
        except Exception:
            continue

        if len(text) >= CHARACTER_THRESHOLD:
            return {'source': 'NPR', 'title': title, 'url': url, 'text': text}

        if len(text) > len(longest_text):
            longest_text = text
            best_article = {'source': 'NPR', 'title': title, 'url': url, 'text': text}

    return best_article or {'source': 'NPR', 'title': 'No qualifying article found', 'url': '', 'text': ''}


def get_the_conversation_article():
    feed = feedparser.parse('https://theconversation.com/us/articles.atom')
    if not feed.entries:
        return {'source': 'The Conversation', 'title': 'No articles found', 'url': '', 'text': ''}

    best_article = None
    longest_text = ""

    for entry in feed.entries:
        url = entry.link
        try:
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'html.parser')
            title = soup.find('h1').text.strip()

            content = (
                soup.find('div', {'id': 'article-body'}) or 
                soup.find('div', {'class': 'content'}) or 
                soup.find('article')
            )

            if not content:
                continue

            paragraphs = content.find_all('p')
            text = '\n\n'.join(p.text.strip() for p in paragraphs if p.text.strip())

            if len(text) >= CHARACTER_THRESHOLD:
                return {'source': 'The Conversation', 'title': title, 'url': url, 'text': text}

            if len(text) > len(longest_text):
                longest_text = text
                best_article = {'source': 'The Conversation', 'title': title, 'url': url, 'text': text}
        except Exception:
            continue

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
        html_content = entry.get("content", [{}])[0].get("value", "") or entry.get("summary", "")
        soup = BeautifulSoup(html_content, 'html.parser')
        paragraphs = soup.find_all("p")
        text = '\n\n'.join(
            p.text.strip() for p in paragraphs 
            if p.text and not p.text.lower().startswith("the post ")
        )

        if len(text) >= CHARACTER_THRESHOLD:
            return {'source': 'The American Conservative', 'title': title, 'url': url, 'text': text}

        if len(text) > len(longest_text):
            longest_text = text
            best_article = {'source': 'The American Conservative', 'title': title, 'url': url, 'text': text}

    return best_article or {'source': 'The American Conservative', 'title': 'No qualifying article found', 'url': '', 'text': ''}
