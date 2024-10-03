import datetime
from typing import List
from sqlalchemy.orm import joinedload
from sqlalchemy import or_

from database import tables
from .database import Session


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


def create_fake_data():
    # Groups
    create_group(title="Арбитражный суд")
    create_group(title="Имущество")
    create_group(title="Бухгалетрия")

    # Subgroups
    create_subgroup(title="Гражданское право", group_id=1)
    create_subgroup(title="Уголовное право", group_id=1)
    create_subgroup(title="Раздел имущества", group_id=2)
    create_subgroup(title="Установка 1С", group_id=3)
    create_subgroup(title="Импорт из 1С", group_id=3)
    create_subgroup(title="Учет мат. ценностей", group_id=3)

    # Questions
    create_question(title="Признание виновника ДТП", subgroup_id=1)
    create_question(title="Раздел имущества при разводе", subgroup_id=1)
    create_question(title="Какой максимальный срок по УК РФ ст. 105?", subgroup_id=2)
    create_question(title="Правила раздела имущества согласно ГК РФ", subgroup_id=3)
    create_question(title="Комиссия при наследстве", subgroup_id=3)
    create_question(title="Откуда скачать установочник 1С?", subgroup_id=4)
    create_question(title="Как распаковать установочник 1С?", subgroup_id=4)
    create_question(title="Как проверить версию 1С после установки?", subgroup_id=4)
    create_question(title="Стандартная кодировка при выгрузке из 1С в csv формате", subgroup_id=5)
    create_question(title="Время ожидания выгрузки из 1С", subgroup_id=5)
    create_question(title="Стандарты создания таблиц для учета мат. ценностей в госбюджетных учреждениях", subgroup_id=6)
    create_question(title="Стандарты создания таблиц для учета мат. ценностей в юридических организациях", subgroup_id=6)

    # Answers
    create_answer(text="Признание виновника ДТП осуществляется исходя из статьи ГК РФ 39303...", question_id=1)
    create_answer(text="Раздел имущества при разводе и согласии сторон производится...", question_id=2)
    create_answer(text="Раздел имущества при разводе и несогласии сторон производится...", question_id=2)
    create_answer(text="Максимальный срок по УК РФ ст. 105 определяется...", question_id=3)
    create_answer(text="Правило № 1 раздела имущества согласно ГК РФ...", question_id=4)
    create_answer(text="Правило № 2 раздела имущества согласно ГК РФ...", question_id=4)
    create_answer(text="Правило № 3 раздела имущества согласно ГК РФ...", question_id=4)
    create_answer(text="Комиссия при наследстве ответ № 1...", question_id=5)
    create_answer(text="Комиссия при наследстве ответ № 2...", question_id=5)
    create_answer(text="Источник для скачивания 1С № 1...", question_id=6)
    create_answer(text="Источник для скачивания 1С № 2...", question_id=6)
    create_answer(text="Источник для скачивания 1С № 3...", question_id=6)
    create_answer(text="Способ распаковки установочника 1С № 1...", question_id=7)
    create_answer(text="Способ распаковки установочника 1С № 2...", question_id=7)
    create_answer(text="Проверка версии 1С ответ № 1...", question_id=8)
    create_answer(text="Стандартная выгрузка из 1С ответ № 1...", question_id=9)
    create_answer(text="Время выгрузки из 1С ответ № 1...", question_id=10)
    create_answer(text="Время выгрузки из 1С ответ № 2...", question_id=10)
    create_answer(text="Стандарты создания таблиц для учета мат. ценностей в госбюджетных учреждениях № 1...", question_id=11)
    create_answer(text="Стандарты создания таблиц для учета мат. ценностей в госбюджетных учреждениях № 2...", question_id=11)
    create_answer(text="Стандарты создания таблиц для учета мат. ценностей в юридических организациях № 1...", question_id=12)
    create_answer(text="Стандарты создания таблиц для учета мат. ценностей в юридических организациях № 2...", question_id=12)
    create_answer(text="Стандарты создания таблиц для учета мат. ценностей в юридических организациях № 3...", question_id=12)

    print("Тестовые данные созданы!")