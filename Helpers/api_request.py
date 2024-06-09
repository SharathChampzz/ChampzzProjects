import requests

class ApiRequest:
    
    def __init__(self):
        pass
    
    def download_image(self, url:str, file_path:str):
        img_response = requests.get(url, stream=True)
        if img_response.status_code == 200:
            with open(file_path, 'wb') as img_file:
                for chunk in img_response.iter_content(1024):
                    img_file.write(chunk)
        else:
            raise Exception(f"Failed to download image: {img_response.status_code}: URL: {url}")
                    
    