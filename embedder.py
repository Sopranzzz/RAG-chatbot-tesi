from langchain_huggingface import HuggingFaceEmbeddings

class Embedder:
    def __init__(self, model_name):
        self.embedding_model = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs={"device": "cuda"},
            encode_kwargs={"device": "cuda", "batch_size": 100}
        )

    def embed_chunks(self, chunks):
        texts = [chunk["text"] for chunk in chunks]
        embeddings = self.embedding_model.embed_documents(texts)
        for chunk, embedding in zip(chunks, embeddings):
            chunk["embedding"] = embedding
        return chunks