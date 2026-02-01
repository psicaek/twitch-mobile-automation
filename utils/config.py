"""
Configuration file for test framework.
Contains all hardcoded values: URLs, timeouts, device settings, etc.
"""


class Config:
    """Base configuration"""

    # URLs
    TWITCH_URL = "https://m.twitch.tv/"

    # Mobile device
    MOBILE_DEVICE = "iPhone 14 Pro Max"

    # Browser preferences
    NOTIFICATION_SETTING = 2  # Block notifications

    # Test data
    STARCRAFT_SEARCH_TERM = "StarCraft II"

    # Screenshot names
    SCREENSHOT_HOME = "01_home_page.png"
    SCREENSHOT_BEFORE_SCROLL = "03_before_scroll.png"
    SCREENSHOT_AFTER_SCROLL = "04_after_scroll_{}.png"
    SCREENSHOT_STREAMER = "05_streamer_selected.png"


class LocatorSelectors:
    """CSS Selector patterns used in locators"""

    # Content indicators
    CONTENT_INDICATORS = [
        '[data-a-target="tw-core-button-label-text"]',
        ".tw-card",
        ".ScCoreLink-sc-16kq0mq-0",
        'img[src*="static-cdn.jtvnw.net"]',
    ]

    # Skeleton/loading indicators
    SKELETON_SELECTORS = [
        '[class*="skeleton"]',
        '[class*="loading"]',
        '[class*="ScSkeletonWrapper"]',
        ".tw-skeleton",
        '[aria-label*="Loading"]',
        '[data-a-target*="loading"]',
    ]


class Messages:
    """Assertion and log messages"""

    # URL assertions
    URL_TWITCH_DOMAIN = "Should be on Twitch domain"
    URL_DIRECTORY_PAGE = "Should be on directory/search page"

    # Element assertions
    SEARCH_ICON_VISIBLE = "Search icon should be visible on home page"

    SEARCH_INPUT_VISIBLE = "Search input should be visible before typing"
    SEARCH_INPUT_ENABLED = "Search input should be enabled"
    SEARCH_SUGGESTIONS_APPEAR = "Search suggestions should appear for '{}'"

    # Content assertions

    STREAMER_SELECTION_FAILED = "Failed to select any streamer after multiple attempts"

    # Success messages
    HOME_PAGE_SUCCESS = "✓ Successfully on Twitch home page"
    SEARCH_OPENED_SUCCESS = "✓ Search interface opened successfully"

    # Mature content popup
    MATURE_DETECTED = "Mature content warning detected."
    MATURE_POPUP_HANDLED = "✓ Mature content popup handled successfully"
    MATURE_POPUP_NOT_PRESENT = "Mature content popup not present"

    # Dom
    STABLE_DOM = "✓ DOM stable"
