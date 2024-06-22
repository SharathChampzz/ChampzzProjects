import os
import time
import requests
from bs4 import BeautifulSoup
from typing import List, Dict

class IndianNews:
    def __init__(self, num_news: int = 5):
        self.base_url = "https://www.indiatoday.in"
        self.num_news = num_news
        self.seen_news = self.load_seen_news()

    def load_seen_news(self) -> set:
        """Load previously seen news titles from a local file."""
        if os.path.exists('seen_news.txt'):
            with open('seen_news.txt', 'r') as file:
                return set(file.read().splitlines())
        return set()

    def save_seen_news(self):
        """Save seen news titles to a local file."""
        with open('seen_news.txt', 'w') as file:
            for title in self.seen_news:
                file.write(f"{title}\n")

    def fetch_news(self) -> List[Dict[str, str]]:
        response = requests.get(self.base_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        elements = soup.select('.B1S3_story__card__A_fhi .B1S3_content__thumbnail__wrap__iPgcS .B1S3_story__thumbnail___pFy6 a')

        news_data = []
        count = 0
        for post in elements:
            if count >= self.num_news:
                break
            post_url = f"{self.base_url}{post.get('href')}"
            title = post.get('title')

            if title in self.seen_news:
                continue

            try:
                child_image_src = post.find('img').get('src')
                news_details = requests.get(post_url) # get highlights from the post url page
                news_details.raise_for_status()
                news_soup = BeautifulSoup(news_details.text, 'html.parser')
                news_highlights = news_soup.select('ul.Story_highlights__list__FRRjs li')
                highlights_text = [highlight.get_text() for highlight in news_highlights]
                
                # TODO: Get the full content of the news post and summarize using NLP and add to highlights_text

                news_data.append({
                    'title': title,
                    'posturl': post_url,
                    'image': child_image_src.split('&size=')[0],
                    'highlights': '<br>'.join(highlights_text)
                })

                self.seen_news.add(title)
                count += 1
                time.sleep(2)  # Adding delay to avoid bot detection

            except Exception as e:
                print(f"Error processing news: {title}. Error: {e}")
                continue

        self.save_seen_news()
        return news_data

def publish_blog(title, content, news_source, image_url: str = None, image_path: str = None):
    url = 'http://127.0.0.1:8000/api/blogs/'
    headers = {'SkipAuth': 'true'}

    form_data = {
        'title': title,
        'content': content,
        'news_source': news_source
    }

    try:
        if image_url:
            form_data['image_url'] = image_url
            response = requests.post(url, headers=headers, data=form_data)
        else:
            with open(image_path, 'rb') as image_file:
                files = {'image': image_file}
                response = requests.post(url, headers=headers, data=form_data, files=files)

        response.raise_for_status()
        print('Request was successful.')
        print('Response:', response.json())

    except Exception as e:
        print(f"Failed to publish blog: {title}. Error: {e}")
        print('Response:', response.json())

if __name__ == "__main__":
    news_fetcher = IndianNews(num_news=5)
    news_data = news_fetcher.fetch_news()
    print(f"Total news to be published: {len(news_data)}")

    for news in news_data:
        publish_blog(
            title=news['title'],
            content=news.get('highlights'),
            news_source=news['posturl'],
            image_url=news['image']
        )
