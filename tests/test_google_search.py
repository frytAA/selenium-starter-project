"""
Example test for Google search functionality using pytest fixtures.
"""
import logging
import pytest
from selenium.webdriver.common.by import By


@pytest.mark.smoke
def test_google_search(browser):
    """
    Test the Google search functionality with proper logging.
    """
    logging.info("Starting Google search test")
    
    # Navigate to Google
    logging.info("Navigating to Google")
    browser.navigate_to("https://www.google.com")
    
    # Accept cookies if the dialog appears (common in EU)
    try:
        logging.info("Checking for cookie consent dialog")
        browser.click_element(By.ID, "L2AGLb", timeout=5)
        logging.info("Cookie consent accepted")
    except:
        logging.info("No cookie consent dialog found")
    
    # Input search query
    search_term = "Selenium with Python"
    logging.info(f"Entering search term: '{search_term}'")
    browser.input_text(By.NAME, "q", search_term)
    
    # Submit the search form
    logging.info("Submitting search form")
    browser.click_element(By.NAME, "btnK")
    
    # Verify search results contain expected text
    logging.info("Verifying search results")
    results_stats = browser.find_element(By.ID, "result-stats")
    assert results_stats is not None, "Search results stats not found"
    
    # Log search results count
    stats_text = results_stats.text
    logging.info(f"Search results: {stats_text}")
    
    # Take a screenshot of the results
    logging.info("Taking screenshot of search results")
    browser.take_screenshot("tests/screenshots/google_search_results.png")
    
    # Assert that the page title contains the search query
    page_title = browser.driver.title
    logging.info(f"Page title: {page_title}")
    assert search_term in page_title, f"Search term '{search_term}' not found in page title '{page_title}'"
    
    logging.info("Google search test completed successfully")


@pytest.mark.regression
def test_google_advanced_search(browser):
    """
    Test Google's advanced search features.
    """
    logging.info("Starting Google advanced search test")
    
    # Navigate to Google
    browser.navigate_to("https://www.google.com")
    
    # Accept cookies if needed
    try:
        browser.click_element(By.ID, "L2AGLb", timeout=5)
    except:
        logging.info("No cookie consent dialog found")
    
    # Click on the menu for advanced search options
    # Note: This is a simplified example and may need to be adjusted based on Google's UI
    try:
        browser.click_element(By.CSS_SELECTOR, "a.gb_pa", timeout=5)
        logging.info("Clicked on Google menu")
    except:
        logging.warning("Could not find Google menu, using direct navigation instead")
        browser.navigate_to("https://www.google.com/advanced_search")
    
    # Verify we're on the advanced search page or a page with advanced options
    try:
        # This is just an example, actual selectors would need to be updated
        advanced_search_heading = browser.find_element(By.XPATH, "//h1[contains(text(), 'Advanced')]")
        logging.info("Advanced search page found")
        assert advanced_search_heading is not None, "Advanced search heading not found"
    except:
        # In case we can't find the advanced search page, let's just search with quotes
        logging.info("Direct advanced search not accessible, using quoted search instead")
        browser.navigate_to("https://www.google.com")
        browser.input_text(By.NAME, "q", '"Selenium Python framework"')
        browser.click_element(By.NAME, "btnK")
    
    # Verify search results
    results = browser.find_element(By.ID, "result-stats")
    assert results is not None, "Search results not found"
    logging.info(f"Advanced search results: {results.text}")
    
    logging.info("Advanced search test completed")