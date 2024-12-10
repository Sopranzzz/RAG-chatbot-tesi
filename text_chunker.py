from langchain.text_splitter import RecursiveCharacterTextSplitter

class TextChunker:
    def __init__(self, chunk_size=300, chunk_overlap=40):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            separators=["\n\n", "\n", " ", ""],
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len
        )

    def chunk_section(self, section):
        chunks = []
        for page in section["content"]:
            page_text = page["text"]
            page_number = page["page_number"]
            page_chunks = self.text_splitter.create_documents(
                texts=[page_text],
                metadatas=[{
                    "source": section["path"],
                    "page_number": page_number
                }]
            )
            for chunk in page_chunks:
                chunks.append({
                    "text": chunk.page_content,
                    "source": chunk.metadata["source"],
                    "page_number": chunk.metadata["page_number"]
                })
        return chunks