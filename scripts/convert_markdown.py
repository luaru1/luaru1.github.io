import markdown
from pathlib import Path
from string import Template
from utils.metadata import extract_metadata
from utils.post import get_all_posts

# 디렉토리 설정
POSTS_DIR = Path("posts")
OUTPUT_DIR = Path("posts-html")
TEMPLATE_PATH = Path("template/post-template.html")

# 템플릿 읽기
with open(TEMPLATE_PATH, encoding="utf-8") as f:
    html_template = Template(f.read())

def convert_all_posts():
    count = 0
    posts = get_all_posts(POSTS_DIR)

    for meta in posts:
        md_file = POSTS_DIR / meta["category"] / (meta["slug"] + ".md")
        html_file = Path(meta["url"].lstrip("/"))  # "/posts-html/..." → "posts-html/..."

        # 변환 필요 여부
        if html_file.exists() and html_file.stat().st_mtime >= md_file.stat().st_mtime:
            continue

        with open(md_file, encoding="utf-8") as f:
            lines = f.readlines()

        # YAML 경계선 이후 내용만 추출
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

        html = html_template.substitute(
            title=meta["title"],
            date=meta["date"].strftime("%Y-%m-%d"),
            content=html_body
        )

        html_file.parent.mkdir(parents=True, exist_ok=True)
        html_file.write_text(html, encoding="utf-8")
        count += 1

    print(f"마크다운 변환 완료: {count}개 파일 변환됨")