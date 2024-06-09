import os
import requests
from bs4 import BeautifulSoup
from Helpers.api_request import ApiRequest
from Helpers.image_processing import ImageProcessing

def create_directory(path):
    """Create directory if it doesn't exist."""
    if not os.path.exists(path):
        os.mkdir(path)

def get_existing_urls(file_path):
    """Retrieve existing URLs from file."""
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return set(file.read().splitlines())
    return set()

def main():
    api_request = ApiRequest()
    image_processing = ImageProcessing()

    # Step 1: Make a request to the URL
    url = "https://www.indiatoday.in/"
    response = requests.get(url)
    response.raise_for_status()  # Check if the request was successful

    # Step 2: Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Step 3: Find all elements matching the given CSS selector
    elements = soup.select('.B1S3_story__card__A_fhi .B1S3_content__thumbnail__wrap__iPgcS img')
    print(f'Total news found: {len(elements)}')

    # Step 4: Extract the src and title attributes
    data = [{'src': img.get('src'), 'title': img.get('title')} for img in elements if img.get('src') and img.get('title')]

    # Create directories and file paths
    current_directory = os.path.dirname(os.path.abspath(__file__))
    images_directory = os.path.join(current_directory, 'india_news_folder')
    create_directory(images_directory)

    src_file_path = os.path.join(current_directory, 'src_urls.txt')
    existing_urls = get_existing_urls(src_file_path)

    # Step 5: Iterate over the data and process each image
    news_count = 5
    print(f'Iterating over {len(data)} news items...')
    for item in data:
        try:
            src = item['src'].split('?')[0]
            title = item['title']

            if src in existing_urls:
                print('The src URL already exists in the file')
                continue

            if '.gif?' in src:
                continue

            # Print the title and src
            print(f"Title: {title}, Src: {src}")

            # Add the src URL to the file
            with open(src_file_path, 'a') as file:
                file.write(f"{src}\n")

            # Generate a random image name based on the current time
            image_name = src.split('/')[-1]
            image_path = os.path.join(images_directory, image_name)
            print(f'Downloading image: {image_path}')

            # Download and process the image
            api_request.download_image(url=src, file_path=image_path)
            image_processing.add_caption_to_image(image_path=image_path, caption=title)

            news_count -= 1
            if news_count == 0:
                break
        except Exception as e:
            print(f"An error occurred: {e}")
            continue

if __name__ == "__main__":
    main()
