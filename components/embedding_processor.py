import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import gensim.downloader as api


class EmbeddingProcessor:
    """
    A class for processing text embeddings using pre-trained word vectors.

    Attributes:
        word_vectors: Pre-trained word vectors loaded from the GloVe model.
    """

    def __init__(self) -> None:
        """
        Initializes the EmbeddingProcessor with pre-trained word vectors.
        """
        self.word_vectors = api.load("glove-wiki-gigaword-100")

    def text_to_embeddings(self, text: str) -> np.ndarray:
        """
        Converts text into word embeddings and calculates the average embedding.

        Args:
            text (str): The input text.

        Returns:
            np.ndarray: The mean embedding of the input text.
        """
        words = text.split()
        embeddings = [self.word_vectors[word] for word in words if word in self.word_vectors.key_to_index]
        return np.mean(embeddings, axis=0) if embeddings else np.zeros(self.word_vectors.vector_size)

    @staticmethod
    def calculate_cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
        """
        Calculates the cosine similarity between two vectors.

        Args:
            vec1 (np.ndarray): The first vector.
            vec2 (np.ndarray): The second vector.

        Returns:
            float: The cosine similarity between the two vectors.
        """
        return cosine_similarity([vec1], [vec2])[0][0]
