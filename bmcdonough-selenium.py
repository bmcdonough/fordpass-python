#!/usr/bin/env python3
import logging
import logging.handlers
import os

from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

MY_URL = "ford.com"
TEXT_TO_FIND = "sign"  # Adjust the text you're searching for

def config_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(filename)s[%(process)d] - [%(name)s:%(lineno)d] :: (%(funcName)s) %(levelname)s - %(message)s",
        handlers=[logging.handlers.SysLogHandler(address="/dev/log", facility="user")],
    )
    return logging.getLogger(__name__)

def find_link_with_text(driver, text):
    """Uses Selenium to navigate to the URL and find an link containing the text."""
    # Find all links using a generic tag selector (adjust based on website structure)
    links = driver.find_elements(By.TAG_NAME, "a")

    # Extract and print the link text (visible text) and href attribute (URL)
    for link in links:
        link_text = link.get_attribute('text').strip().lower()  # Remove leading/trailing whitespaces

        if text in link_text:
            _LOGGER.info(f"link found containing '{text}': href='{link.get_attribute('href')}' text='{link.get_attribute('text')}'")
            return(link.get_attribute('href'))  # Exit the loop after finding the first link (adjust if needed)

        # No link found containing the text
    _LOGGER.warn(f"No link found containing the text '{text}'.")
    print(f"No link found containing the text '{text}'.")
    return None


def main():
    try:
        # Get the path to the downloaded ChromeDriver
        chromedriver_path = ChromeDriverManager().install()

        ua = UserAgent()
        userAgent = ua.random
        print(userAgent)

        service = Service(chromedriver_path)
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument(f'user-agent={userAgent}')
#        options.add_argument("--no-sandbox")
#        options.add_argument("--disable-gpu")
#        options.add_argument("--disable-extensions")

        # Check if path exists
        if not os.path.exists(chromedriver_path):
            raise Exception("ChromeDriver download failed!")

        # Use the path to create a new Chrome WebDriver
        driver = webdriver.Chrome(service=service, options=options)

        url = MY_URL
        if not url.startswith("http"):
            url = f"https://{url}"
        driver.get(url)

        link_url = find_link_with_text(driver, TEXT_TO_FIND)
        if link_url:
            print(link_url)
            driver.get(link_url)

        driver.quit()
        return 0  # Indicate successful execution
    except Exception as e:
        print(f"An error occurred: {e}")
        return 1  # Indicate error

if __name__ == "__main__":
    _LOGGER = config_logging()
    exit_code = main()
    if exit_code == 0:
        print("Main completed successfully.")
    else:
        print("Main failed to complete.")