import math

def paginate(items, per_page):
    total_pages = math.ceil(len(items) / per_page)

    def get_page(page):
        start = (page - 1) * per_page
        end = start + per_page
        return items[start:end]

    return total_pages, get_page

def generate_pagination_links(current_page, total_pages, base_path):
    links = []
    for i in range(1, total_pages + 1):
        if i == current_page:
            links.append(f'<span class="current">{i}</span>')
        else:
            url = f"{base_path}-{i}.html"
            links.append(f'<a href="{url}">{i}</a>')
    return '<div class="pagination">\n' + "\n".join(links) + "\n</div>"