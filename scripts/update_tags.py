from pathlib import Path
from string import Template
from collections import defaultdict
from utils.pagination import paginate, generate_pagination_links
from utils.metadata import extract_metadata
from utils.slug import slugify_name

POSTS_DIR = Path("posts")
OUTPUT_DIR = Path("tags")
INDEX_TEMPLATE = Path("template/card-item-template.html")
BASE_TEMPLATE = Path("template/base-page-template.html")
GRID_TEMPLATE = Path("template/card-grid-pagination-template.html")
CARD_TEMPLATE = Path("template/card-item-wide-template.html")
PER_PAGE = 10

def generate_tag_pages():
    tags = defaultdict(list)

    for cat_dir in POSTS_DIR.iterdir():
        if not cat_dir.is_dir():
            continue
        for md in cat_dir.glob("*.md"):
            meta = extract_metadata(md)
            if meta:
                url = f"/posts-html/{meta['category']}/{meta['slug']}.html"
                for tag in meta["tags"]:
                    tags[tag].append({
                        "title": meta["title"],
                        "date": meta["date"],
                        "url": url
                    })

    # 태그 인덱스 페이지
    with open(INDEX_TEMPLATE, encoding="utf-8") as f:
        card_tpl = Template(f.read())
    with open(BASE_TEMPLATE, encoding="utf-8") as f:
        base_tpl = Template(f.read())

    OUTPUT_DIR.mkdir(exist_ok=True)

    cards = "\n".join(
        card_tpl.substitute(url=f"/tags/{slugify_name(tag)}/{slugify_name(tag)}-1.html", name=tag, count=len(posts))
        for tag, posts in sorted(tags.items(), key=lambda x: len(x[1]), reverse=True)
    )

    index_html = base_tpl.substitute(
        title="태그",
        heading="태그",
        content=f'<div class="card-container">\n{cards}\n</div>'
    )

    (OUTPUT_DIR / "index.html").write_text(index_html, encoding="utf-8")

    # 태그별 상세 페이지 (페이지네이션 적용)
    with open(GRID_TEMPLATE, encoding="utf-8") as f:
        grid_tpl = Template(f.read())
    with open(CARD_TEMPLATE, encoding="utf-8") as f:
        post_tpl = Template(f.read())

    for tag, posts in tags.items():
        tag_dir = OUTPUT_DIR / slugify_name(tag)
        tag_dir.mkdir(exist_ok=True)

        posts.sort(key=lambda x: x["date"], reverse=True)
        total_pages, get_page = paginate(posts, PER_PAGE)

        for page in range(1, total_pages + 1):
            page_posts = get_page(page)

            post_html = "\n".join(
                post_tpl.substitute(
                    url=post["url"],
                    title=post["title"],
                    date=post["date"].strftime("%Y-%m-%d")
                )
                for post in page_posts
            )

            pagination = generate_pagination_links(page, total_pages, f"{tag_dir}/{slugify_name(tag)}")
            grid_html = grid_tpl.substitute(cards=post_html, pagination=pagination)

            final_html = base_tpl.substitute(
                title=f"{tag} | 태그",
                heading=f"# {tag}",
                content=grid_html
            )

            filename = f"{slugify_name(tag)}-{page}.html"
            (tag_dir / filename).write_text(final_html, encoding="utf-8")

    print(f"태그 페이지 생성 완료: {len(tags)}개 태그")