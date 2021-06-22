import databases
import sqlalchemy
import os
import pymysql

pymysql.install_as_MySQLdb()


DATABASE_URL = os.getenv("DATABASE_URL_LIBRARY")

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

engine = sqlalchemy.create_engine(
    DATABASE_URL
)
metadata.create_all(engine)
