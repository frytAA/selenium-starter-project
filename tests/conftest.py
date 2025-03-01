"""
Pytest configuration file with fixtures and hooks for multiple browsers.
"""
import os
import logging
import pytest
from datetime import datetime
from pathlib import Path

# Import the BrowserAutomation class
from src.browser_automation import BrowserAutomation


# Set up logging
def setup_logging():
    """Configure logging for tests."""
    log_dir = Path("tests/logs")
    log_dir.mkdir(exist_ok=True, parents=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_dir / f"test_run_{timestamp}.log"
    
    # Configure root logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # Create file handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


# Initialize logging before tests start
@pytest.fixture(scope="session", autouse=True)
def initialize_logging():
    """Initialize logging for the test session."""
    logger = setup_logging()
    logger.info("Test session started")
    yield logger
    logger.info("Test session ended")


def pytest_addoption(parser):
    """Add command line options to pytest."""
    parser.addoption(
        "--browser", 
        default="chrome", 
        help="Browser to run tests on: chrome, firefox, edge, or safari"
    )
    parser.addoption(
        "--headless", 
        action="store_true", 
        default=False,
        help="Run browser in headless mode"
    )


@pytest.fixture(scope="function")
def browser(request):
    """
    Provide a browser instance for each test.
    
    Returns:
        BrowserAutomation: A browser automation instance
    """
    # Get browser type from command line or environment variable
    browser_type = request.config.getoption("--browser")
    browser_env = os.environ.get("BROWSER", "").lower()
    if browser_env:
        browser_type = browser_env
    
    # Get headless mode from command line or environment variable
    headless = request.config.getoption("--headless")
    headless_env = os.environ.get("HEADLESS", "").lower() == "true"
    if headless_env:
        headless = True
    
    # Log browser details
    logging.info(f"Creating {browser_type} browser instance (headless={headless})")
    
    # Create browser instance
    try:
        browser_instance = BrowserAutomation(browser_type=browser_type, headless=headless)
        logging.info(f"{browser_type.capitalize()} browser instance created successfully")
    except Exception as e:
        logging.error(f"Failed to create {browser_type} browser instance: {e}")
        raise
    
    # Provide the browser to the test
    yield browser_instance
    
    # Cleanup after test
    browser_instance.close()
    logging.info(f"{browser_type.capitalize()} browser instance closed")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Take screenshot when a test fails.
    
    Args:
        item: Test item
        call: Test call info
    """
    # Execute all other hooks to obtain the report object
    outcome = yield
    report = outcome.get_result()
    
    # We only care about the call phase of a test (setup/call/teardown)
    if report.when == "call" and report.failed:
        # Check if a browser fixture is available
        browser_fixture = item.funcargs.get("browser", None)
        if browser_fixture:
            try:
                # Create screenshots directory if it doesn't exist
                screenshot_dir = Path("tests/screenshots")
                screenshot_dir.mkdir(exist_ok=True, parents=True)
                
                # Generate a unique filename
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                test_name = item.name
                browser_type = browser_fixture.browser_type.lower()
                screenshot_path = str(screenshot_dir / f"fail_{test_name}_{browser_type}_{timestamp}.png")
                
                # Take screenshot
                browser_fixture.take_screenshot(screenshot_path)
                logging.info(f"Screenshot saved at {screenshot_path}")
                
                # Attach screenshot to the report
                if hasattr(item.config, "_html"):
                    # Include screenshot in HTML report if pytest-html is used
                    html = '<div><img src="%s" alt="screenshot" style="width:600px;height:auto;" ' \
                           'onclick="window.open(this.src)" align="right"/></div>' % screenshot_path
                    extra = getattr(report, 'extra', [])
                    extra.append(pytest.html.extras.html(html))
                    report.extra = extra
            except Exception as e:
                logging.error(f"Failed to take screenshot: {e}")


def pytest_configure(config):
    """
    Configure test reports directory.
    
    Args:
        config: Pytest configuration object
    """
    # Create reports directory if it doesn't exist
    Path("tests/reports").mkdir(exist_ok=True, parents=True)
    
    # Set up HTML report if pytest-html plugin is available
    if hasattr(config, "_html"):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        browser_type = config.getoption("--browser", "chrome")
        config._html.report_title = f"Selenium Test Report - {browser_type.capitalize()}"
        config._html.logfile = f"tests/reports/report_{browser_type}_{timestamp}.html"