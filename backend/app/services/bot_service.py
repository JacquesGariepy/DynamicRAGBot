import uuid
from app.models.bot import Bot
from app import db
from app.utils.web_scraper import WebScraper

class BotService:
    def __init__(self):
        self.web_scraper = WebScraper()

    def create_bot(self, user_id, name, config):
        new_bot = Bot(id=str(uuid.uuid4()), name=name, config=config, owner_id=user_id)
        db.session.add(new_bot)
        db.session.commit()
        return new_bot

    def start_bot(self, bot):
        bot.status = 'running'
        db.session.commit()
        self._run_bot(bot)

    def stop_bot(self, bot):
        bot.status = 'stopped'
        db.session.commit()

    def _run_bot(self, bot):
        if 'urls' in bot.config:
            for url in bot.config['urls']:
                content = self.web_scraper.scrape(url)
                # Process and store the scraped content
                # This could involve calling the RAG service to index the content
                pass

    def update_bot_config(self, bot, new_config):
        bot.config.update(new_config)
        db.session.commit()