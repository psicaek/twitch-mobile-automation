"""
Centralized locator repository.
Separates locators from page logic for better maintainability.
"""

from selenium.webdriver.common.by import By


class TwitchLocators:
    """All locators for Twitch pages"""

    # Navigation
    SEARCH_ICON = (By.CSS_SELECTOR, 'a[href="/directory"]')

    # Search
    SEARCH_INPUT = (By.CSS_SELECTOR, 'input[data-a-target="tw-input"]')
    SEARCH_SUGGESTION = (By.CSS_SELECTOR, 'a[href^="/directory/category"]')

    # Content
    STREAMER_CARD = (By.CSS_SELECTOR, "article a[href$='/home'].tw-link")

    # Popups
    COOKIE_BANNER = (By.CSS_SELECTOR, 'div[data-a-target="consent-banner"]')
    COOKIE_ACCEPT = (By.CSS_SELECTOR, 'button[data-a-target="consent-banner-accept"]')
    MATURE_WARNING = (
        By.CSS_SELECTOR,
        'button[data-a-target="content-classification-gate-overlay-start-watching-button"]',
    )


class BaseLocators:
    """Generic locators used across pages"""

    LOADING_SPINNER = (By.CSS_SELECTOR, ".loading, .spinner")
    SKELETON_LOADER = (By.CSS_SELECTOR, '[class*="skeleton"]')
