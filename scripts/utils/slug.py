import re

def slugify_name(name):
    return re.sub(r'[^a-zA-Z0-9\uAC00-\uD7A3]', '', name)