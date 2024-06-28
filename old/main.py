from app import app
from rag import RAGSystem

if __name__ == '__main__':
    rag_system = RAGSystem()
    app.run(debug=True)
