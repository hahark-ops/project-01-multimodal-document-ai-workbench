import hashlib
import math
import re

TOKEN_PATTERN = re.compile(r"[A-Za-z0-9']+")
EMBEDDING_SIZE = 256


def _tokenize(text: str) -> list[str]:
    return [token.lower() for token in TOKEN_PATTERN.findall(text)]


def embed_text(text: str, *, dimensions: int = EMBEDDING_SIZE) -> list[float]:
    vector = [0.0] * dimensions

    for token in _tokenize(text):
        digest = hashlib.blake2b(token.encode("utf-8"), digest_size=8).digest()
        index = int.from_bytes(digest[:4], "big") % dimensions
        sign = 1.0 if digest[4] % 2 == 0 else -1.0
        vector[index] += sign

    norm = math.sqrt(sum(value * value for value in vector))
    if norm == 0:
        return vector

    return [value / norm for value in vector]
