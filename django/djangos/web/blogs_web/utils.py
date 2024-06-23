import os
import time
import requests
import sqlite3
from bs4 import BeautifulSoup
from typing import List, Dict
from backend.blogs_api.models import Blog
import logging
logger = logging.getLogger('django')

class News:
    def __init__(self, num_news: int = 5):
        self.num_news = num_news
        self.init_db()
        self.seen_news = self.load_seen_news()

    def init_db(self):
        """Initialize the SQLite database to store seen and failed news."""
        self.conn = sqlite3.connect('news_db.sqlite')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS news (
                id INTEGER PRIMARY KEY,
                title TEXT UNIQUE,
                status BOOLEAN
            )
        ''')
        self.conn.commit()

    def load_seen_news(self) -> set:
        """Load previously seen news titles from the SQLite database."""
        self.cursor.execute('SELECT title FROM news WHERE status = 1')
        return set(row[0] for row in self.cursor.fetchall())

    def save_news(self, title: str, status: bool):
        """Save news titles with their status to the SQLite database."""
        try:
            self.cursor.execute('INSERT INTO news (title, status) VALUES (?, ?)', (title, status))
            self.conn.commit()
        except sqlite3.IntegrityError:
            pass  # Ignore duplicates

    def fetch_india_today_news(self) -> List[Dict[str, str]]:
        base_url = "https://www.indiatoday.in"
        response = requests.get(base_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        elements = soup.select('.B1S3_story__card__A_fhi .B1S3_content__thumbnail__wrap__iPgcS .B1S3_story__thumbnail___pFy6 a')

        news_data = []
        count = 0
        for post in elements:
            if count >= self.num_news:
                break
            post_url = f"{base_url}{post.get('href')}"
            title = post.get('title')

            if title in self.seen_news:
                continue

            try:
                child_image_src = post.find('img').get('src')
                news_details = requests.get(post_url)
                news_details.raise_for_status()
                news_soup = BeautifulSoup(news_details.text, 'html.parser')
                news_highlights = news_soup.select('ul.Story_highlights__list__FRRjs li')
                highlights_text = [highlight.get_text() for highlight in news_highlights]

                news_data.append({
                    'title': title,
                    'posturl': post_url,
                    'image': child_image_src.split('&size=')[0],
                    'highlights': '<br>'.join(highlights_text)
                })

                self.seen_news.add(title)
                self.save_news(title, True)
                count += 1
                time.sleep(2)

            except Exception as e:
                print(f"Error processing news: {title}. Error: {e}")
                self.save_news(title, False)
                continue

        return news_data

    def fetch_times_of_india_news(self):
        # Placeholder for future implementation
        pass

def save_news_to_db():
    news = News(num_news=1)
    india_today_news = news.fetch_india_today_news()
    logger.info(f"India Today News: {india_today_news}")

    for news_item in india_today_news:
        try:
            blog = Blog(title=news_item['title'], content=news_item['highlights'], image_url=news_item['image'], news_source=news_item['posturl'])
            blog.save()
        except Exception as e:
            logger.error(f"Error saving news to database: {str(e)}")
            continue
