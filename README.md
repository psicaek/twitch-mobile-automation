# Twitch Mobile Automation Framework

A scalable Selenium-based test automation framework for Twitch mobile web application, built with Python and Pytest using the Page Object Model design pattern.

### Key Components

- **BasePage**: Contains reusable methods for all pages (waits, assertions, interactions)
- **TwitchHomePage**: Twitch-specific methods and locators
- **Config**: Centralized configuration (URLs, timeouts, test data)
- **Locators**: Separated locator definitions for maintainability
- **Messages**: Consistent assertion and log messages

### Prerequisites

- Python 3.8 or higher
- Google Chrome browser (latest version)
- pip (Python package manager)

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/YOUR_USERNAME/twitch-selenium-framework.git
   cd twitch-selenium-framework

   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv

   # Activate on Windows

   venv\Scripts\activate

   # Activate on Mac/Linux

   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run all tests**

   ```bash
     pytest tests/test_twich.py -v
   ```

## Test Scenario

This framework automates the following test case on Twitch mobile:

1.  Navigate to Twitch homepage
2.  Click on the search icon
3.  Search for "StarCraft II"
4.  Scroll down 2 times to load more content
5.  Select a random streamer from results

**All steps include assertions to validate expected behavior.**
