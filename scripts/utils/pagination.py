import math

def paginate(items, per_page):
    total_pages = math.ceil(len(items) / per_page)

    def get_page(page):
        start = (page - 1) * per_page
        end = start + per_page
        return items[start:end]

    return total_pages, get_page