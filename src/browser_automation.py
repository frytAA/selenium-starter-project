"""
A class to handle browser automation using Selenium with support for multiple browsers.
"""
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.safari.service import Service as SafariService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager


class BrowserAutomation:
    """
    A class to handle browser automation using Selenium with support for multiple browsers.
    """

    def __init__(self, browser_type="chrome", headless=False):
        """
        Initialize the browser automation with the specified browser.
        
        Args:
            browser_type (str): Browser type to use ('chrome', 'firefox', 'edge', 'safari')
            headless (bool): Whether to run the browser in headless mode
        """
        self.browser_type = browser_type.lower()
        self.driver = None
        
        if self.browser_type == "chrome":
            options = ChromeOptions()
            if headless:
                options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")
            
            self.driver = webdriver.Chrome(
                service=ChromeService(ChromeDriverManager().install()),
                options=options
            )
            
        elif self.browser_type == "firefox":
            options = FirefoxOptions()
            if headless:
                options.add_argument("--headless")
            
            self.driver = webdriver.Firefox(
                service=FirefoxService(GeckoDriverManager().install()),
                options=options
            )
            
        elif self.browser_type == "edge":
            options = EdgeOptions()
            if headless:
                options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--window-size=1920,1080")
            
            self.driver = webdriver.Edge(
                service=EdgeService(EdgeChromiumDriverManager().install()),
                options=options
            )
            
        elif self.browser_type == "safari":
            options = SafariOptions()
            # Safari doesn't support headless mode
            
            self.driver = webdriver.Safari(
                service=SafariService(),
                options=options
            )
            
        else:
            raise ValueError(f"Unsupported browser type: {browser_type}")
            
        # Set implicit wait as a base timing strategy
        self.driver.implicitly_wait(5)
        
        # Set page load timeout
        self.driver.set_page_load_timeout(30)

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
            
        Raises:
            TimeoutException: If element isn't found within timeout
        """
        element = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        return element
    
    def find_elements(self, by, value, timeout=10):
        """
        Find multiple elements on the page with waiting.
        
        Args:
            by (By): The method to locate the elements
            value (str): The value to search for
            timeout (int): The maximum time to wait for the elements
            
        Returns:
            list: The found elements
        """
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_all_elements_located((by, value))
        )
        return self.driver.find_elements(by, value)

    def click_element(self, by, value, timeout=10):
        """
        Click on an element.
        
        Args:
            by (By): The method to locate the element
            value (str): The value to search for
            timeout (int): The maximum time to wait for the element
        """
        element = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((by, value))
        )
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

    def wait_for_url_contains(self, text, timeout=10):
        """
        Wait for the URL to contain specific text.
        
        Args:
            text (str): The text to look for in the URL
            timeout (int): The maximum time to wait
            
        Returns:
            bool: True if the condition is met within the timeout
        """
        return WebDriverWait(self.driver, timeout).until(
            EC.url_contains(text)
        )
    
    def wait_for_element_visible(self, by, value, timeout=10):
        """
        Wait for an element to be visible.
        
        Args:
            by (By): The method to locate the element
            value (str): The value to search for
            timeout (int): The maximum time to wait
            
        Returns:
            WebElement: The visible element
        """
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located((by, value))
        )
    
    def wait_for_element_invisible(self, by, value, timeout=10):
        """
        Wait for an element to be invisible.
        
        Args:
            by (By): The method to locate the element
            value (str): The value to search for
            timeout (int): The maximum time to wait
            
        Returns:
            bool: True if the element is invisible
        """
        return WebDriverWait(self.driver, timeout).until(
            EC.invisibility_of_element_located((by, value))
        )

    def execute_script(self, script, *args):
        """
        Execute JavaScript in the browser.
        
        Args:
            script (str): The JavaScript to execute
            *args: Arguments to pass to the JavaScript
            
        Returns:
            The result of the JavaScript execution
        """
        return self.driver.execute_script(script, *args)

    def take_screenshot(self, filename="screenshot.png"):
        """
        Take a screenshot of the current page.
        
        Args:
            filename (str): The filename to save the screenshot as
        """
        self.driver.save_screenshot(filename)
        return self
    
    def get_cookies(self):
        """
        Get all cookies from the browser.
        
        Returns:
            list: All cookies
        """
        return self.driver.get_cookies()
    
    def add_cookie(self, cookie_dict):
        """
        Add a cookie to the browser.
        
        Args:
            cookie_dict (dict): The cookie to add
        """
        self.driver.add_cookie(cookie_dict)
        return self
    
    def delete_all_cookies(self):
        """
        Delete all cookies from the browser.
        """
        self.driver.delete_all_cookies()
        return self

    def close(self):
        """
        Close the browser and end the session.
        """
        if self.driver:
            self.driver.quit()