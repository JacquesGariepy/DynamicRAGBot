import logging
from logging.handlers import RotatingFileHandler
import json
from flask import request
from pythonjsonlogger import jsonlogger

class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get('timestamp'):
            log_record['timestamp'] = record.created
        if flask.has_request_context():
            log_record['ip'] = request.remote_addr
            log_record['user_agent'] = request.user_agent.string
        log_record['level'] = record.levelname

def setup_logger(name, log_file, level=logging.INFO, max_bytes=10000000, backup_count=10):
    handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
    formatter = CustomJsonFormatter('%(timestamp)s %(level)s %(name)s %(message)s')
    handler.setFormatter(formatter)
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    
    return logger

# Usage
app_logger = setup_logger('app', 'logs/app.log')
bot_logger = setup_logger('bot', 'logs/bot.log')