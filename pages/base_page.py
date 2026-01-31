import logging
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.logger = logging.getLogger(self.__class__.__name__)

    def open_url(self, url):
        start_time = time.time()
    
        self.driver.get(url)
        self.logger.info(f"Opened URL: {url}")
    
        try:
            WebDriverWait(self.driver, 3).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, ".loading, .spinner"))
        )
        except TimeoutException:
            self.logger.warning("Loading indicators not dismissed within timeout.")
            
    
    
        elapsed = time.time() - start_time
        self.logger.info(f"✓ Page fully loaded in {elapsed:.2f}s")
        self.driver.save_screenshot("load_page.png")

    def find(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def click(self, locator):
        
        try:
            self.wait.until(EC.element_to_be_clickable(locator)).click()
            self.logger.info("Clicked element: %s", locator)
        except TimeoutException:
            self.logger.info("Element not clickable: %s", locator)

    def enter_text(self, locator, text):
        element = self.find(locator)
        element.clear()
        try:
            element.send_keys(text)
            self.logger.info(f"Entering text '{text}' into element: {locator}")
        except Exception as e:
            self.logger.warning(f"Standard send_keys failed for {locator}, trying JavaScript. Error: {e}")
             

    def swipe_down(self, times=2, ):
        """
        Scrolls the window vertically.
        Requirement: 'scroll down 2 times'
        """
        for _ in range(times):
            self.driver.execute_script("window.scrollBy(0, window.innerHeight );")
            self.logger.info(f"Scrolled down  pixels.")
             
            time.sleep(0.5)  # Allow UI to settle (critical for mobile scrolling)
            
   
    def popup_handler(self, popup_locator, accept_locator):
        """
        Generic popup handler.
        Checks for popup presence and clicks accept if found.
        """
        try:
            
            popup_accept = self.wait.until(EC.element_to_be_clickable(accept_locator))
            if  popup_accept.is_displayed():
                self.logger.info("Popup detected, attempting to accept.")
                
                self.click(accept_locator)

            try:
                self.wait.until(EC.invisibility_of_element(popup_locator))
                self.logger.info("✓ Popup confirmed dismissed.")
            except TimeoutException:
                self.logger.error("✗ Popup still visible after click!")
                self.driver.save_screenshot("popup_stuck.png")

            else:
                self.logger.info("Popup not displayed.")  
                return False
            
            
        except TimeoutException:
            self.logger.info("No popup detected.")  

       
    def wait_for_page_to_load(self, timeout=3):
        """
        Waits for the page to load by checking for the absence of loading indicators.
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, ".loading, .spinner"))
            )
            self.logger.info("✓ Page loaded successfully.")
        except TimeoutException:
            self.logger.error("✗ Page did not load within the timeout period.")
                


    def is_in_viewport(self,element):
        return self.driver.execute_script("""
        const element = arguments[0];
        const rect = element.getBoundingClientRect();
        const windowHeight = window.innerHeight || document.documentElement.clientHeight;
        const windowWidth = window.innerWidth || document.documentElement.clientWidth;
        
        return (rect.top >= 0) && (rect.bottom <= windowHeight) && 
               (rect.left >= 0) && (rect.right <= windowWidth);
        """, element)