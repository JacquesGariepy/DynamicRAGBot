from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
import litellm
import os
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class RAGSystem:
    def __init__(self, db_name: str = 'rag_system'):
        self.db_name = db_name
        self.model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
        self.qdrant_client = QdrantClient("localhost", port=6333)
        self.create_collection()
        litellm.api_key = os.getenv('OPENAI_API_KEY')

    def create_collection(self):
        self.qdrant_client.recreate_collection(
            collection_name=self.db_name,
            vectors_config=VectorParams(size=768, distance=Distance.COSINE),
        )

    def insert_data(self, source: str, title: str, content: str, data_type: str):
        vector = self.model.encode(content)
        self.qdrant_client.upsert(
            collection_name=self.db_name,
            points=[{
                'id': hash(source + title),
                'payload': {
                    'source': source,
                    'title': title,
                    'content': content,
                    'type': data_type
                },
                'vector': vector.tolist()
            }]
        )

    def search_similar_documents(self, query: str, k: int = 3) -> List[Dict]:
        vector = self.model.encode(query)
        results = self.qdrant_client.search(
            collection_name=self.db_name,
            query_vector=vector.tolist(),
            limit=k
        )
        return [hit.payload for hit in results]

    def generate_response(self, user_question: str, similar_documents: List[Dict]) -> str:
        context = "\n".join([doc['content'] for doc in similar_documents])
        prompt = f"Voici des informations pertinentes :\n{context}\n\nQuestion utilisateur : {user_question}\nRéponse :"
        try:
            response = litellm.completion(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=150
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "Je suis désolé, mais je ne peux pas générer une réponse pour le moment."

    def ask_question(self, question: str) -> str:
        similar_docs = self.search_similar_documents(question)
        return self.generate_response(question, similar_docs)
