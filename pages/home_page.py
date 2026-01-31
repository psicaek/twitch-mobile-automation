from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pages.base_page import BasePage
import time

class TwitchHomePage(BasePage):
    # --- Locators ---
    SEARCH_ICON = (By.CSS_SELECTOR, 'a[href="/directory"]')
    SEARCH_INPUT = (By.CSS_SELECTOR, 'input[data-a-target="tw-input"]')
    FIRST_STREAMER_CARD = (By.CSS_SELECTOR, 'div[data-a-target="video-tower-card-0"] img') 
    # Note: Selectors on Twitch mobile change frequently. 
    # Using robust attributes like href or type is safer.
    
    # Popups
    COOKIE_BANNER = (By.CSS_SELECTOR, 'div[data-a-target="consent-banner"]')
    COOKIE_ACCEPT = (By.CSS_SELECTOR, 'button[data-a-target="consent-banner-accept"]')
    MATURE_WARNING = (By.CSS_SELECTOR, 'button[data-a-target="player-overlay-mature-accept"]')

    def navigate_to_twitch(self):
    
        self.open_url("https://m.twitch.tv/")

  
        
    def handle_popup(self):
        self.popup_handler(self.COOKIE_BANNER, self.COOKIE_ACCEPT)
    

    def perform_click(self, locator):
        self.click(locator)

    def enter_text_in_field(self, locator, text):
        self.enter_text(locator, text)
         

