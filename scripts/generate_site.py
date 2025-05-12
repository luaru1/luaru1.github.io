from convert_markdown import convert_all_posts
from update_all_posts import update_all_posts_page
from update_home import update_home_page
from update_categories import generate_category_pages
from update_tags import generate_tag_pages

def main():
    print("마크다운 → HTML 변환 중...")
    convert_all_posts()

    print("전체 글 목록 페이지 생성 중...")
    update_all_posts_page()

    print("홈 화면 최근 글 갱신 중...")
    update_home_page()

    print("카테고리별 페이지 생성 중...")
    generate_category_pages()

    print("태그별 페이지 생성 중...")
    generate_tag_pages()

    print("\n사이트 전체 빌드 완료!")

if __name__ == "__main__":
    main()