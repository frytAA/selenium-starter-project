"""
A class to handle browser automation using Selenium.
"""
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


class BrowserAutomation:
    """
    A class to handle browser automation using Selenium.
    """

    def __init__(self, headless=False):
        """
        Initialize the browser automation with Chrome.
        
        Args:
            headless (bool): Whether to run the browser in headless mode
        """
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        
        # Add additional options for stability
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        # Initialize the Chrome driver
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )

    def navigate_to(self, url):
        """
        Navigate to a specific URL.
        
        Args:
            url (str): The URL to navigate to
        """
        self.driver.get(url)
        return self

    def find_element(self, by, value, timeout=10):
        """
        Find an element on the page with waiting.
        
        Args:
            by (By): The method to locate the element
            value (str): The value to search for
            timeout (int): The maximum time to wait for the element
            
        Returns:
            WebElement: The found element
        """
        element = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        return element

    def click_element(self, by, value, timeout=10):
        """
        Click on an element.
        
        Args:
            by (By): The method to locate the element
            value (str): The value to search for
            timeout (int): The maximum time to wait for the element
        """
        element = self.find_element(by, value, timeout)
        element.click()
        return self

    def input_text(self, by, value, text, timeout=10):
        """
        Input text into a field.
        
        Args:
            by (By): The method to locate the element
            value (str): The value to search for
            text (str): The text to input
            timeout (int): The maximum time to wait for the element
        """
        element = self.find_element(by, value, timeout)
        element.clear()
        element.send_keys(text)
        return self

    def get_text(self, by, value, timeout=10):
        """
        Get text from an element.
        
        Args:
            by (By): The method to locate the element
            value (str): The value to search for
            timeout (int): The maximum time to wait for the element
            
        Returns:
            str: The text content of the element
        """
        element = self.find_element(by, value, timeout)
        return element.text

    def take_screenshot(self, filename="screenshot.png"):
        """
        Take a screenshot of the current page.
        
        Args:
            filename (str): The filename to save the screenshot as
        """
        self.driver.save_screenshot(filename)
        return self

    def close(self):
        """
        Close the browser and end the session.
        """
        if self.driver:
            self.driver.quit()