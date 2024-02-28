from models import Authors, Quotes, Tag
from connect import connect
from datetime import datetime
import json

# Read authors.json and save authors
with open('../authors.json') as f:
    authors_data = json.load(f)
    for author_data in authors_data:
        author = Authors(
            fullname=author_data['fullname'],
            born_date=datetime.strptime(author_data['born_date'], '%B %d, %Y'),
            born_location=author_data['born_location'],
            description=author_data['description']
        )
        author.save()

# Read quotes.json and save quotes
with open('../quotes.json') as f:
    quotes_data = json.load(f)
    for quote_data in quotes_data:
        author = Authors.objects(fullname=quote_data['author']).first()
        if author:
            quote = Quotes(
                tags=[Tag(name=tag) for tag in quote_data['tags']],
                author=author,
                quote=quote_data['quote']
            )
            quote.save()
        else:
            print(f"Author '{quote_data['author']}' not found for quote '{quote_data['quote']}'")
