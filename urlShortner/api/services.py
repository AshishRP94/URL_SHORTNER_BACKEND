import random
import string
import logging
from .repositories import URLRepository

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

class ShorteningStrategy:
    def generate_code(self):
        raise NotImplementedError

class RandomStringStrategy(ShorteningStrategy):
    def generate_code(self, length=6):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

class URLShortenerService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(URLShortenerService, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, strategy=None):
        if not hasattr(self, 'initialized'): 
            self.strategy = strategy or RandomStringStrategy()
            self.repository = URLRepository()
            self.initialized = True

    def shorten_url(self, original_url):
        try:
            short_url = self.strategy.generate_code()
            return self.repository.create_url(original_url, short_url)
        except Exception as e:
            logger.error(f"An error occurred while shortening the long URL: {e}")
            return None
    
    def get_short_by_long_url(self, original_url):
        try:
            url = self.repository.get_short_by_long_url(original_url)
            if url:
                return url.short_url
            return None
        except Exception as e:
            logger.error(f"An error occurred while getting the short URL by long URL: {e}")
            return None

    def resolve_url(self, short_url):
        try:
            url = self.repository.get_by_short_url(short_url)
            if url:
                return url.original_url
            return None
        except Exception as e:
            logger.error(f"An error occurred while resolving the short URL: {e}")
            return None
