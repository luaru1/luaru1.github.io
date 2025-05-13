from pathlib import Path
from string import Template
from utils.post import get_all_posts

POSTS_DIR = Path("posts")
OUTPUT_FILE = Path("index.html")

# 템플릿 경로
BASE_TEMPLATE = Path("template/base-page-template.html")
CARD_TEMPLATE = Path("template/card-item-wide-template.html")
GRID_TEMPLATE = Path("template/card-grid-wide-template.html")

def update_home_page():
    all_posts = get_all_posts(POSTS_DIR)
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
