# Selenium Starter Project with UV

A starter project for browser automation using Selenium WebDriver with Python and UV as the package manager. This project follows best practices for Selenium automation and provides a foundation for building test suites.

## Features

- Browser automation using Selenium WebDriver
- Chrome driver management with webdriver-manager
- Example tests with pytest
- UV package management
- Structured test organization with conftest.py
- Automatic screenshot capturing on test failures
- Centralized logging system for debugging
- HTML report generation
- Page object pattern implementation

## Prerequisites

- Python 3.8 or higher
- Chrome browser installed
- UV package manager (recommended)

## Setup with UV

1. Install UV if you haven't already:

```bash
curl -sSf https://astral.sh/uv/install.sh | sh
```

2. Clone this repository:

```bash
git clone https://github.com/yourusername/selenium-starter.git
cd selenium-starter
```

3. Create a virtual environment and install dependencies:

```bash
uv venv
source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
uv pip install -e .
uv pip install -e ".[test]"  # Install test dependencies
```

## Setup with traditional pip

If you prefer to use pip instead of UV:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
pip install -r requirements.txt
```

## Project Structure

```
selenium-starter-project/
│
├── src/
│   ├── __init__.py
│   ├── browser_automation.py   # Enhanced browser automation class with multi-browser support
│   ├── config_manager.py       # Configuration management for different environments
│   └── pages/                  # Page Object Model implementations
│       ├── __init__.py
│       ├── base_page.py        # Base class for all page objects
│       └── google_pages.py     # Google-specific page objects
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py             # Pytest fixtures and configuration with multi-browser support
│   ├── test_google_search.py   # Example test case
│   ├── test_with_page_objects.py # Example using Page Object Model
│   │
│   ├── reports/                # Store test execution reports
│   │   └── .gitkeep
│   │
│   ├── screenshots/            # Save screenshots on test failures
│   │   └── .gitkeep
│   │
│   └── logs/                   # Centralized logging for debugging
│       └── .gitkeep
│
├── config.json                 # Environment-specific configuration
├── Dockerfile                  # Docker configuration for containerized testing
├── docker-compose.yml          # Docker Compose setup for easier test execution
├── requirements.txt            # Dependencies for pip
├── pyproject.toml              # Project metadata and dependencies for UV
├── README.md                   # Project documentation
└── .gitignore                  # Files to ignore in version control
```

## Running Tests

Run the example test with pytest:

```bash
pytest tests/test_google_search.py -v
```

Run tests in headless mode:

```bash
HEADLESS=True pytest tests/test_google_search.py -v
```

Run only smoke tests:

```bash
pytest -m smoke -v
```

Generate an HTML report (automatically saved to reports/ directory):

```bash
pytest tests/test_google_search.py
```

View logs in the `tests/logs/` directory and screenshots of failures in the `tests/screenshots/` directory.

## Parallel Test Execution

To improve test execution speed, this project supports running tests in parallel using pytest-xdist:

### Setup

1. Install pytest-xdist:

```bash
# With UV
uv pip install pytest-xdist

# With pip
pip install pytest-xdist
```

2. Verify the dependency is present in your `pyproject.toml`:

```toml
[project.optional-dependencies]
test = [
    "pytest>=7.4.3",
    "pytest-html>=4.1.1",
    "pytest-xdist>=3.3.1",
]
```

### Running Tests in Parallel

Run tests with multiple processes:

```bash
# Run with 4 parallel processes
pytest tests/ -n 4

# Run with auto-detection of CPU cores
pytest tests/ -n auto

# Run specific test file in parallel
pytest tests/test_google_search.py -n 2
```

### Considerations for Parallel Testing

- Ensure your tests are independent and don't share state
- Use unique filenames for screenshots and reports
- Don't hard-code resource names that could conflict
- Consider using pytest fixtures with 'function' scope
- If using a real browser (non-headless), be aware of screen real estate

### Debugging Parallel Tests

When a test fails during parallel execution, you can rerun it in isolation:

```bash
# Rerun a specific failing test in regular mode
pytest tests/test_google_search.py::test_google_search -v
```

The HTML reports and screenshots will help trace issues that only appear during parallel execution.


## Usage Examples

The `BrowserAutomation` class provides a simplified interface for common Selenium operations:

```python
from browser_automation import BrowserAutomation
from selenium.webdriver.common.by import By

# Initialize the browser
browser = BrowserAutomation(headless=False)

try:
    # Navigate to a website
    browser.navigate_to("https://www.example.com")
    
    # Click a button
    browser.click_element(By.ID, "submit-button")
    
    # Fill a form field
    browser.input_text(By.NAME, "username", "testuser")
    
    # Get text from an element
    text = browser.get_text(By.CLASS_NAME, "message")
    print(f"Message: {text}")
    
    # Take a screenshot
    browser.take_screenshot("example.png")
    
finally:
    # Always close the browser when done
    browser.close()
```

## Customization

- Modify `browser_automation.py` to add more functionality as needed
- Create new test files in the `tests` directory following the example
- Extend the Page Object pattern for your specific application

## Best Practices

- Always use explicit waits instead of `time.sleep()`
- Close the browser after each test with `tearDown()` or `finally` blocks
- Take screenshots on test failures for debugging
- Use appropriate locators (IDs and names are more reliable than XPaths)
- Keep tests independent and isolated from each other

## License

This project is licensed under the MIT License - see the LICENSE file for details.