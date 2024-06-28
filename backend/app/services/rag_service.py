from sentence_transformers import SentenceTransformer
import litellm
from app.services.vector_store import VectorStore
import os

class RAGService:
    def __init__(self):
        self.model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
        self.vector_store = VectorStore()
        litellm.api_key = os.getenv('OPENAI_API_KEY')
        litellm.set_verbose = True

    def add_document(self, content, metadata=None):
        embedding = self.model.encode(content)
        self.vector_store.add_document(content, metadata, embedding)

    def query(self, question):
        query_vector = self.model.encode(question)
        results = self.vector_store.search(query_vector, limit=3)
        context = " ".join([hit.payload['content'] for hit in results])
        
        response = litellm.completion(
            model="gpt-3.5-turbo",  # You can change this to other models
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Context: {context}\n\nQuestion: {question}\nAnswer:"}
            ]
        )
        return response.choices[0].message.content.strip()

    def delete_document(self, document_id):
        self.vector_store.delete_document(document_id)