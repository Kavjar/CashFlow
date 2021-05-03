import os
from contextlib import contextmanager
from typing import Iterator
from flask import Flask
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

flask_app = Flask(__name__)
flask_app.config["DEBUG"] = True
engine = create_engine(os.environ["DATABASE_URL"])
metadata = MetaData(bind=engine)
Base = declarative_base(metadata)
Session = sessionmaker(bind=engine)
session = Session()

# @contextmanager
# def session_scope() -> Iterator[Session]:
#     """
#     Context manager to handle tranaction to DB
#     """
#     try:
#         yield session
#         session.commit()
#     except SQLAlchemyError:
#         session.rollback()
#         raise
#     else:
#         try:
#             session.commit()
#         except SQLAlchemyError:
#             session.rollback()
#             raise


from restful_api import models, views