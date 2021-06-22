from core.db import metadata
import sqlalchemy

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("user", sqlalchemy.String(16)),
    sqlalchemy.Column("password", sqlalchemy.String(100)),
    sqlalchemy.Column("is_admin", sqlalchemy.Boolean()),
    sqlalchemy.Column("is_active", sqlalchemy.Boolean())
)