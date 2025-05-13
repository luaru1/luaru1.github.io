from utils.metadata import extract_metadata

def get_all_posts(POSTS_DIR):
    posts = []
    for category_dir in POSTS_DIR.iterdir():
        if not category_dir.is_dir():
            continue
        for md_file in category_dir.glob("*.md"):
            meta = extract_metadata(md_file)
            if meta:
                meta["url"] = f'/posts-html/{meta["category"]}/{meta["slug"]}.html'
                posts.append(meta)
    return sorted(posts, key=lambda x: x["date"], reverse=True)