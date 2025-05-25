import hashlib
from pydantic import HttpUrl

class UrlShortner:
    def __init__(self, length: int = 6):
        self.length = length

    def generate_short(self, http_url: HttpUrl) -> str:
        url = str(http_url)
        hash_object = hashlib.sha256(url.encode())
        short_code = hash_object.hexdigest()[:self.length]
        return short_code