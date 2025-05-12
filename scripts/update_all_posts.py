from pathlib import Path
from datetime import datetime, date
import yaml
from string import Template
from utils.pagination import paginate

POSTS_DIR = Path("posts")
OUTPUT_DIR = Path(".")
PER_PAGE = 10

# 템플릿 경로
BASE_TEMPLATE = Path("template/base-page-template.html")
CARD_TEMPLATE = Path("template/card-item-wide-template.html")
GRID_TEMPLATE = Path("template/grid-with-pagination-template.html")

def extract_metadata(md_file):
    with open(md_file, encoding="utf-8") as f:
        lines = f.readlines()
    if lines[0].strip() == "---":
        end_idx = lines[1:].index("---\n") + 1
        meta = yaml.safe_load("".join(lines[1:end_idx]))
        raw_date = meta.get("date", "1900-01-01")
        if isinstance(raw_date, datetime):
            post_date = raw_date
        elif isinstance(raw_date, date):
            post_date = datetime.combine(raw_date, datetime.min.time())
        else:
            post_date = datetime.strptime(str(raw_date), "%Y-%m-%d")
        return {
            "title": meta.get("title", md_file.stem),
            "date": post_date,
            "category": meta.get("category", md_file.parent.name),
            "slug": md_file.stem
        }
    return None

def get_all_posts():
    posts = []
    for category_dir in POSTS_DIR.iterdir():
        if not category_dir.is_dir():
            continue
        for md_file in category_dir.glob("*.md"):
            meta = extract_metadata(md_file)
            if meta:
                meta["url"] = f"/posts-html/{meta['category']}/{meta['slug']}.html"
                posts.append(meta)
    return sorted(posts, key=lambda x: x['date'], reverse=True)

def generate_pagination_links(current_page, total_pages, base_name):
    links = []
    for i in range(1, total_pages + 1):
        if i == current_page:
            links.append(f'<span class="current">{i}</span>')
        else:
            url = f'/{base_name}.html' if i == 1 else f'/{base_name}-{i}.html'
            links.append(f'<a href="{url}">{i}</a>')
    return '<div class="pagination">\n' + '\n'.join(links) + '\n</div>'

def update_all_posts_page():
    posts = get_all_posts()
    total_pages, get_page = paginate(posts, PER_PAGE)

    with open(BASE_TEMPLATE, encoding="utf-8") as f:
        base_tpl = Template(f.read())
    with open(CARD_TEMPLATE, encoding="utf-8") as f:
        card_tpl = Template(f.read())
    with open(GRID_TEMPLATE, encoding="utf-8") as f:
        grid_tpl = Template(f.read())
    
    for page in range(1, total_pages + 1):
        page_posts = get_page(page)

        cards_html = '\n'.join(
            card_tpl.substitute(
                url=post['url'],
                title=post['title'],
                date=post['date'].strftime('%Y-%m-%d')
            ) for post in page_posts
        )

        pagination_links = generate_pagination_links(page, total_pages, 'all-posts')

        grid_html = grid_tpl.substitute(cards=cards_html, pagination=pagination_links)

        final_html = base_tpl.substitute(
            title="전체 글",
            heading="전체 글",
            content=grid_html
        )

        filename = f'all-posts.html' if page == 1 else f'all-posts-{page}.html'
        (OUTPUT_DIR / filename).write_text(final_html, encoding = 'utf-8')

    print("all-posts.html (전체 글) 생성 완료")

if __name__ == "__main__":
    update_all_posts_page()
