import logging
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from utils.config import Config, LocatorSelectors, Messages


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.logger = logging.getLogger(self.__class__.__name__)

    def open_url(self, url):
        start_time = time.time()

        self.driver.get(url)
        self.logger.info(f"Opened URL: {url}")

        self.wait_for_page_to_load()

        elapsed = time.time() - start_time
        self.logger.info(f"✓ Page fully loaded in {elapsed:.2f}s")
        self.driver.save_screenshot(Config.SCREENSHOT_HOME)

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
            self.logger.warning(
                f"Standard send_keys failed for {locator}, trying JavaScript. Error: {e}"
            )

    def swipe_down(self, times=2, step=80, steps_per_swipe=10, delay=0.05):
        """
        Smoothly scrolls down the page.
        """

        for _ in range(times):
            for _ in range(steps_per_swipe):
                self.driver.execute_script(f"window.scrollBy(0, {step});")
                time.sleep(delay)

        self.logger.info("Completed one smooth swipe down")
        time.sleep(0.3)  # settle time

    def popup_handler(self, popup_locator, accept_locator):
        """
        Generic popup handler.
        Checks for popup presence and clicks accept if found.
        """
        try:

            popup_accept = self.wait.until(EC.element_to_be_clickable(accept_locator))
            if popup_accept.is_displayed():
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

    def wait_for_page_to_load(self):
        """
        Waits for the page to load by checking for the absence of loading indicators.
        """
        self.wait_for_dom_stable()

    def is_in_viewport(self, element):
        return self.driver.execute_script(
            """
        const element = arguments[0];
        const rect = element.getBoundingClientRect();
        const windowHeight = window.innerHeight || document.documentElement.clientHeight;
        const windowWidth = window.innerWidth || document.documentElement.clientWidth;
        
        return (rect.top >= 0) && (rect.bottom <= windowHeight) && 
               (rect.left >= 0) && (rect.right <= windowWidth);
        """,
            element,
        )

    def wait_for_network_idle(self, timeout=5):

        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.execute_script(
                    """
                return (typeof jQuery !== 'undefined') 
                    ? jQuery.active == 0 
                    : true;
                """
                )
            )
            self.logger.info("✓ Network idle (no pending requests)")
            # Small buffer for rendering
        except TimeoutException:
            self.logger.warning("Network idle timeout - proceeding anyway")

    def wait_for_document_ready(self, timeout=5):

        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.execute_script("return document.readyState")
                == "complete"
            )
            self.logger.info("✓ Document ready state: complete")
        except TimeoutException:
            self.logger.warning("Document ready state timeout")

    def wait_for_content_indicators(self, timeout=10):
        """
        Strategy 1: Wait for actual content to appear.
        More reliable than waiting for skeletons to disappear.
        """

        content_found = False
        for selector in LocatorSelectors.CONTENT_INDICATORS:
            try:
                WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
                self.logger.info(f"✓ Content loaded: {selector}")
                content_found = True
                break
            except TimeoutException:
                continue

        if not content_found:
            self.logger.warning("No content indicators found, continuing anyway")

        return content_found

    def wait_for_skeleton_loaders(self, timeout=2):
        """
        Strategy 2: Check for skeleton/loading states to disappear.
        Uses short timeout since skeletons might not exist on all pages.
        """

        for selector in LocatorSelectors.SKELETON_SELECTORS:
            try:
                WebDriverWait(self.driver, timeout).until(
                    EC.invisibility_of_element_located((By.CSS_SELECTOR, selector))
                )
                self.logger.info(f"✓ Skeleton disappeared: {selector}")
            except TimeoutException:
                # Skeletons might not exist - that's OK
                continue

    def wait_for_images_loaded(self, timeout=10):
        """
        Explicitly wait until all images are loaded.
        """

        images_loaded = self.driver.execute_script(
            """
            return Array.from(document.images)
                .filter(img => img.offsetParent !== null)
                .every(img => img.complete && img.naturalWidth > 0);
        """
        )

        try:
            WebDriverWait(self.driver, timeout, poll_frequency=1).until(images_loaded)
            self.logger.info("✓ All images fully loaded")
            return True

        except Exception:
            self.logger.warning("Timeout waiting for images")
            time.sleep(0.5)  # brief wait before proceeding
            return False

    def wait_for_dom_stable(self, timeout=15, stable_time=2):
        """
        Wait until DOM stops changing for 'stable_time' seconds.
        """

        script = """
        if (!window.__lastDOMSize) {
            window.__lastDOMSize = document.body.innerHTML.length;
            window.__stableCounter = 0;
            return false;
        }

        let currentSize = document.body.innerHTML.length;

        if (currentSize === window.__lastDOMSize) {
            window.__stableCounter++;
        } else {
            window.__stableCounter = 0;
        }

        window.__lastDOMSize = currentSize;

        return window.__stableCounter >= arguments[0];
    """

        WebDriverWait(self.driver, timeout, poll_frequency=0.5).until(
            lambda d: d.execute_script(script, stable_time)
        )

        self.logger.info(Messages.STABLE_DOM)

    # Assertion Methods

    def assert_url_contains(self, expected_text, message=None):
        """Assert current URL contains expected text"""
        current_url = self.driver.current_url
        if message is None:
            message = (
                f"Expected URL to contain '{expected_text}', but got '{current_url}'"
            )
        assert expected_text in current_url, message
        self.logger.info(f"✓ Assertion passed: URL contains '{expected_text}'")

    def assert_element_visible(self, locator, message=None):
        """Assert element is visible on page"""
        try:
            element = self.wait.until(EC.visibility_of_element_located(locator))
            if message is None:
                message = f"Element should be visible: {locator}"
            assert element.is_displayed(), message
            self.logger.info(f"✓ Assertion passed: Element visible {locator}")
            return element
        except TimeoutException:
            raise AssertionError(f"Element not found or not visible: {locator}")

    def assert_element_clickable(self, locator, message=None):
        """Assert element is clickable (visible and enabled)"""
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            if message is None:
                message = f"Element should be clickable: {locator}"
            assert element.is_enabled(), message
            self.logger.info(f"✓ Assertion passed: Element clickable {locator}")
            return element
        except TimeoutException:
            raise AssertionError(f"Element not clickable: {locator}")

    def assert_element_count_greater_than(self, locator, min_count, message=None):
        """Assert minimum number of elements present"""
        elements = self.driver.find_elements(*locator)
        if message is None:
            message = f"Expected at least {min_count} elements for {locator}, found {len(elements)}"
        assert len(elements) >= min_count, message
        self.logger.info(
            f"✓ Assertion passed: Found {len(elements)} elements (min: {min_count})"
        )
        return elements

    def assert_text_in_element(self, locator, expected_text, message=None):
        """Assert element contains expected text"""
        element = self.assert_element_visible(locator)
        actual_text = element.text
        if message is None:
            message = f"Expected '{expected_text}' in element, but got '{actual_text}'"
        assert expected_text.lower() in actual_text.lower(), message
        self.logger.info(f"✓ Assertion passed: Text '{expected_text}' found in element")
