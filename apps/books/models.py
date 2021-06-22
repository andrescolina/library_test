
from core.db import metadata
from apps.auth.models import users
import sqlalchemy


book = sqlalchemy.Table(
    "book",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String(200), nullable=False),
    sqlalchemy.Column("subtitle", sqlalchemy.String(200), nullable=False),
    sqlalchemy.Column("date_publish", sqlalchemy.Date(), nullable=False),
    sqlalchemy.Column("editor", sqlalchemy.String(200), nullable=False),
    sqlalchemy.Column("description", sqlalchemy.String(200), nullable=False),
    sqlalchemy.Column("image", sqlalchemy.String(100), nullable=False),
    sqlalchemy.Column("user_created", sqlalchemy.ForeignKey(users.c.id))
)

category = sqlalchemy.Table(
    "categories",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(200), nullable=False),
    sqlalchemy.Column("description", sqlalchemy.String(200), nullable=True)
)

authors = sqlalchemy.Table(
    "authors",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(200), nullable=False),
    sqlalchemy.Column("description", sqlalchemy.String(200), nullable=True)
)

category_book = sqlalchemy.Table(
    "categories_book",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("book_id", sqlalchemy.ForeignKey(users.c.id)),
    sqlalchemy.Column("category_id", sqlalchemy.ForeignKey(category.c.id))
)

authors_book = sqlalchemy.Table(
    "authors_book",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("book_id", sqlalchemy.ForeignKey(users.c.id)),
    sqlalchemy.Column("author_id", sqlalchemy.ForeignKey(authors.c.id))
)