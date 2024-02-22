from app import create_app
from extensions import db
from app.models import ArticleQueue, Category
import feedparser

app = create_app()

categories = {
    'Business': 'https://news.google.com/rss/topics/CAAqJQgKIh9DQkFTRVFvTEwyY3ZNVEl4YW01eE1XMFNBbVZ1S0FBUAE?hl=en-US&gl=US&ceid=US:en',
    'Tech': 'https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGRqTVhZU0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US:en',
    'Entertainment':'https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNREpxYW5RU0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US:en',
    'Sports':'https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFp1ZEdvU0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US:en',
    'Science':'https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFp0Y1RjU0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US:en',
    'Health':'https://news.google.com/rss/topics/CAAqIQgKIhtDQkFTRGdvSUwyMHZNR3QwTlRFU0FtVnVLQUFQAQ?hl=en-US&gl=US&ceid=US:en',
    'Crypto':'https://news.google.com/rss/topics/CAAqJAgKIh5DQkFTRUFvS0wyMHZNSFp3YWpSZlloSUNaVzRvQUFQAQ?hl=en-US&gl=US&ceid=US:en'
}

def fetch_and_store_articles():
    with app.app_context():
        for category_name, rss_url in categories.items():
            feed = feedparser.parse(rss_url)
            category = Category.query.filter_by(name=category_name).first()
            if not category:
                category = Category(name=category_name)
                db.session.add(category)
                db.session.commit()
            for entry in feed.entries:
                exists = ArticleQueue.query.filter_by(guid=entry.guid).first() is not None
                if not exists:
                    article = ArticleQueue(url=entry.link, processed=False, guid=entry.guid, category_id=category.id)
                    db.session.add(article)
                    
            db.session.commit()
    
if __name__ == "__main__":
    fetch_and_store_articles()