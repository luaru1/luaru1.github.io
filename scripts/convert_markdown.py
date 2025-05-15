import markdown
from pathlib import Path
from string import Template
from utils.post import get_all_posts
from utils.slug import slugify_name

POSTS_DIR = Path("posts")
OUTPUT_DIR = Path("posts-html")
CONTENT_TEMPLATE = Path("template/post-template.html")
BASE_TEMPLATE = Path("template/base-page-template.html")

# 템플릿 읽기
with open(CONTENT_TEMPLATE, encoding="utf-8") as f:
    content_tpl = Template(f.read())
with open(BASE_TEMPLATE, encoding="utf-8") as f:
    base_tpl = Template(f.read())

def convert_all_posts():
    count = 0
    posts = get_all_posts(POSTS_DIR)

    for meta in posts:
        md_file = POSTS_DIR / slugify_name(meta["category"]) / f"{meta['slug']}.md"
        html_dir = OUTPUT_DIR / slugify_name(meta["category"])
        html_file = Path(meta["url"].lstrip("/"))

        html_dir.mkdir(exist_ok=True)

        if html_file.exists() and html_file.stat().st_mtime >= md_file.stat().st_mtime:
            continue

        with open(md_file, encoding="utf-8") as f:
            lines = f.readlines()

        if lines[0].strip() == "---":
            end_idx = lines[1:].index("---\n") + 1
            content_md = "".join(lines[end_idx+1:])
        else:
            content_md = "".join(lines)

        html_body = markdown.markdown(
            content_md,
            extensions=["fenced_code", "tables", "codehilite", "toc"],
            extension_configs={
                "codehilite": {"linenums": False},
                "toc": {"permalink": False}
            }
        )

        # 하위 템플릿 먼저 적용
        content_html = content_tpl.substitute(
            date=meta["date"].strftime("%Y-%m-%d"),
            content=html_body
        )

        # base 템플릿에 삽입
        full_html = base_tpl.substitute(
            title=meta["title"],
            heading=meta["title"],
            content=content_html
        )

        html_file.parent.mkdir(parents=True, exist_ok=True)
        html_file.write_text(full_html, encoding="utf-8")
        count += 1

    print(f"마크다운 변환 완료: {count}개 파일 변환됨")