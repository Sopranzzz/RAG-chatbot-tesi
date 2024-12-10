import ray
import torch
from document_extractor import DocumentExtractor
from text_chunker import TextChunker
from embedder import Embedder
from indexer import Indexer
from responder import ResponseGenerator
import numpy as np
from langchain_huggingface import HuggingFaceEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()

# Breve controllo per assicurarsi che CUDA sia disponibile nella macchina che esegue il bot.
if not torch.cuda.is_available():
    raise EnvironmentError(
        "Errore: CUDA non è disponibile.\n"
        "Questa applicazione richiede il supporto Nvidia CUDA per funzionare correttamente.\n"
        "Verifica di avere una GPU compatibile e che i driver CUDA siano aggiornati almeno alla versione 12.4."
    )

# Inizializzazione di Ray per la paralellizzazione dei documenti.
ray.init()

EFS_DIR = r"C:\Users\marco\Downloads\slides07.pdf"

# Estrazione dei Documenti
extractor = DocumentExtractor(EFS_DIR)
documents_with_text = extractor.get_documents()

# Chunking del Testo
chunker = TextChunker(chunk_size=300, chunk_overlap=40)
chunks = []
for doc in documents_with_text:
    chunks.extend(chunker.chunk_section(doc))

# Generazione degli Embedding e Creazione dell'indice utilizzando FAISS
embedding_model_name = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
embedder = Embedder(embedding_model_name)
embedded_chunks = embedder.embed_chunks(chunks)
embeddings = np.stack([chunk['embedding'] for chunk in embedded_chunks])
dimension = embeddings.shape[1]
indexer = Indexer(dimension)
indexer.add_embeddings(embeddings)
query_embedding_model = HuggingFaceEmbeddings(
    model_name=embedding_model_name,
    model_kwargs={"device": "cuda"},
    encode_kwargs={"device": "cuda"}
)

# Funzione per cercare i chunk più rilevanti per una query
def search_query(query, top_k=3):
    query_embedding = query_embedding_model.embed_query(query)
    query_embedding = np.array([query_embedding])
    indices = indexer.search(query_embedding, top_k)
    relevant_chunks = [embedded_chunks[idx] for idx in indices]
    return relevant_chunks

# Funzione per generare la risposta
def generate_response(query, relevant_chunks):
    response = response_generator.generate_response(query, relevant_chunks)
    sources = [f"[**Pagina {chunk['page_number']}**]" for chunk in relevant_chunks]
    sources = list(dict.fromkeys(sources))
    total_chunks = len(embedded_chunks)
    chunks_text = [
        f"Chunk {embedded_chunks.index(chunk) + 1} di {total_chunks}:\n{chunk['text']}"
        for chunk in relevant_chunks
    ]
    return response, sources, chunks_text

# Generazione della Risposta
api_key = os.getenv("API_KEY")
model_name = "mistralai/Mixtral-8x7B-Instruct-v0.1"
response_generator = ResponseGenerator(api_key, model_name)

# E' possibile ottenere una risposta anche senza interfaccia grafica, qualora un utente lo volesse;
# per fare ciò, è sufficiente scrivere la domanda qui sotto.
# Sarà possibile ottenere la risposta nel terminale di VS Code
if __name__ == "__main__":
    query_text = "Quali specie animali sono tipicamente ospitate nelle foreste di faggio e abete rosso?"
    relevant_chunks = search_query(query_text)
    response, sources, chunks_text = generate_response(query_text, relevant_chunks)
    print("Risposta generata:")
    print(response)