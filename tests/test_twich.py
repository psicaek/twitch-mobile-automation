from pages.twitch_page import TwitchHomePage


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
        twitch.SEARCH_ICON, "Search icon should be clickable before clicking"
    )
    twitch.perform_click(twitch.SEARCH_ICON)
    twitch.assert_search_opened()

    # 3. Enter Text "StarCraft II" and click search

    # ASSERTION before action: Input should be visible and enabled
    search_input = twitch.assert_element_visible(
        twitch.SEARCH_INPUT, "Search input should be visible before typing"
    )
    assert search_input.is_enabled(), "Search input should be enabled"

    twitch.enter_text(twitch.SEARCH_INPUT, "StarCraft II")
    # Allow suggestions to load
    twitch.assert_element_visible(
        twitch.STARCRAFT_II_OPTION,
        f"Search suggestions should appear for 'StarCraft II'",
    )

    # Select first Suggestion from list
    twitch.perform_click(twitch.STARCRAFT_II_OPTION)
    twitch.wait_for_page_to_load()

    # 4. Scroll down 2 times
    initial_count = twitch.assert_search_results_loaded("StarCraft II")
    driver.save_screenshot("03_before_scroll.png")

    current_count = initial_count
    for i in range(2):
        twitch.scroll_page(times=1)
        current_count = twitch.assert_more_content_after_scroll(current_count)
        driver.save_screenshot(f"04_after_scroll_{i+1}.png")

    #
    # 5. Select a streamer
    streamer_selected = twitch.select_random_streamer()
    assert streamer_selected, "Failed to select any streamer after multiple attempts"
    twitch.assert_on_streamer_page()
