import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pages.base_page import BasePage
from selenium.common.exceptions import (
    StaleElementReferenceException,
    ElementClickInterceptedException,
    TimeoutException,
)
from selenium.webdriver.support import expected_conditions as EC
from utils.config import Config, Messages
from utils.Twitch_locators import TwitchLocators


class TwitchHomePage(BasePage):
    # --- Locators ---
    SEARCH_ICON = TwitchLocators.SEARCH_ICON
    SEARCH_INPUT = TwitchLocators.SEARCH_INPUT
    STARCRAFT_II_OPTION = TwitchLocators.SEARCH_SUGGESTION
    RANDOM_STREAMER_CARD = TwitchLocators.STREAMER_CARD

    COOKIE_BANNER = TwitchLocators.COOKIE_BANNER
    COOKIE_ACCEPT = TwitchLocators.COOKIE_ACCEPT
    MATURE_WARNING = TwitchLocators.MATURE_WARNING

    def navigate_to_twitch(self):

        self.open_url(Config.TWITCH_URL)

    def handle_popup(self):
        self.popup_handler(self.COOKIE_BANNER, self.COOKIE_ACCEPT)

    def perform_click(self, locator):
        self.click(locator)

    def enter_text_in_field(self, locator, text):
        self.enter_text(locator, text)

    def scroll_page(self, times=2):
        return self.swipe_down(times)

    def select_random_streamer(self):
        """Returns True if streamer successfully selected"""
        streamers = self.driver.find_elements(*self.RANDOM_STREAMER_CARD)
        visible = [s for s in streamers if s.is_displayed() and self.is_in_viewport(s)]

        for streamer in visible:
            try:
                self.perform_click(streamer)
                self.wait_for_page_to_load()
                self.handle_mature_content_popup()
                self.driver.save_screenshot(Config.SCREENSHOT_STREAMER)

                return True
            except (StaleElementReferenceException, ElementClickInterceptedException):
                continue
        return False

    # Assertion Methods

    def assert_on_home_page(self):
        """Verify we're on Twitch home page"""
        self.assert_url_contains("twitch.tv", Messages.URL_TWITCH_DOMAIN)
        self.assert_element_visible(self.SEARCH_ICON, Messages.SEARCH_ICON_VISIBLE)
        self.logger.info(Messages.HOME_PAGE_SUCCESS)

    def assert_search_opened(self):
        """Verify search interface is open"""
        self.assert_element_visible(self.SEARCH_INPUT, Messages.SEARCH_INPUT_VISIBLE)
        search_input = self.driver.find_element(*self.SEARCH_INPUT)
        assert search_input.is_enabled(), Messages.SEARCH_INPUT_ENABLED
        self.logger.info(Messages.SEARCH_OPENED_SUCCESS)

    def assert_search_results_loaded(self, search_term):
        """Verify search results page loaded with content"""
        # Check URL contains search context
        self.assert_url_contains("/directory", Messages.URL_DIRECTORY_PAGE)

        # Verify streamer cards are present
        streamers = self.assert_element_count_greater_than(
            self.RANDOM_STREAMER_CARD,
            1,
            f"Should have at least 1 streamer card for '{search_term}'",
        )

        self.logger.info(f"✓ Search results loaded: {len(streamers)} streamers found")
        return len(streamers)

    def assert_more_content_after_scroll(self, initial_count):
        """Verify additional content loaded after scrolling"""
        current_streamers = self.driver.find_elements(*self.RANDOM_STREAMER_CARD)
        current_count = len(current_streamers)

        assert (
            current_count >= initial_count
        ), f"Expected more streamers after scroll. Before: {initial_count}, After: {current_count}"

        self.logger.info(
            f"✓ More content loaded: {initial_count} -> {current_count} streamers"
        )
        return current_count

    def assert_on_streamer_page(self):
        """Verify we're on an individual streamer's page"""
        current_url = self.driver.current_url

        # URL should be deeper than /directory (e.g., /username or /username/video)
        url_parts = [part for part in current_url.split("/") if part]
        assert (
            len(url_parts) >= 3
        ), f"Should be on streamer page, but URL is too short: {current_url}"

        # Should NOT still be on directory page
        assert (
            "/directory" not in current_url
        ), "Should have navigated away from directory page"

        self.logger.info(f"✓ Successfully on streamer page: {current_url}")

    def get_visible_streamers(self):
        """Get list of visible, clickable streamers with assertions"""
        all_streamers = self.driver.find_elements(*self.RANDOM_STREAMER_CARD)

        visible_streamers = [
            s
            for s in all_streamers
            if s.is_displayed() and s.is_enabled() and self.is_in_viewport(s)
        ]

        assert (
            len(visible_streamers) > 0
        ), f"No visible streamers found. Total elements: {len(all_streamers)}"

        self.logger.info(
            f"✓ Found {len(visible_streamers)} visible/clickable streamers"
        )
        return visible_streamers

    def handle_mature_content_popup(self):
        """Handle mature content warning that some streamers show"""
        try:
            mature_button = self.wait.until(
                EC.element_to_be_clickable(self.MATURE_WARNING)
            )
            self.logger.info(Messages.MATURE_DETECTED)
            mature_button.click()
            self.logger.info(Messages.MATURE_POPUP_HANDLED)
        except TimeoutException:
            self.logger.info(Messages.MATURE_POPUP_NOT_PRESENT)
