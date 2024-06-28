from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from app.models.document import Document
from app import db
import numpy as np

class VectorStore:
    def __init__(self, collection_name="documents"):
        self.client = QdrantClient("localhost", port=6333)
        self.collection_name = collection_name
        self._ensure_collection_exists()

    def _ensure_collection_exists(self):
        collections = self.client.get_collections().collections
        if self.collection_name not in [c.name for c in collections]:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=768, distance=Distance.COSINE),
            )

    def add_document(self, content, metadata, embedding):
        document = Document(content=content, metadata=metadata, embedding=embedding)
        db.session.add(document)
        db.session.commit()

        self.client.upsert(
            collection_name=self.collection_name,
            points=[PointStruct(
                id=document.id,
                vector=embedding.tolist(),
                payload={'content': content, 'metadata': metadata}
            )]
        )

    def search(self, query_vector, limit=5):
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector.tolist(),
            limit=limit
        )
        return results

    def delete_document(self, document_id):
        document = Document.query.get(document_id)
        if document:
            db.session.delete(document)
            db.session.commit()
            self.client.delete(
                collection_name=self.collection_name,
                points_selector=[document_id]
            )