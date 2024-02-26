from app import create_app
from flask_apscheduler import APScheduler
from scripts.fetcharticles import fetch_and_store_articles
from scripts.summarizearticles import process_queue

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)