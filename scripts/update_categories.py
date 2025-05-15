from pathlib import Path
from string import Template
from collections import defaultdict
from utils.pagination import paginate, generate_pagination_links
from utils.metadata import extract_metadata
from utils.slug import slugify_name

POSTS_DIR = Path("posts")
OUTPUT_DIR = Path("categories")
OUTPUT_DIR.mkdir(exist_ok=True)
INDEX_TEMPLATE = Path("template/card-item-template.html")
BASE_TEMPLATE = Path("template/base-page-template.html")
GRID_TEMPLATE = Path("template/card-grid-pagination-template.html")
CARD_TEMPLATE = Path("template/card-item-wide-template.html")
PER_PAGE = 10

def generate_category_pages():
    categories = defaultdict(list)

    for cat_dir in POSTS_DIR.iterdir():
        if not cat_dir.is_dir():
            continue
        for md in cat_dir.glob("*.md"):
            meta = extract_metadata(md)
            if meta:
                url = f"/posts-html/{slugify_name(meta['category'])}/{meta['slug']}.html"
                categories[meta['category']].append({
                    "title": meta["title"],
                    "date": meta["date"],
                    "url": url
                })

    # 카테고리 인덱스 페이지 생성
    with open(INDEX_TEMPLATE, encoding="utf-8") as f:
        card_tpl = Template(f.read())
    with open(BASE_TEMPLATE, encoding="utf-8") as f:
        base_tpl = Template(f.read())

    cards = "\n".join(
        card_tpl.substitute(url=f"/categories/{slugify_name(cat)}/{slugify_name(cat)}-1.html", name=cat, count=len(posts))
        for cat, posts in sorted(categories.items(), key=lambda x: len(x[1]), reverse=True)
    )

    index_html = base_tpl.substitute(
        title="카테고리",
        heading="카테고리",
        content=f'<div class="card-container">\n{cards}\n</div>'
    )

    (OUTPUT_DIR / "index.html").write_text(index_html, encoding="utf-8")

    # 각 카테고리별 상세 페이지 (페이지네이션 포함)
    with open(GRID_TEMPLATE, encoding="utf-8") as f:
        grid_tpl = Template(f.read())
    with open(CARD_TEMPLATE, encoding="utf-8") as f:
        post_tpl = Template(f.read())

    for cat, posts in categories.items():
        category_dir = OUTPUT_DIR / slugify_name(cat)
        category_dir.mkdir(exist_ok=True)

        posts.sort(key=lambda x: x["date"], reverse=True)
        total_pages, get_page = paginate(posts, PER_PAGE)

        for page in range(1, total_pages + 1):
            page_posts = get_page(page)

            post_html = "\n".join(
                post_tpl.substitute(
                    url=p["url"],
                    title=p["title"],
                    date=p["date"].strftime("%Y-%m-%d")
                )
                for p in page_posts
            )

            pagination = generate_pagination_links(page, total_pages, f"{category_dir}/{slugify_name(cat)}")
            grid_html = grid_tpl.substitute(cards=post_html, pagination=pagination)

            final_html = base_tpl.substitute(
                title=f"{cat} | 카테고리",
                heading=cat,
                content=grid_html
            )

            filename = f"{slugify_name(cat)}-{page}.html"
            (category_dir / filename).write_text(final_html, encoding="utf-8")

    print(f"카테고리 페이지 생성 완료: {len(categories)}개 카테고리")