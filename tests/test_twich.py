import pytest
from pages.twitch_page import TwitchHomePage
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import StaleElementReferenceException
import random

from tests.conftest import driver


@pytest.mark.repeat(10)
def test_twitch_mobile_search_flow(driver):
    """
    Test Case:
    1. Go to Twitch
    2. Click search icon
    3. Input StarCraft II
    4. Scroll down 2 times
    5. Select one streamer
    """
    twitch = TwitchHomePage(driver)

    # 1. Go to Twitch
    twitch.navigate_to_twitch()
    # Allow page to load fully
    twitch.handle_popup()

    # 2 Click search icon
    twitch.perform_click(twitch.SEARCH_ICON)

    # 3. Enter Text "StarCraft II" and click search

    twitch.enter_text(twitch.SEARCH_INPUT, "StarCraft II")
    # Allow suggestions to load

    # Select first Suggestion from list
    twitch.perform_click(twitch.STARCRAFT_II_OPTION)
    twitch.wait_for_page_to_load()

    # 4. Scroll down 2 times
    twitch.scroll_page(times=2)

    #
    # 5. Select a streamer
    # Find all streamer cards
    # Get all streamer links
    streamers = driver.find_elements(*twitch.RANDOM_STREAMER_CARD)

    # Filter only visible and enabled elements
    visible_streamers = [
        s
        for s in streamers
        if s.is_displayed() and s.is_enabled() and twitch.is_in_viewport(s)
    ]

    if visible_streamers:
        # Try clicking a random visible streamer
        for attempt in range(len(visible_streamers)):
            random_streamer = random.choice(visible_streamers)
            try:
                twitch.perform_click(random_streamer)
                twitch.wait_for_page_to_load()
                driver.save_screenshot("streamer_selected.png")
                break  # success
            except (StaleElementReferenceException, ElementClickInterceptedException):
                # Remove this one and try another
                visible_streamers.remove(random_streamer)
    else:
        twitch.logger.warning("No visible/clickable streamers found!")
