from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
import time
import datetime

class Browser:
    def __init__(self, driver_location, headless=True):
        self.chrome_options = Options()
        if headless:
            self.chrome_options.add_argument("--headless")
        else:
            self.chrome_options.add_argument("--start-maximized")
            
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        
        self.service = Service(executable_path=driver_location)  # Replace with the path to your chromedriver
        self.driver = None

    def open_browser(self, url: str=None) -> None:
        """Open a browser and navigate to the given URL."""
        if not self.driver:
            self.driver = webdriver.Chrome(service=self.service, options=self.chrome_options)
        self.driver.implicitly_wait(10)
        if url:
            self.driver.get(url)
        
    def close_browser(self) -> None:
        """Close the browser."""
        if self.driver:
            self.driver.quit()
            self.driver = None

    def wait_for_completion(self, timeout: int=30) -> None:
        """Wait for the given amount of time."""
        sleep_time = 2
        # time.sleep(sleep_time) # wait for at least 2 seconds when this method is called
        
        load_time = 0
        while load_time <= timeout:
            if self.driver.execute_script("return document.readyState") == "complete":
                break
            time.sleep(sleep_time)
            load_time = load_time + sleep_time
            
    def navigate_to_url(self, url: str) -> None:
        """Navigate to the given URL in the current browser session."""
        self.driver.get(url)
        self.wait_for_completion()
        
    def click_element_by_xpath(self, xpath: str) -> None:
        """Click an element on the page using the given XPath selector."""
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
        self.wait_for_completion()
        
    def click_element_by_name(self, name: str) -> None:
        """Click an element on the page using the given name selector."""
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.NAME, name))).click()
        self.wait_for_completion()
        
    def check_if_element_exists(self, xpath: str) -> bool:
        """Check if an element exists on the page using the given XPath selector."""
        return bool(self.driver.find_elements(By.XPATH, xpath))
    
    def get_element(self, xpath: str=None, name: str=None, id: str=None, tag: str=None) -> WebElement:
        """Get an element on the page using the given XPath selector."""
        if xpath:
            element = self.driver.find_element(By.XPATH, xpath)
        elif name:
            element = self.driver.find_element(By.NAME, name)
        elif id:
            element = self.driver.find_element(By.ID, id)
        elif tag:
            element = self.driver.find_element(By.TAG_NAME, tag)
        else:
            raise ValueError("No selector provided.")
            
        return element
    
    def get_elements(self, xpath: str=None, name: str=None, id: str=None, tag: str=None) -> list:
        """Get all elements on the page using the given XPath selector."""
        elements = []
        
        if xpath:
            elements = self.driver.find_elements(By.XPATH, xpath)
        elif name:
            elements = self.driver.find_elements(By.NAME, name)
        elif id:
            elements = self.driver.find_elements(By.ID, id)
        elif tag:
            elements = self.driver.find_elements(By.TAG_NAME, tag)
        else:
            raise ValueError("No selector provided.")
            
        return elements
    
    def send_text_to_element(self, text: str, xpath: str=None, name: str=None, id: str=None) -> None:
        """Send keys to an element on the page using the given name selector."""
        element = self.get_element(xpath, name, id)
        element.send_keys(text)