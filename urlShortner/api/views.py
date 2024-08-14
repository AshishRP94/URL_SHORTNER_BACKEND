import logging
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views import View
from .services import URLShortenerService
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt
from traceback import format_exc

# Set up logging
logger = logging.getLogger(__name__)

@csrf_exempt
def shorten_url(request):
    if request.method == "POST":
        try:
            original_url = request.POST.get('url')
            if not original_url:
                return HttpResponse("URL not provided", status=400)
            
            cache_key = f"shortened_url_{original_url}"
            shortened_url = cache.get(cache_key)
            if not shortened_url:
                service = URLShortenerService()
                shortened_url = service.get_short_by_long_url(original_url)
                if shortened_url:
                    return HttpResponse(f"Shortened URL: {shortened_url}")
                
                shortened_url = service.shorten_url(original_url)
                cache.set(cache_key, shortened_url, 60 * 15) 
            
            return HttpResponse(f"Shortened URL: {shortened_url.__getattribute__('short_url')}")
        
        except Exception as e:
            logger.error(f"An error occurred while shortening the URL: {str(e)}\n{format_exc()}")
            return HttpResponse(f"An error occurred while shortening the URL: {str(e)}", status=500)

    return HttpResponse("Invalid HTTP method  use POST", status=405)

@csrf_exempt
def resolve_short_url(request, short_url):
    if request.method=="GET":   
        try:
            service = URLShortenerService()
            original_url = service.resolve_url(short_url)
            
            if original_url:
                return HttpResponseRedirect(original_url)
            else:
                raise Http404("Short URL not found")
        
        except Exception as e:
            logger.error(f"An error occurred while resolving the URL: {str(e)}\n{format_exc()}")
            raise Http404(f"An error occurred while resolving the URL: {str(e)}")
    
    return HttpResponse("Invalid HTTP method use GET", status=405)

