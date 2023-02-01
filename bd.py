from sqlalchemy import create_engine
engine = create_engine("mysql://user:pwd@localhost/college",echo = True)
from sqlalchemy import Table, Column, Integer, String, MetaData
meta = MetaData()

tasks = Table(
