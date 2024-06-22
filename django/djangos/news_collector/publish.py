import requests

def publish_blog(title, content, image_path, news_source):
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

# Example usage
title = 'Sample Title'
content = 'Sample content for the blog post.'
image_path = r"C:\Users\sharathkumarhk\Pictures\Screenshots\Screenshot 2023-03-01 114903.png"
publish_blog(title, content, image_path)
