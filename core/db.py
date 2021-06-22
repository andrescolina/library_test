import databases
import sqlalchemy
import os
import pymysql

pymysql.install_as_MySQLdb()


DATABASE_URL = os.getenv("DATABASE_URL_LIBRARY")

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()


users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("user", sqlalchemy.String(16)),
    sqlalchemy.Column("password", sqlalchemy.String(100)),
    sqlalchemy.Column("is_admin", sqlalchemy.Boolean()),
    sqlalchemy.Column("is_active", sqlalchemy.Boolean())
)

book = sqlalchemy.Table(
    "book",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String(16), nullable=False),
    sqlalchemy.Column("subtitle", sqlalchemy.String(16), nullable=False),
    sqlalchemy.Column("date_publish", sqlalchemy.Date(), nullable=False),
    sqlalchemy.Column("editor", sqlalchemy.String(16), nullable=False),
    sqlalchemy.Column("source", sqlalchemy.String(16), nullable=False),
    sqlalchemy.Column("description", sqlalchemy.String(16), nullable=False),
    sqlalchemy.Column("image", sqlalchemy.String(100), nullable=False),
    sqlalchemy.Column("user_created", sqlalchemy.ForeignKey(users.c.id))
)


category = sqlalchemy.Table(
    "categories",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(16), nullable=False),
    sqlalchemy.Column("description", sqlalchemy.String(16), nullable=True)
)

authors = sqlalchemy.Table(
    "authors",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(16), nullable=False),
    sqlalchemy.Column("description", sqlalchemy.String(16), nullable=True)
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
    sqlalchemy.Column("authors_id", sqlalchemy.ForeignKey(authors.c.id))
)

engine = sqlalchemy.create_engine(
    DATABASE_URL
)
metadata.create_all(engine)
