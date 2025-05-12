import yaml
from pathlib import Path
import datetime
from string import Template
from collections import defaultdict
from utils.pagination import paginate  # 유틸 함수

POSTS_DIR = Path("posts")
OUTPUT_DIR = Path("tags")
TAG_TEMPLATE = Path("template/tag-card-template.html")
BASE_TEMPLATE = Path("template/base-page-template.html")
GRID_TEMPLATE = Path("template/grid-with-pagination-template.html")
CARD_TEMPLATE = Path("template/card-item-wide-template.html")
PER_PAGE = 10

def extract_metadata(md_file):
    with open(md_file, encoding="utf-8") as f:
        lines = f.readlines()
    if lines[0].strip() == "---":
        end_idx = lines[1:].index("---\n") + 1
        meta = yaml.safe_load("".join(lines[1:end_idx]))
        raw_date = meta.get("date", "1900-01-01")
        if isinstance(raw_date, datetime.datetime):
            parsed_date = raw_date
        elif isinstance(raw_date, datetime.date):
            parsed_date = datetime.datetime.combine(raw_date, datetime.datetime.min.time())
        else:
            parsed_date = datetime.datetime.strptime(str(raw_date), "%Y-%m-%d")
        return {
            "title": meta.get("title", md_file.stem),
            "date": parsed_date,
            "tags": meta.get("tags", []),
            "category": meta.get("category", md_file.parent.name),
            "slug": md_file.stem
        }
    return None

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
    with open(TAG_TEMPLATE, encoding="utf-8") as f:
        card_tpl = Template(f.read())
    with open(BASE_TEMPLATE, encoding="utf-8") as f:
        base_tpl = Template(f.read())

    OUTPUT_DIR.mkdir(exist_ok=True)

    cards = "\n".join(
        card_tpl.substitute(name=tag, count=len(posts))
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

            pagination = generate_pagination_links(page, total_pages, f"/tags/{tag}")
            grid_html = grid_tpl.substitute(cards=post_html, pagination=pagination)

            final_html = base_tpl.substitute(
                title=f"{tag} | 태그",
                heading=f"#{tag}",
                content=grid_html
            )

            filename = f"{tag}.html" if page == 1 else f"{tag}-{page}.html"
            (OUTPUT_DIR / filename).write_text(final_html, encoding="utf-8")

    print(f"태그 페이지 생성 완료: {len(tags)}개 태그")

def generate_pagination_links(current_page, total_pages, base_path):
    links = []
    for i in range(1, total_pages + 1):
        if i == current_page:
            links.append(f'<span class="current">{i}</span>')
        else:
            url = f"{base_path}.html" if i == 1 else f"{base_path}-{i}.html"
            links.append(f'<a href="{url}">{i}</a>')
    return '<div class="pagination">\n' + "\n".join(links) + '\n</div>'
