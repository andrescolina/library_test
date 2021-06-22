

def query_normal(field, value, condition):
    return """
        SELECT 
            a.id AS id,
            a.title AS title,
            a.subtitle AS subtitle,
            a.date_publish AS date_publish,
            a.editor AS editor,
            a.description AS description,
            a.image AS image,
            GROUP_CONCAT(distinct a.categories) AS categories,
            GROUP_CONCAT(distinct a.authors) AS authors FROM
        (SELECT 
            a.id AS id,
            a.title AS title,
            a.subtitle AS subtitle,
            a.date_publish AS date_publish,
            a.editor AS editor,
            a.description AS description,
            a.image AS image,
            e.name AS categories,
            c.name AS authors
        FROM
            library.book a
        LEFT JOIN 
            library.authors_book b
            ON a.id = b.book_id
        INNER JOIN
            library.authors c
            ON c.id = b.authors_id
        LEFT JOIN 
            library.categories_book d
            ON a.id = d.book_id
        INNER JOIN
            library.categories e
            ON e.id = d.category_id
        WHERE
            a.""" + field + """ """ + condition + """ """ + value + """) a
        GROUP BY
            a.id,
            a.title,
            a.subtitle,
            a.date_publish,
            a.editor,
            a.description,
            a.image
    """


def query_relations(value, categories):
    if categories:
        relation = """
            library.categories a
            INNER JOIN 
                library.categories_book b
                ON a.id = b.category_id
        """
    else:
        relation = """
            library.authors a
            INNER JOIN 
                library.authors_book b
                ON a.id = b.authors_id
        """
    return """
            SELECT 
                a.id AS id,
                a.title AS title,
                a.subtitle AS subtitle,
                a.date_publish AS date_publish,
                a.editor AS editor,
                a.description AS description,
                a.image AS image,
                GROUP_CONCAT(distinct a.categories) AS categories,
                GROUP_CONCAT(distinct a.authors) AS authors
            FROM (SELECT 
                c.id AS id,
                c.title AS title,
                c.subtitle AS subtitle,
                c.date_publish AS date_publish,
                c.editor AS editor,
                c.description AS description,
                c.image AS image,
                h.name AS categories,
                f.name AS authors
            FROM
                """ + relation +  """
            INNER JOIN 
                library.book c
                ON b.book_id = c.id
            LEFT JOIN 
                library.authors_book e
                ON c.id = e.book_id
            INNER JOIN
                library.authors f
                ON f.id = e.authors_id
            LEFT JOIN 
                library.categories_book g
                ON c.id = g.book_id
            INNER JOIN
                library.categories h
                ON g.category_id = h.id
            WHERE
                a.name LIKE '%""" + value + """%') a
            GROUP BY
                a.id,
                a.title,
                a.subtitle,
                a.date_publish,
                a.editor,
                a.description,
                a.image;
                """