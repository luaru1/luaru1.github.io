import yaml
from datetime import datetime, date

def extract_metadata(md_file):
    with open(md_file, encoding="utf-8") as f:
        lines = f.readlines()
    if lines[0].strip() == "---":
        end_idx = lines[1:].index("---\n") + 1
        meta = yaml.safe_load("".join(lines[1:end_idx]))
        raw_date = meta.get("date", "2025-01-01")
        if isinstance(raw_date, datetime):
            parsed_date = raw_date
        elif isinstance(raw_date, date):
            parsed_date = datetime.combine(raw_date, datetime.min.time())
        else:
            parsed_date = datetime.strptime(str(raw_date), "%Y-%m-%d")
        return {
            "title": meta.get("title", md_file.stem),
            "date": parsed_date,
            "tags": meta.get("tags", []),
            "category": meta.get("category", md_file.parent.name),
            "slug": md_file.stem
        }
    return None