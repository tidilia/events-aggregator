def build_url(base_url: str, page: int, page_size: int, date_from=None):
    params = f"?page={page}&page_size={page_size}"
    if date_from:
        params += f"&date_from={date_from}"
    return base_url + params