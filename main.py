from news import fetch_news
from llm import summarize
from emailer import send_email


def run():
    articles = fetch_news()
    summary = summarize(articles)
    send_email(summary)


if __name__ == "__main__":
    try:
        run()
    except Exception:
        import traceback

        traceback.print_exc()
        raise
