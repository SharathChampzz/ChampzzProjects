import requests
from bs4 import BeautifulSoup
from typing import List, Dict

class IndianNews:
    
    def __init__(self):
        pass
    
    def india_today(self) -> List[Dict[str, str]]:
        # Step 1: Make a request to the URL
        url = "https://www.indiatoday.in"
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful

        # Step 2: Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Step 3: Find all elements matching the given CSS selector
        # elements = soup.select('.B1S3_story__card__A_fhi .B1S3_content__thumbnail__wrap__iPgcS img')
        elements = soup.select('.B1S3_story__card__A_fhi .B1S3_content__thumbnail__wrap__iPgcS .B1S3_story__thumbnail___pFy6 a')
        print(f'Total news found: {len(elements)}')

        data = []
        for post in elements[:2]:
            post_url = f"{url}{post.get('href')}"
            title = post.get('title')
            child_image_src = post.find('img').get('src')
            print(f'Post URL: {post_url}')

            new_short_notes = requests.get(post_url)
            new_short_notes.raise_for_status()
            news_soup = BeautifulSoup(new_short_notes.text, 'html.parser')
            news_highlights = news_soup.select('ul.Story_highlights__list__FRRjs li')

            # get text from the news_highlights
            news_highlights_text = [highlight.get_text() for highlight in news_highlights]

            # '\n'.join(news_highlights_text)

            data.append({
                'title': title,
                'posturl': post_url, 
                'image': child_image_src.split('&size=')[0],
                'highlights': '<br>'.join(news_highlights_text)
                })

        
        return data

def publish_blog(title, content, news_source, image_url:str=None, image_path: str=None):
    url = 'http://127.0.0.1:8000/api/blogs/'
    headers = {
        'SkipAuth': 'true'
    }

    # Prepare the form data
    form_data = {
        'title': title,
        'content': content,
        'news_source': news_source
    }
    
    if image_url:
        form_data['image_url'] = image_url
        response = requests.post(url, headers=headers, data=form_data)
    else:
        # Open the image file in binary mode
        with open(image_path, 'rb') as image_file:
            files = {
                'image': image_file
            }
            response = requests.post(url, headers=headers, data=form_data, files=files)

    # Check if the request was successful
    if response.status_code == 200:
        print('Request was successful.')
        print('Response:', response.json())
    else:
        print('Request failed with status code:', response.status_code)
        print('Response:', response.text)

def download_image(url:str, file_path:str):
    img_response = requests.get(url, stream=True)
    if img_response.status_code == 200:
        with open(file_path, 'wb') as img_file:
            for chunk in img_response.iter_content(1024):
                img_file.write(chunk)
    else:
        raise Exception(f"Failed to download image: {img_response.status_code}: URL: {url}")
        
news = IndianNews()
news_data = news.india_today()
print(len(news_data))

for news in news_data:
    print(news['highlights'])
    # file_name = f'file_{random.randint(1, 1000)}'
    # file_name = f'news_image.jpg'
    # download_image(news['image'], file_name)
    publish_blog(title=news['title'], content=news.get('highlights'), news_source=news['posturl'], image_url=news['image'], image_path=None)
    
    # for key, value in news.items():
    #     print(f'{key}: {value}')
    #     # print('\n')
        