import faiss
import numpy as np

class Indexer:
    def __init__(self, dimension):
        self.index = faiss.IndexFlatL2(dimension)

    def add_embeddings(self, embeddings):
        self.index.add(embeddings)

    def search(self, query_embedding, top_k=3):
        D, I = self.index.search(query_embedding, top_k)
        return I[0]