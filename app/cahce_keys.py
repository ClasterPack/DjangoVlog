def page_detail_cache_key(page_id: int) -> str:
    return f"page_detail:{page_id}:v1"