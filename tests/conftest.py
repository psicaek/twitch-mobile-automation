import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="function")
def driver():
    """
    Initializes Chrome with Mobile Emulation enabled.
    """
    mobile_emulation = {"deviceName": "iPhone 14 Pro Max"}

    options = webdriver.ChromeOptions()
    options.add_experimental_option("mobileEmulation", mobile_emulation)

    # Block notifications to reduce flakiness
    prefs = {"profile.default_content_setting_values.notifications": 2}
    options.add_experimental_option("prefs", prefs)
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    # Initialize Driver - Simplified approach
    try:
        # Try webdriver-manager first
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
    except Exception as e:
        print(f"webdriver-manager failed: {e}")
        print("Attempting to use system ChromeDriver...")
        # Fallback to system-installed ChromeDriver
        driver = webdriver.Chrome(options=options)

    driver.implicitly_wait(5)  # Soft wait as backup

    yield driver

    driver.quit()
