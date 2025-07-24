import time

# In-memory storage for demonstration
url_store = {}

def save_url_mapping(short_code, original_url):
    url_store[short_code] = {
        "original_url": original_url,
        "created_at": time.time(),
        "clicks": 0
    }

def get_url_mapping(short_code):
    return url_store.get(short_code)

def increment_click(short_code):
    if short_code in url_store:
        url_store[short_code]["clicks"] += 1

def short_code_exists(short_code):
    return short_code in url_store