import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from utils.config import Config


@pytest.fixture(scope="function")
def driver():
    """Initializes Chrome with Mobile Emulation enabled."""
    mobile_emulation = {"deviceName": Config.MOBILE_DEVICE}

    options = webdriver.ChromeOptions()
    options.add_experimental_option("mobileEmulation", mobile_emulation)

    # Block notifications
    prefs = {
        "profile.default_content_setting_values.notifications": Config.NOTIFICATION_SETTING
    }
    options.add_experimental_option("prefs", prefs)
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    # Initialize Driver
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
    except Exception as e:
        print(f"webdriver-manager failed: {e}")
        print("Attempting to use system ChromeDriver...")
        driver = webdriver.Chrome(options=options)

    # Set page load timeout
    # driver.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)

    yield driver

    driver.quit()
