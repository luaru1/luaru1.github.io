from pathlib import Path
from datetime import datetime, date
import yaml
from string import Template

POSTS_DIR = Path("posts")
OUTPUT_FILE = Path("index.html")

# 템플릿 경로
BASE_TEMPLATE = Path("template/base-page-template.html")
CARD_TEMPLATE = Path("template/card-item-wide-template.html")
GRID_TEMPLATE = Path("template/card-grid-wide-template.html")

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
    return posts

def update_home_page():
    all_posts = sorted(get_all_posts(), key=lambda x: x["date"], reverse=True)
    recent_posts = all_posts[:5]

    with open(BASE_TEMPLATE, encoding="utf-8") as f:
        base_tpl = Template(f.read())
    with open(CARD_TEMPLATE, encoding="utf-8") as f:
        card_tpl = Template(f.read())
    with open(GRID_TEMPLATE, encoding="utf-8") as f:
        grid_tpl = Template(f.read())

    cards = "\n".join(
        card_tpl.substitute(
            url=post["url"],
            title=post["title"],
            date=post["date"].strftime("%Y-%m-%d")
        ) for post in recent_posts
    )

    grid_html = grid_tpl.substitute(cards=cards)

    final_html = base_tpl.substitute(
        title="루아의 아카이브",
        heading="최근 글",
        content=grid_html
    )

    OUTPUT_FILE.write_text(final_html, encoding="utf-8")
    print("index.html (최근 글) 업데이트 완료")

if __name__ == "__main__":
    update_home_page()
