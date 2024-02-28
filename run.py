from app import create_app
from app.models import Category
import datetime

app = create_app()

@app.context_processor
def inject_categories():
    categories = Category.query.all()
    return dict(categories=categories)

@app.template_filter('datetimefmt')
def datetimefmt_filter(value, formats=None):
    """A custom Jinja filter to format datetime objects or strings with multiple possible formats."""
    if value is None:
        return ""
       
    if formats is None:
        formats = [
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d %H:%M:%S%Z",
            "%Y-%m-%d %H:%M:%S.%f%Z",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d %H:%M:%S.%f"
        ]
    
    if isinstance(value, str):
        value = trim_datetime_string(value)
        for fmt in formats:
            try:
                value = datetime.datetime.strptime(value, fmt)
                break  # Exit the loop on successful parsing
            except ValueError:
                continue  # Try the next format
        else:
            # If no format succeeded, return the original string or handle it differently
            return value
    
    # Adjust the output format to your preference
    return value.strftime('%B %d, %Y')

def trim_datetime_string(value):
    # Start from the end of the string and move backwards
    for i in range(len(value) - 1, -1, -1):
        if value[i] in ('.', '+', '-'):
            # Once we find a '.', '+' or '-', trim the string up to that point and stop
            return value[:i]
    # If we don't find any of the characters, return the original string
    return value

if __name__ == '__main__':
    app.run(debug=True)