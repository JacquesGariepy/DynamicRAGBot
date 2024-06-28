import os
import requests
import logging
import time
import random
import git
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from queue import PriorityQueue, Empty
from typing import Set, Dict, Any
import tempfile
from pdfminer.high_level import extract_text as extract_pdf_text
from docx import Document

logger = logging.getLogger(__name__)

class DynamicBot:
    def __init__(self, bot_id: str, rag_system):
        self.bot_id = bot_id
        self.rag_system = rag_system
        self.task_queue = PriorityQueue()
        self.visited_urls: Set[str] = set()
        self.visited_paths: Set[str] = set()
        self.MAX_RETRIES = 3
        self.COOLDOWN_TIME = 5  # secondes
        self.running = True

    def add_task(self, task: Dict[str, Any], priority: int = 1):
        if task['type'] == 'web' and task['url'] not in self.visited_urls:
            self.task_queue.put((priority, task))
            self.visited_urls.add(task['url'])
        elif task['type'] in ['repository', 'file_system', 'database', 'api'] and task['path'] not in self.visited_paths:
            self.task_queue.put((priority, task))
            self.visited_paths.add(task['path'])

    def scrape_web(self, url: str):
        for attempt in range(self.MAX_RETRIES):
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')

                title = soup.title.string if soup.title else "No title"
                content = soup.get_text(separator='\n', strip=True)
                
                if self.filter_content(content):
                    self.rag_system.insert_data(url, title, content, 'web')
                    logger.info(f"Bot {self.bot_id}: Scraped web page: {url}")

                    for link in soup.find_all('a', href=True):
                        next_url = urljoin(url, link['href'])
                        if self.is_valid_url(next_url):
                            self.add_task({'type': 'web', 'url': next_url})

                break
            except requests.RequestException as e:
                logger.error(f"Bot {self.bot_id}: Error scraping {url}: {e}")
                if attempt < self.MAX_RETRIES - 1:
                    time.sleep(self.COOLDOWN_TIME)
                else:
                    logger.error(f"Bot {self.bot_id}: Failed to scrape {url} after {self.MAX_RETRIES} attempts")

    # Ajoutez ici les méthodes pour scrape_repository, scrape_file_system, etc.

    def is_valid_url(self, url: str) -> bool:
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)

    def filter_content(self, content: str) -> bool:
        return len(content) > 100

    def run(self):
        while self.running:
            try:
                _, task = self.task_queue.get(timeout=1)
                if task['type'] == 'web':
                    self.scrape_web(task['url'])
                # Ajoutez ici les autres types de tâches
                self.task_queue.task_done()
            except Empty:
                continue
            except Exception as e:
                logger.error(f"Bot {self.bot_id}: Error in worker: {e}")

    def stop(self):
        logger.info(f"Bot {self.bot_id}: Stopping...")
        self.running = False

    def get_status(self):
        return {
            "bot_id": self.bot_id,
            "queue_size": self.task_queue.qsize(),
            "visited_urls": len(self.visited_urls),
            "visited_paths": len(self.visited_paths),
            "running": self.running
        }
