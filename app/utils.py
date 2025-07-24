import re
import random
import string

def is_valid_url(url):
    # Simple regex for URL validation
    regex = re.compile(
        r'^(https?://)?'  # http:// or https://
        r'([a-zA-Z0-9.-]+(\.[a-zA-Z]{2,}))'  # domain
        r'(:\d+)?'  # optional port
        r'(\/\S*)?$'  # path
    )
    return re.match(regex, url) is not None

def generate_short_code(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))