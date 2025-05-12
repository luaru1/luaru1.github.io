import os
import markdown
import yaml
from pathlib import Path
from string import Template

# 디렉토리 설정
POSTS_DIR = Path("posts")
OUTPUT_DIR = Path("posts-html")
TEMPLATE_PATH = Path("template/post-template.html")

# 템플릿 읽기
with open(TEMPLATE_PATH, encoding="utf-8") as f:
    html_template = Template(f.read())

# HTML 변환 함수
def convert_all_posts():
    count = 0
    for category_dir in POSTS_DIR.iterdir():
        if not category_dir.is_dir():
            continue
        category = category_dir.name
        for md_file in category_dir.glob("*.md"):
            # 대상 경로
            html_dir = OUTPUT_DIR / category
            html_file = html_dir / (md_file.stem + ".html")

            # 변환 필요 여부
            if html_file.exists() and html_file.stat().st_mtime >= md_file.stat().st_mtime:
                continue

            # 마크다운 파일 읽기
            with open(md_file, encoding="utf-8") as f:
                lines = f.readlines()

            # YAML 메타데이터
            if lines[0].strip() == "---":
                end_idx = lines[1:].index("---\n") + 1
                metadata = yaml.safe_load("".join(lines[1:end_idx]))
                content_md = "".join(lines[end_idx+1:])
            else:
                metadata = {}
                content_md = "".join(lines)

            title = metadata.get("title", md_file.stem)
            date = metadata.get("date", "작성일 미상")

            html_body = markdown.markdown(
                content_md,
                extensions=['fenced_code', 'tables', 'codehilite', 'toc'],
                extension_configs={
                    'codehilite': {'linenums': False},
                    'toc': {'permalink': False}
                }
            )

            # HTML 구성
            html = html_template.substitute(
                title=title,
                date=date,
                content=html_body
            )

            # 저장
            html_dir.mkdir(parents=True, exist_ok=True)
            html_file.write_text(html, encoding="utf-8")
            count += 1

    print(f"마크다운 변환 완료: {count}개 파일 변환됨")