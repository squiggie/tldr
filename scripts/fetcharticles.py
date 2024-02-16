from app import create_app
from extensions import db
from app.models import ArticleQueue  # Import your model
import feedparser

app = create_app()

def fetch_and_store_articles():
    with app.app_context():
        # Example Google News RSS URL for top stories. Adjust as needed.
        rss_url = 'https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en'
        feed = feedparser.parse(rss_url)
        for entry in feed.entries:
            # Check if the article URL already exists in the database
            exists = ArticleQueue.query.filter_by(guid=entry.guid).first() is not None
            if not exists:
                article = ArticleQueue(url=entry.link, processed=False, guid=entry.guid)
                db.session.add(article)

        db.session.commit()
    
if __name__ == "__main__":
    fetch_and_store_articles()