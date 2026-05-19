import feedparser

FEEDS = [
    "https://hnrss.org/newest?q=artificial+intelligence",
    "https://www.theverge.com/artificial-intelligence/rss/index.xml"
]

def fetch_news():
    articles = []

    for url in FEEDS:
        feed = feedparser.parse(url)

        for entry in feed.entries[:10]:
            articles.append({
                "title": entry.title,
                "link": entry.link,
                "summary": getattr(entry, "summary", "")
            })

    return articles
