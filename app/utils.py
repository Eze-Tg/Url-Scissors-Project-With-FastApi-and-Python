# app/utils.py

import re
import hashlib

def is_valid_url(url: str) -> bool:
    regex = re.compile(
        r"^(?:http|ftp)s?://"  # http:// or https://
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"  # domain...
        r"localhost|"  # localhost...
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or IP
        r"(?::\d+)?"  # optional port
        r"(?:/?|[/?]\S+)$", re.IGNORECASE
    )
    return re.match(regex, url) is not None

def generate_short_url(long_url: str, custom_alias: str = None) -> str:
    url_hash = hashlib.sha256(long_url.encode()).hexdigest()[:10]
    if custom_alias:
        return f"http://yourcustomdomain.com/{custom_alias}"
    else:
        return f"http://yourcustomdomain.com/{url_hash}"
