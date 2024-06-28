import requests
from bs4 import BeautifulSoup
from app.utils.logger import setup_logger

logger = setup_logger('web_scraper', 'logs/web_scraper.log')

class WebScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'RAGBotManager WebScraper 1.0'
        })

    def scrape(self, url):
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract text from paragraphs
            paragraphs = soup.find_all('p')
            content = ' '.join([p.get_text() for p in paragraphs])
            
            logger.info(f"Successfully scraped {url}")
            return content
        except requests.RequestException as e:
            logger.error(f"Error scraping {url}: {str(e)}")
            return None