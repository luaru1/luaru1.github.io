from pathlib import Path
from string import Template
from utils.post import get_all_posts
from utils.pagination import paginate, generate_pagination_links

POSTS_DIR = Path("posts")
OUTPUT_DIR = Path("all-posts")
PER_PAGE = 10

# 템플릿 경로
BASE_TEMPLATE = Path("template/base-page-template.html")
CARD_TEMPLATE = Path("template/card-item-wide-template.html")
GRID_TEMPLATE = Path("template/card-grid-pagination-template.html")

def update_all_posts_page():
    all_posts = get_all_posts(POSTS_DIR)
    total_pages, get_page = paginate(all_posts, PER_PAGE)

    with open(BASE_TEMPLATE, encoding="utf-8") as f:
        base_tpl = Template(f.read())
    with open(CARD_TEMPLATE, encoding="utf-8") as f:
        card_tpl = Template(f.read())
    with open(GRID_TEMPLATE, encoding="utf-8") as f:
        grid_tpl = Template(f.read())
    
    for page in range(1, total_pages + 1):
        page_posts = get_page(page)

        cards_html = "\n".join(
            card_tpl.substitute(
                url=post["url"],
                title=post["title"],
                date=post["date"].strftime("%Y-%m-%d")
            ) for post in page_posts
        )

        pagination_links = generate_pagination_links(page, total_pages, "all-posts")

        grid_html = grid_tpl.substitute(cards=cards_html, pagination=pagination_links)

        final_html = base_tpl.substitute(
            title="전체 글",
            heading="전체 글",
            content=grid_html
        )

        filename = f"all-posts-{page}.html"
        (OUTPUT_DIR / filename).write_text(final_html, encoding = "utf-8")

    print("all-posts.html (전체 글) 생성 완료")