from .models import Quotes
from typing import List, Dict

def add_quote(quote: str, author: str = 'Unknown') -> Quotes:
    """Add a new quote to the database."""
    new_quote = Quotes(quote=quote, author=author)
    new_quote.save()
    return new_quote

def get_quotes() -> List[Dict]:
    """Get all quotes from the database."""
    quotes = Quotes.objects.all()
    return [{'id': quote.id, 'quote': quote.quote, 'author': quote.author, 'date_added': quote.date_added} for quote in quotes]

def get_quote(quote_id: int) -> Dict:
    """Get a specific quote from the database."""
    quote = Quotes.objects.get(id=quote_id)
    return {'id': quote.id, 'quote': quote.quote, 'author': quote.author, 'date_added': quote.date_added}

def modify_quote(quote_id: int, new_quote: str = None, new_author: str = None) -> Quotes:
    """Modify an existing quote."""
    quote = Quotes.objects.get(id=quote_id)
    if new_quote:
        quote.quote = new_quote
    if new_author:
        quote.author = new_author
    # TODO: Update modified time
    quote.save()
    return quote

