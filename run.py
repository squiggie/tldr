from app import create_app
from flask_apscheduler import APScheduler
from scripts.fetcharticles import fetch_and_store_articles
from scripts.summarizearticles import process_queue

app = create_app()
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()
scheduler.api_enabled = False

@scheduler.task('interval', id='job1', seconds=60, misfire_grace_time=900)
def job1():
    fetch_and_store_articles()

@scheduler.task('interval', id='job2', seconds=5, misfire_grace_time=900)
def job2():
    process_queue()

if __name__ == '__main__':
    app.run(debug=True)