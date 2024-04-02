from selenium import webdriver
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import warnings
from urllib3.exceptions import InsecureRequestWarning

warnings.filterwarnings("ignore", category=InsecureRequestWarning)

# Setup Chrome options and service
options = ChromeOptions()
service = ChromeService(ChromeDriverManager().install())

# Initialize the WebDriver
driver = webdriver.Chrome(service=service, options=options)

# Navigate to Wikipedia and click on the English link
driver.get("https://www.wikipedia.org/")
english_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "js-link-box-en")))
english_link.click()


def search_wikipedia(query):
    try:
        search_box = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "search"))
        )
        search_box.clear()
        search_box.send_keys(query)

        # Locate the search button and click it
        search_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "cdx-button.cdx-search-input__end-button"))
        )
        search_button.click()

    except Exception as e:
        print(f"An error occurred: {e}")
        return False, None
    return True, driver.current_url


def get_article_links():
    links = []
    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".mw-search-results"))
        )
        search_results = driver.find_elements(By.CSS_SELECTOR, ".mw-search-results li a")[:5]  # Adjust the number as needed
        links = [result.get_attribute('href') for result in search_results]
    except Exception as e:
        print(f"An error occurred while trying to get article links: {e}")
    return links


def get_article_info(url):
    try:
        driver.get(url)
        heading = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "firstHeading"))
        ).text
        paragraphs = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#mw-content-text p"))
        )
        text = [paragraph.text for paragraph in paragraphs]
        return heading, text

    except TimeoutException:
        print("Timed out waiting for elements to load.")
    except NoSuchElementException as e:
        print(f"Element not found: {e}")
    except Exception as e:
        print(f"An error occurred while trying to extract article info from {url}: {e}")
    return None, None


from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import gensim.downloader as api

# Load pre-trained word embeddings
"""
Overall, by using the glove-wiki-gigaword-100 model, we can leverage the rich semantic information captured in the pre-trained word embeddings to enhance various natural language processing tasks, including information retrieval, question answering, and text generation.
"""
word_vectors = api.load("glove-wiki-gigaword-100")


# Function to convert text to embeddings
def text_to_embeddings(text):
    words = text.split()
    embeddings = [word_vectors[word] for word in words if word in word_vectors.key_to_index]
    return np.mean(embeddings, axis=0) if embeddings else np.zeros(word_vectors.vector_size)


# Function to calculate cosine similarity between two vectors
def calculate_cosine_similarity(vec1, vec2):
    return cosine_similarity([vec1], [vec2])[0][0]


# query = "most common species of Canadian ducks"
# query = "Roman Empire"
# query = 'When was born Elon Musk?'
query = 'War in Ukraine 2022'
# query = 'Tell me which companies CEO is Elon Musk?'

# Extract article information (title and paragraphs)
is_searched, url = search_wikipedia(query)
if is_searched:
    article_links = get_article_links()
    all_paragraphs = []

    # If we have an exact article
    if not article_links:
        title, paragraphs = get_article_info(url)

        print(f'Title: {title}')
        print(f'Paragraphs: {paragraphs}')

    # more articles
    else:

        # Collect paragraphs from all articles
        for url in article_links:
            title, paragraphs = get_article_info(url)
            all_paragraphs.extend(paragraphs)

        # Convert user query and all paragraphs to embeddings
        query_embedding = text_to_embeddings(query)
        paragraph_embeddings = [text_to_embeddings(paragraph) for paragraph in all_paragraphs]

        # Calculate cosine similarity between user query and each paragraph
        similarity_scores = [calculate_cosine_similarity(query_embedding, emb) for emb in paragraph_embeddings]

        # Find the index of the paragraph with the highest similarity score
        most_similar_index = np.argmax(similarity_scores)

        # Print the most similar answer
        print(f"Most Similar Paragraph: {all_paragraphs[most_similar_index]}\n")

# Close the browser
driver.quit()
