from pages.twitch_page import TwitchHomePage
from utils.config import Config, Messages
from tests.conftest import driver


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
    twitch.assert_on_home_page()

    # Handle Cookie Popup
    twitch.handle_popup()

    # 2 Click search icon
    twitch.assert_element_clickable(
        twitch.SEARCH_ICON,
    )
    twitch.perform_click(twitch.SEARCH_ICON)
    twitch.assert_search_opened()

    # 3. Enter Text "StarCraft II" and click search

    # ASSERTION before action: Input should be visible and enabled
    search_input = twitch.assert_element_visible(
        twitch.SEARCH_INPUT, Messages.SEARCH_INPUT_VISIBLE
    )
    assert search_input.is_enabled(), Messages.SEARCH_INPUT_ENABLED

    twitch.enter_text(twitch.SEARCH_INPUT, Config.STARCRAFT_SEARCH_TERM)
    # Allow suggestions to load
    twitch.assert_element_visible(
        twitch.STARCRAFT_II_OPTION,
        Messages.SEARCH_SUGGESTIONS_APPEAR.format(Config.STARCRAFT_SEARCH_TERM),
    )

    # Select first Suggestion from list
    twitch.perform_click(twitch.STARCRAFT_II_OPTION)
    twitch.wait_for_page_to_load()

    # 4. Scroll down 2 times
    initial_count = twitch.assert_search_results_loaded(Config.STARCRAFT_SEARCH_TERM)
    driver.save_screenshot(Config.SCREENSHOT_BEFORE_SCROLL)

    current_count = initial_count
    for i in range(2):
        twitch.scroll_page(times=1)
        current_count = twitch.assert_more_content_after_scroll(current_count)
        driver.save_screenshot(Config.SCREENSHOT_AFTER_SCROLL.format(i + 1))

    #
    # 5. Select a streamer
    streamer_selected = twitch.select_random_streamer()
    assert streamer_selected, Messages.STREAMER_SELECTION_FAILED
    twitch.assert_on_streamer_page()
