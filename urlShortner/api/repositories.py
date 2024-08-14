from .models import URL

class URLRepository:
    def get_by_short_url(self, short_url):
        return URL.objects.filter(short_url=short_url).first()
    
    def get_short_by_long_url(self, original_url):
        return URL.objects.filter(original_url=original_url).first()

    def create_url(self, original_url, short_url, expiration_date=None):
        return URL.objects.create(
            original_url=original_url,
            short_url=short_url,
            expiration_date=expiration_date
        )