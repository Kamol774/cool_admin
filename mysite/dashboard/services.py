from django.db import connection
from contextlib import closing

def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def dictfetchone(cursor):
    row = cursor.fetchone()
    if row is None:
        return False
    columns = [col[0] for col in cursor.description]
    return dict(zip(columns, row))


def get_authors():
    with closing(connection.cursor()) as cursor:
        cursor.execute(
            """select count(dashboard_book.id) as books_count, dashboard_author.* from dashboard_book
            right join dashboard_author on dashboard_book.author_id = dashboard_author.id
            group by dashboard_author.id"""
            
            # """select dashboard_author.*, count(dashboard_book.id) as books_count from dashboard_author
            # left join dashboard_book on dashboard_author.id = dashboard_book.author_id
            # group by dashboard_author.id"""
        )
        authors = dictfetchall(cursor)
        return authors


def get_author_by_id(author_id):
    with closing(connection.cursor()) as cursor:
        cursor.execute("""SELECT * FROM dashboard_author WHERE id = %s""", [author_id])
        authors = dictfetchall(cursor)
        return authors


def get_categories():
    with closing(connection.cursor()) as cursor:
        cursor.execute(
            """select dashboard_category.*, count(dashboard_book.id) as books_count from dashboard_category
            left join dashboard_book on dashboard_category.id = dashboard_book.category_id
            group by dashboard_category.id"""
        )
        categories = dictfetchall(cursor)
        return categories


def get_category_by_id(category_id):
    with closing(connection.cursor()) as cursor:
        cursor.execute("""SELECT * FROM dashboard_category WHERE id = %s""", [category_id])
        categories = dictfetchall(cursor)
        return categories
