import requests
from bs4 import BeautifulSoup
from typing import List, Dict

class IndianNews:
    
    def __init__(self):
        pass
    
    def india_today(self) -> List[Dict[str, str]]:
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
        
        # Update data with more details in future, If in case we need more details
        
        return data