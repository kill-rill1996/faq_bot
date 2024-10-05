import datetime
from typing import List
from sqlalchemy.orm import joinedload
from sqlalchemy import or_

from database import tables
from .database import Session


def create_admin(tg_id: str) -> None:
    """Добавление администратора"""
    with Session() as session:
        admin = tables.Admin(tg_id=tg_id)
        session.add(admin)
        session.commit()


def get_admin_by_id(tg_id: str) -> tables.Admin:
    """Получение админа по tg_id"""
    with Session() as session:
        admin = session.query(tables.Admin)\
            .filter(tables.Admin.tg_id == tg_id)\
            .first()
        return admin


def get_all_admins() -> List[tables.Admin]:
    """Получение всех админов"""
    with Session() as session:
        admins = session.query(tables.Admin).all()
        return admins


def create_group(title: str) -> int:
    """Создание группы"""
    with Session() as session:
        group = tables.Group(title=title)
        session.add(group)
        session.commit()
        return group.id


def create_subgroup(title: str, group_id: int) -> int:
    """Создание подгруппы по id группы"""
    with Session() as session:
        subgroup = tables.SubGroup(title=title, group_id=group_id)
        session.add(subgroup)
        session.commit()
        return subgroup.id


def create_question(title: str, subgroup_id: int) -> int:
    """Создание вопроса по id подгруппы"""
    with Session() as session:
        question = tables.Question(title=title, subgroup_id=subgroup_id)
        session.add(question)
        session.commit()
        return question.id


def create_answer(text: str, question_id: int) -> None:
    """Создание ответа на вопрос с question_id"""
    with Session() as session:
        answer = tables.Answer(text=text, question_id=question_id)
        session.add(answer)
        session.commit()


def get_all_groups() -> List[tables.Group]:
    """Получение всех групп"""
    with Session() as session:
        groups = session.query(tables.Group).order_by(tables.Group.title).all()
        return groups


def get_all_subgroups_by_group_id(group_id: int) -> List[tables.SubGroup]:
    """Получение всех подгрупп по id группы"""
    with Session() as session:
        subgroups = session.query(tables.SubGroup)\
            .filter(tables.SubGroup.group_id == group_id)\
            .order_by(tables.SubGroup.title).all()

        return subgroups


def get_all_questions_by_subgroup_id(subgroup_id: int) -> List[tables.Question]:
    """Получение всех вопросов по id подгруппы"""
    with Session() as session:
        questions = session.query(tables.Question)\
            .filter(tables.Question.subgroup_id == subgroup_id)\
            .order_by(tables.Question.title).all()

        return questions


def get_all_answers_by_question_id(question_id: int) -> List[tables.Answer]:
    """Получение всех ответов по id вопроса"""
    with Session() as session:
        answers = session.query(tables.Answer)\
            .filter(tables.Answer.question_id == question_id)\
            .order_by(tables.Answer.id).all()

        return answers


def get_question_by_id(question_id: int) -> tables.Question:
    """Получение вопроса по его id"""
    with Session() as session:
        question = session.query(tables.Question).filter(tables.Question.id == question_id).first()
        return question

