from app.models import ArticleQueue, Category, Article
import feedparser
from transformers import pipeline
from newspaper import Article as NewspaperArticle
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import time
import os
from dotenv import load_dotenv

Base = declarative_base()
load_dotenv()
summarizer = pipeline("summarization", model="Falconsai/text_summarization")

categories = {
    'Business': 'https://news.google.com/rss/topics/CAAqJQgKIh9DQkFTRVFvTEwyY3ZNVEl4YW01eE1XMFNBbVZ1S0FBUAE?hl=en-US&gl=US&ceid=US:en',
    'Tech': 'https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGRqTVhZU0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US:en',
    'Entertainment':'https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNREpxYW5RU0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US:en',
    'Sports':'https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFp1ZEdvU0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US:en',
    'Science':'https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFp0Y1RjU0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US:en',
    'Health':'https://news.google.com/rss/topics/CAAqIQgKIhtDQkFTRGdvSUwyMHZNR3QwTlRFU0FtVnVLQUFQAQ?hl=en-US&gl=US&ceid=US:en',
    'Crypto':'https://news.google.com/rss/topics/CAAqJAgKIh5DQkFTRUFvS0wyMHZNSFp3YWpSZlloSUNaVzRvQUFQAQ?hl=en-US&gl=US&ceid=US:en'
}

if os.getenv('FLASK_ENV') == 'development':
    DEBUG = True
    DATABASE_URI = os.getenv('DEVELOPMENT_DATABASE_URI')
else:
    DEBUG = False
    DATABASE_URI = os.getenv('PRODUCTION_DATABASE_URI')

# Set up the engine
engine = create_engine(DATABASE_URI)

# Create a sessionmaker
Session = sessionmaker(bind=engine)

# Create tables (if they don't already exist)
Base.metadata.create_all(engine)

def fetch_and_store_articles():
    # Create a new session
    session = Session()
    for category_name, rss_url in categories.items():
        feed = feedparser.parse(rss_url)
        category = session.query(Category).filter_by(name=category_name).first()
        if not category:
            category = Category(name=category_name)
            session.add(category)
            session.commit()
        for entry in feed.entries:
            exists = session.query(ArticleQueue).filter_by(guid=entry.guid).first() is not None
            if not exists:
                article = ArticleQueue(url=entry.link, processed=False, guid=entry.guid, category_id=category.id)
                session.add(article)        
        session.commit()


def mark_article_as_processed(guid):
    # Create a new session
    session = Session()
    article = session.query(ArticleQueue).get(guid)
    if article:
        article.processed = True
        session.commit()

def fetch_article_details(url):
    article = NewspaperArticle(url)
    article.download()
    article.parse()
    return {
        "title": article.title,
        "authors": ", ".join(article.authors),
        "published_date": article.publish_date,
        "image": article.top_image,
        "text": article.text
    }

def generate_synopsis(text):
    # Ensure the text is not too long for the model
    max_chunk_size = 1024  # Adjust based on the model's max input size
    if len(text) > max_chunk_size:
        text = text[:max_chunk_size]
    
    summary = summarizer(text, max_length=1500, min_length=40, do_sample=False)
    return summary[0]['summary_text']

def process_queue():
    # Create a new session
    session = Session()
    # Fetch unprocessed URLs from the queue
    urls_to_process = session.query(ArticleQueue).filter_by(processed=False).limit(10)

    for queue_item in urls_to_process:
        try:
            details = fetch_article_details(queue_item.url)
            synopsis = generate_synopsis(details["text"])

            # Create and save the article with its synopsis
            article = Article(
                guid=queue_item.guid,
                url=queue_item.url,
                title=details["title"],
                author=details["authors"],
                published_date=details["published_date"] if details["published_date"] else datetime.datetime.now(),
                added_date=datetime.datetime.now(),
                image=details["image"],
                synopsis=synopsis,
                category_id=queue_item.category_id
            )
            session.add(article)
        except Exception as e:
            print(f"Error processing article {queue_item.url}: {e}")

        finally:
            # Mark article as processed regardless of success or failure
            queue_item.processed = True
            session.commit()

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_executor('threadpool')
    scheduler.add_job(fetch_and_store_articles, 'interval', seconds=60, id='job1', misfire_grace_time=900)
    scheduler.add_job(process_queue, 'interval', seconds=5, id='job2', misfire_grace_time=900)
    scheduler.start()

    try:
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()

if __name__ == "__main__":
    start_scheduler()