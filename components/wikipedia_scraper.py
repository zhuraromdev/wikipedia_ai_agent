from typing import List, Tuple
from selenium import webdriver
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager

from components.instructions import Instruction


class WikipediaScraper:
    """
    A class to interact with the Wikipedia website and scrape information.

    Attributes:
        options (ChromeOptions): Options for configuring the Chrome browser.
        service (ChromeService): Service for managing Chrome browser.
        driver (WebDriver): WebDriver instance for controlling the browser.
        wait (WebDriverWait): WebDriverWait instance for waiting for elements to load.
    """

    def __init__(self) -> None:
        """
        Initializes the WikipediaScraper with required configurations.
        """
        self.options = ChromeOptions()
        self.service = ChromeService(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        self.wait = WebDriverWait(self.driver, 10)

    def execute_instruction(self, instruction: Instruction):
        """
        Executes a single instruction.

        Args:
            instruction (Instruction): Instruction object containing details of action, target element, and input data.

        Raises:
            TimeoutException: If the operation times out while waiting for an element.
            NoSuchElementException: If the target element is not found.
            Exception: For other unexpected errors during instruction execution.
        """
        try:
            if instruction.action_type == "navigate":
                self.driver.get(instruction.input_data)
            elif instruction.action_type == "click":
                if instruction.target_element["by"] == "class_name":
                    element = self.wait.until(
                        EC.element_to_be_clickable((By.CLASS_NAME, instruction.target_element["value"])))
                else:
                    element = self.wait.until(EC.element_to_be_clickable(
                        (getattr(By, instruction.target_element["by"].upper()), instruction.target_element["value"])))
                element.click()
            elif instruction.action_type == "input":
                element = self.wait.until(EC.element_to_be_clickable(
                    (getattr(By, instruction.target_element["by"].upper()), instruction.target_element["value"])))
                element.clear()
                element.send_keys(instruction.input_data)
        except TimeoutException as e:
            print(f"Timeout occurred while executing instruction: {instruction.action_type}. Error: {e}")
        except NoSuchElementException as e:
            print(f"Element not found while executing instruction: {instruction.action_type}. Error: {e}")
        except Exception as e:
            print(f"An error occurred while executing instruction: {instruction.action_type}. Error: {e}")

    def execute_instructions(self, instructions: List[Instruction]):
        """
        Executes a list of instructions sequentially.

        Args:
            instructions (List[Instruction]): List of Instruction objects to be executed.
        """
        for instruction in instructions:
            self.execute_instruction(instruction)

    def search_wikipedia(self, query: str) -> Tuple[bool, str]:
        """
        Searches Wikipedia for the given query.

        Args:
            query (str): The search query.

        Returns:
            Tuple[bool, str]: A tuple containing a boolean flag indicating if the search was successful and the URL of the search result page.
        """
        try:
            self.driver.get("https://www.wikipedia.org/")
            english_link = self.wait.until(EC.element_to_be_clickable((By.ID, "js-link-box-en")))
            english_link.click()

            search_box = self.wait.until(EC.element_to_be_clickable((By.NAME, "search")))
            search_box.clear()
            search_box.send_keys(query)

            search_button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "cdx-button.cdx-search-input__end-button")))
            search_button.click()
        except Exception as e:
            print(f"An error occurred: {e}")
            return False, ""
        return True, self.driver.current_url

    def get_article_links(self) -> List[str]:
        """
        Retrieves a list of article links from the search result page.

        Returns:
            List[str]: A list of URLs of the search result articles.
        """
        links = []
        try:
            self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".mw-search-results")))
            search_results = self.driver.find_elements(By.CSS_SELECTOR, ".mw-search-results li a")[:5]  # Adjust the number as needed
            links = [result.get_attribute('href') for result in search_results]
        except Exception as e:
            print(f"An error occurred while trying to get article links: {e}")
        return links

    def get_article_info(self, url: str) -> Tuple[str, List[str]]:
        """
        Retrieves the title and paragraphs of the article from the given URL.

        Args:
            url (str): The URL of the Wikipedia article.

        Returns:
            Tuple[str, List[str]]: A tuple containing the title of the article and a list of paragraphs in the article.
        """
        try:
            self.driver.get(url)
            heading = self.wait.until(EC.presence_of_element_located((By.ID, "firstHeading"))).text
            paragraphs = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#mw-content-text p")))
            text = [paragraph.text for paragraph in paragraphs]
            return heading, text
        except TimeoutException:
            print("Timed out waiting for elements to load.")
        except NoSuchElementException as e:
            print(f"Element not found: {e}")
        except Exception as e:
            print(f"An error occurred while trying to extract article info from {url}: {e}")
        return "", []
