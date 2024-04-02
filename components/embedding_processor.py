import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import gensim.downloader as api


class EmbeddingProcessor:
    def __init__(self) -> None:
        self.word_vectors = api.load("glove-wiki-gigaword-100")

    def text_to_embeddings(self, text: str) -> np.ndarray:
        words = text.split()
        embeddings = [self.word_vectors[word] for word in words if word in self.word_vectors.key_to_index]
        return np.mean(embeddings, axis=0) if embeddings else np.zeros(self.word_vectors.vector_size)

    @staticmethod
    def calculate_cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
        return cosine_similarity([vec1], [vec2])[0][0]
