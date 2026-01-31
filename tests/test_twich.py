from pages.home_page import TwitchHomePage
import time

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
    
    twitch.enter_text(twitch.SEARCH_INPUT,"StarCraft II")
      # Allow suggestions to load
    #twitch.press_enter(twitch.SEARCH_INPUT)  

     # Assuming pressing enter/clicking input triggers search  
   
    #twitch.scroll_page(times=2, pixels=400)
    
    #time.sleep(2)
    # 5. Select first streamer