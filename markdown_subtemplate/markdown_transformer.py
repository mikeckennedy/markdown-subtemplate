import hashlib

import markdown2

# Note: Do NOT enable link-patterns, it causes a crash.
__enabled_markdown_extras = [
    "cuddled-lists",
    "code-friendly",
    "fenced-code-blocks",
    "tables"
]

__cache = dict()


def transform(text, safe_mode=True):
    if not text:
        return text

    hash_val = get_hash(text)

    if hash_val in __cache:
        return __cache[hash_val]

    html = markdown2.markdown(text, extras=__enabled_markdown_extras, safe_mode=safe_mode)

    __cache[hash_val] = html

    return html


def get_hash(text):
    md5 = hashlib.md5()
    data = text.encode('utf-8')
    md5.update(data)

    return md5.hexdigest()


def clear_cache():
    __cache.clear()
