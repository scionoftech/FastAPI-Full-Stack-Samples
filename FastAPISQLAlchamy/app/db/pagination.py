import math


class Page(object):
    """ Pagination Util for List data"""

    def __init__(self, items, page, page_size, total):
        self.items = items
        self.page_size = len(items)
        self.previous_page = None
        self.next_page = None
        self.has_previous = page > 1
        if self.has_previous:
            self.previous_page = page - 1
        previous_items = (page - 1) * page_size
        self.has_next = previous_items + len(items) < total
        if self.has_next:
            self.next_page = page + 1
        self.total_items = total
        self.pages = int(math.ceil(total / float(page_size)))


def paginate(query, page, page_size) -> Page:
    if page <= 0:
        raise AttributeError('page needs to be >= 1')
    if page_size <= 0:
        raise AttributeError('page_size needs to be >= 1')
    items = query.limit(page_size).offset((page - 1) * page_size).all()
    # We remove the ordering of the query since
    # it doesn't matter for getting a count and
    # might have performance implications
    # as discussed on this Flask-SqlAlchemy issue
    # https://github.com/mitsuhiko/flask-sqlalchemy/issues/100
    total = query.count()
    return Page(items, page, page_size, total)
