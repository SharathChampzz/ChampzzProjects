import os
from Helpers.api_request import ApiRequest
from Helpers.image_processing import ImageProcessing
from Helpers.indian_news import IndianNews

CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
NEWS_IMAGES_DIRECTORY = os.path.join(CURRENT_DIRECTORY, 'india_news_folder')
URL_FILE = os.path.join(CURRENT_DIRECTORY, 'src_urls.txt')



GET_GET_NEWS_COUNT = 5

def get_existing_urls(file_path):
    """Retrieve existing URLs from file."""
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return set(file.read().splitlines())
    return set()

def main():
    api_request = ApiRequest()
    image_processing = ImageProcessing()

    # get news from india today
    indian_news = IndianNews()
    data = indian_news.india_today()
    
    # create required directories
    if not os.path.exists(NEWS_IMAGES_DIRECTORY):
        os.mkdir(NEWS_IMAGES_DIRECTORY)
        
    # read existing URLs
    existing_urls = get_existing_urls(URL_FILE)

    # Iterate over the data and process each image
    GET_NEWS_COUNT = 5
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
            with open(URL_FILE, 'a') as file:
                file.write(f"{src}\n")

            # Generate a random image name based on the current time
            image_name = src.split('/')[-1]
            image_path = os.path.join(NEWS_IMAGES_DIRECTORY, image_name)
            print(f'Downloading image: {image_path}')

            # Download and process the image
            api_request.download_image(url=src, file_path=image_path)
            image_processing.add_caption_to_image(image_path=image_path, caption=title)

            GET_NEWS_COUNT -= 1
            if GET_NEWS_COUNT == 0:
                break
        except Exception as e:
            print(f"An error occurred: {e}")
            continue

if __name__ == "__main__":
    main()
