import datetime
from typing import List
from sqlalchemy.orm import joinedload
from sqlalchemy import or_

from database import tables
from .database import Session


def create_group() -> None:
    """Создание пользователя и его payers на все существующие события"""
    with Session() as session:
        group = tables.Group(title="test_group")
        session.add(group)
        session.commit()