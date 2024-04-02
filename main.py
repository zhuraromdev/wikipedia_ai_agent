# query = 'What is SpaceX?'
# query = "most common species of Canadian ducks"
# query = "Roman Empire"
# query = 'When was born Elon Musk?'
# query = "the most common species of Canadian ducks?"
# query = 'War in Ukraine 2022'
# query = 'Tell me which companies CEO is Elon Musk?'

import numpy as np

from components.embedding_processor import EmbeddingProcessor
from components.wikipedia_scraper import WikipediaScraper


def main():
    scraper = WikipediaScraper()
    processor = EmbeddingProcessor()

    query = input("Enter your query: ")

    is_searched, url = scraper.search_wikipedia(query)
    if is_searched:
        article_links = scraper.get_article_links()
        all_paragraphs = []

        # If no article links found, extract information from the main article
        if not article_links:
            title, paragraphs = scraper.get_article_info(url)

            print(f'Title: {title}')
            print(f'Paragraphs: {paragraphs}')

        else:
            # Extracting information from all linked articles
            for url in article_links:
                title, paragraphs = scraper.get_article_info(url)
                all_paragraphs.extend(paragraphs)

            query_embedding = processor.text_to_embeddings(query)
            paragraph_embeddings = [processor.text_to_embeddings(paragraph) for paragraph in all_paragraphs]

            similarity_scores = [processor.calculate_cosine_similarity(query_embedding, emb) for emb in paragraph_embeddings]
            most_similar_index = np.argmax(similarity_scores)

            print(f"Most Similar Paragraph: {all_paragraphs[most_similar_index]}\n")

    scraper.driver.quit()


if __name__ == "__main__":
    main()

