import os
import requests
import sqlite3
import logging
import time
import random
import git
import numpy as np
import faiss
import openai
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor
from queue import Queue, Empty
from typing import Set, Dict, Any, List
import signal
import tempfile
from pdfminer.high_level import extract_text as extract_pdf_text
from docx import Document
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv()

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configuration de l'API OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

class DynamicRAGBot:
    def __init__(self, db_name: str = 'dynamic_rag_bot.db'):
        self.db_name = db_name
        self.create_database()
        self.task_queue = Queue()
        self.visited_urls: Set[str] = set()
        self.visited_paths: Set[str] = set()
        self.MAX_RETRIES = 3
        self.COOLDOWN_TIME = 5  # secondes
        self.running = True
        self.model = SentenceTransformer('multi-qa-MiniLM-L6-cos-v1')
        self.index = None
        self.documents = []

    def create_database(self):
        """Créer la base de données SQLite et les tables."""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS documents
                     (id INTEGER PRIMARY KEY, source TEXT, title TEXT, content TEXT, type TEXT,
                      timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
        conn.commit()
        conn.close()

    def insert_data(self, source: str, title: str, content: str, data_type: str):
        """Insérer les données scrapées dans la base de données."""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("INSERT INTO documents (source, title, content, type) VALUES (?, ?, ?, ?)",
                  (source, title, content, data_type))
        conn.commit()
        conn.close()
        self.documents.append(content)
        self.update_index()

    def update_index(self):
        """Mettre à jour l'index FAISS avec les nouveaux documents."""
        if not self.documents:
            return
        
        embeddings = self.model.encode(self.documents, convert_to_numpy=True)
        if self.index is None:
            self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(np.array(embeddings))

    def add_task(self, task: Dict[str, Any]):
        """Ajouter une tâche à la file d'attente."""
        if task['type'] == 'web' and task['url'] not in self.visited_urls:
            self.task_queue.put(task)
            self.visited_urls.add(task['url'])
        elif task['type'] in ['repository', 'file_system'] and task['path'] not in self.visited_paths:
            self.task_queue.put(task)
            self.visited_paths.add(task['path'])

    def scrape_web(self, url: str):
        """Scraper une page web et extraire les liens."""
        for attempt in range(self.MAX_RETRIES):
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')

                title = soup.title.string if soup.title else "No title"
                content = soup.get_text(separator='\n', strip=True)
                self.insert_data(url, title, content, 'web')
                logger.info(f"Scraped web page: {url}")

                # Extraire et ajouter les nouveaux liens à la file d'attente
                for link in soup.find_all('a', href=True):
                    next_url = urljoin(url, link['href'])
                    if self.is_valid_url(next_url):
                        self.add_task({'type': 'web', 'url': next_url})

                break  # Sortir de la boucle si le scraping a réussi
            except requests.RequestException as e:
                logger.error(f"Error scraping {url}: {e}")
                if attempt < self.MAX_RETRIES - 1:
                    time.sleep(self.COOLDOWN_TIME)  # Attendre avant de réessayer
                else:
                    logger.error(f"Failed to scrape {url} after {self.MAX_RETRIES} attempts")

    def scrape_repository(self, repo_url: str):
        """Cloner et scraper un dépôt Git."""
        with tempfile.TemporaryDirectory() as tmpdirname:
            try:
                repo = git.Repo.clone_from(repo_url, tmpdirname)
                logger.info(f"Cloned repository: {repo_url}")

                for root, _, files in os.walk(tmpdirname):
                    for file in files:
                        file_path = os.path.join(root, file)
                        self.scrape_file(file_path, 'repository')

                        # Ajouter des tâches pour les sous-répertoires
                        if os.path.isdir(file_path):
                            self.add_task({'type': 'file_system', 'path': file_path})

            except git.GitCommandError as e:
                logger.error(f"Error cloning repository {repo_url}: {e}")

    def scrape_file_system(self, directory: str):
        """Scraper les fichiers d'un système de fichiers local."""
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                self.scrape_file(file_path, 'file_system')

            # Ajouter des tâches pour les sous-répertoires
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                self.add_task({'type': 'file_system', 'path': dir_path})

    def scrape_file(self, file_path: str, source_type: str):
        """Scraper un fichier individuel."""
        try:
            if file_path.endswith('.pdf'):
                content = extract_pdf_text(file_path)
            elif file_path.endswith('.docx'):
                doc = Document(file_path)
                content = "\n".join([para.text for para in doc.paragraphs])
            else:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            
            self.insert_data(file_path, os.path.basename(file_path), content, source_type)
            logger.info(f"Scraped file: {file_path}")
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {e}")

    def is_valid_url(self, url: str) -> bool:
        """Vérifier si l'URL est valide et doit être scrapée."""
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)

    def worker(self):
        """Fonction de travail pour chaque thread."""
        while self.running:
            try:
                task = self.task_queue.get(timeout=1)
                if task['type'] == 'web':
                    self.scrape_web(task['url'])
                elif task['type'] == 'repository':
                    self.scrape_repository(task['url'])
                elif task['type'] == 'file_system':
                    self.scrape_file_system(task['path'])
                self.task_queue.task_done()
            except Empty:
                continue  # Continuer si la file d'attente est vide
            except Exception as e:
                logger.error(f"Error in worker: {e}")

    def run(self):
        """Exécuter le bot de manière autonome."""
        with ThreadPoolExecutor(max_workers=5) as executor:
            workers = [executor.submit(self.worker) for _ in range(5)]

            while self.running:
                # Afficher des statistiques périodiquement
                logger.info(f"Queue size: {self.task_queue.qsize()}, Visited URLs: {len(self.visited_urls)}, Visited Paths: {len(self.visited_paths)}")
                time.sleep(10)  # Attendre 10 secondes avant la prochaine mise à jour

            # Attendre que tous les workers terminent
            for worker in workers:
                worker.result()

    def stop(self):
        """Arrêter le bot."""
        logger.info("Stopping the bot...")
        self.running = False

    def search_similar_documents(self, query: str, k: int = 3) -> List[str]:
        """Rechercher les documents similaires."""
        if self.index is None or not self.documents:
            return []
        query_vector = self.model.encode([query], convert_to_numpy=True)
        D, I = self.index.search(query_vector, k)
        return [self.documents[i] for i in I[0]]

    def generate_response(self, user_question: str, similar_documents: List[str]) -> str:
        """Générer une réponse contextuelle avec GPT-4."""
        context = "\n".join(similar_documents)
        prompt = f"Voici des informations pertinentes :\n{context}\n\nQuestion utilisateur : {user_question}\nRéponse :"
        try:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=150,
                n=1,
                stop=None,
                temperature=0.7
            )
            return response.choices[0].text.strip()
        except openai.error.OpenAIError as e:
            logger.error(f"Error generating response: {e}")
            return "Je suis désolé, mais je ne peux pas générer une réponse pour le moment."

    def ask_question(self, question: str) -> str:
        """Traiter une question de l'utilisateur et générer une réponse."""
        similar_docs = self.search_similar_documents(question)
        return self.generate_response(question, similar_docs)

def signal_handler(signum, frame):
    """Gestionnaire de signal pour arrêter le bot proprement."""
    logger.info("Received stop signal. Shutting down...")
    bot.stop()

def main():
    global bot
    bot = DynamicRAGBot()

    # Configurer le gestionnaire de signal
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Ajouter quelques tâches de départ
    start_tasks = [
        {'type': 'web', 'url': "https://en.wikipedia.org/wiki/Web_scraping"},
        {'type': 'web', 'url': "https://news.ycombinator.com"},
        {'type': 'repository', 'url': "https://github.com/example/repo.git"},
        {'type': 'file_system', 'path': "./local_directory"},
    ]
    for task in start_tasks:
        bot.add_task(task)

    # Démarrer le bot dans un thread séparé
    import threading
    bot_thread = threading.Thread(target=bot.run)
    bot_thread.start()

    # Boucle principale pour les questions de l'utilisateur
    try:
        while True:
            user_question = input("Posez votre question (ou 'q' pour quitter) : ")
            if user_question.lower() == 'q':
                break
            response = bot.ask_question(user_question)
            print("Réponse :", response)
    finally:
        bot.stop()
        bot_thread.join()

if __name__ == "__main__":
    main()
