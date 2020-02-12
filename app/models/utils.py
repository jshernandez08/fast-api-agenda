
def _get_paginator(page, per_page):
    start = (int(page) - 1) * per_page
    return start, per_page