from app import create_app
from app.models import Category
app = create_app()

@app.context_processor
def inject_categories():
    categories = Category.query.all()
    return dict(categories=categories)

if __name__ == '__main__':
    app.run(debug=True)