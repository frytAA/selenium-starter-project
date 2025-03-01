"""
Page objects for Google search functionality.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pages.base_page import BasePage


class GoogleHomePage(BasePage):
    """
    Page object for Google home page.
    """
    # Locators
    SEARCH_INPUT = (By.NAME, "q")
    SEARCH_BUTTON = (By.NAME, "btnK")
    COOKIE_ACCEPT_BUTTON = (By.ID, "L2AGLb")
    GOOGLE_APPS_BUTTON = (By.CSS_SELECTOR, "a.gb_d")
    
    def __init__(self, browser):
        """
        Initialize the Google home page.
        
        Args:
            browser (BrowserAutomation): The browser automation instance
        """
        super().__init__(browser)
        self.url = "https://www.google.com"
        
    def open(self):
        """
        Open the Google home page.
        
        Returns:
            GoogleHomePage: The page object
        """
        self.browser.navigate_to(self.url)
        return self
    
    def accept_cookies(self):
        """
        Accept cookies if the dialog appears.
        
        Returns:
            GoogleHomePage: The page object
        """
        try:
            self.browser.click_element(*self.COOKIE_ACCEPT_BUTTON, timeout=5)
        except:
            # No cookie dialog, that's fine
            pass
        return self
    
    def search(self, query):
        """
        Perform a search.
        
        Args:
            query (str): The search query
            
        Returns:
            GoogleSearchResultsPage: The search results page
        """
        self.browser.input_text(*self.SEARCH_INPUT, query)
        
        # Try clicking the search button first
        try:
            self.browser.click_element(*self.SEARCH_BUTTON, timeout=5)
        except:
            # If button click fails, press Enter instead
            self.browser.find_element(*self.SEARCH_INPUT).send_keys(Keys.RETURN)
            
        return GoogleSearchResultsPage(self.browser)


class GoogleSearchResultsPage(BasePage):
    """
    Page object for Google search results page.
    """
    # Locators
    RESULTS_STATS = (By.ID, "result-stats")
    SEARCH_INPUT = (By.NAME, "q")
    SEARCH_BUTTON = (By.NAME, "btnK")
    RESULTS_LINKS = (By.CSS_SELECTOR, "div.g h3")
    
    # CAPTCHA detection
    CAPTCHA_CONTAINER = (By.ID, "captcha-form")
    CAPTCHA_HEADING = (By.XPATH, "//h1[contains(text(), 'unusual traffic') or contains(text(), 'verify') or contains(text(), 'CAPTCHA')]")
    
    def is_captcha_present(self):
        """
        Check if CAPTCHA challenge is present.
        
        Returns:
            bool: True if CAPTCHA is detected, False otherwise
        """
        try:
            # Try both common CAPTCHA identifiers
            self.browser.find_element(*self.CAPTCHA_CONTAINER, timeout=3)
            return True
        except:
            try:
                self.browser.find_element(*self.CAPTCHA_HEADING, timeout=3)
                return True
            except:
                return False
    
    def get_result_stats(self):
        """
        Get the search results stats text.
        
        Returns:
            str: The results stats text or None if CAPTCHA is present
        """
        if self.is_captcha_present():
            return None
            
        try:
            stats = self.browser.find_element(*self.RESULTS_STATS)
            return stats.text
        except:
            return None
    
    def get_search_query(self):
        """
        Get the current search query from the input field.
        
        Returns:
            str: The search query
        """
        search_input = self.browser.find_element(*self.SEARCH_INPUT)
        return search_input.get_attribute("value")
    
    def get_results_links(self):
        """
        Get all result links.
        
        Returns:
            list: List of link elements
        """
        return self.browser.find_elements(*self.RESULTS_LINKS)
    
    def click_result(self, index=0):
        """
        Click on a search result by index.
        
        Args:
            index (int): The index of the result to click (0-based)
            
        Returns:
            BasePage: A generic page object after clicking
        """
        results = self.get_results_links()
        if index < len(results):
            results[index].click()
            return BasePage(self.browser)
        else:
            raise IndexError(f"Result index {index} out of range (0-{len(results)-1})")