"""
Base page object for all page objects in the framework.
"""

class BasePage:
    """
    Base class for all page objects.
    """
    
    def __init__(self, browser):
        """
        Initialize the page with a browser instance.
        
        Args:
            browser (BrowserAutomation): The browser automation instance
        """
        self.browser = browser
        
    def get_title(self):
        """
        Get the page title.
        
        Returns:
            str: The page title
        """
        return self.browser.driver.title
    
    def get_url(self):
        """
        Get the current URL.
        
        Returns:
            str: The current URL
        """
        return self.browser.driver.current_url
    
    def refresh_page(self):
        """
        Refresh the current page.
        
        Returns:
            BasePage: The current page object
        """
        self.browser.driver.refresh()
        return self
    
    def go_back(self):
        """
        Navigate back in browser history.
        
        Returns:
            BasePage: The current page object
        """
        self.browser.driver.back()
        return self
    
    def go_forward(self):
        """
        Navigate forward in browser history.
        
        Returns:
            BasePage: The current page object
        """
        self.browser.driver.forward()
        return self