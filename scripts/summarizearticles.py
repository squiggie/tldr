from transformers import pipeline
from newspaper import Article as NewspaperArticle
from extensions import db
from app.models import ArticleQueue, Article
import datetime
from app import create_app

app = create_app()

# Load the summarization pipeline
summarizer = pipeline("summarization", model="Falconsai/text_summarization")

def mark_article_as_processed(guid):
    with app.app_context():
        article = ArticleQueue.query.get(guid)
        if article:
            article.processed = True
            db.session.commit()

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
    with app.app_context():
        # Fetch unprocessed URLs from the queue
        urls_to_process = ArticleQueue.query.filter_by(processed=False).limit(10)

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
                db.session.add(article)
            except Exception as e:
                print(f"Error processing article {queue_item.url}: {e}")

            finally:
                # Mark article as processed regardless of success or failure
                queue_item.processed = True
                db.session.commit()

if __name__ == "__main__":
    process_queue()