import requests
import requests_cache
from bs4 import BeautifulSoup
from hashlib import md5
import os
url="https://www.jumia.com.ng/catalog/?q=phone"


def generate_cached_name(url):
    return f"cached_{md5(url.encode('utf-8')).hexdigest()}"



def initialize_scraper_api(url):
    cache_name = generate_cached_name(url)
    requests_cache.install_cache(cache_name, expire_after=86400)
    payload = {
        "api_key": os.getenv("API_KEY"),
        "url":url
    }
    
    response = requests.get(
        'https://api.scraperapi.com/', params=payload
    )
    return response






