"""
Page objects package for Selenium automation.
"""
from pages.base_page import BasePage
from pages.google_pages import GoogleHomePage, GoogleSearchResultsPage

__all__ = ["BasePage", "GoogleHomePage", "GoogleSearchResultsPage"]