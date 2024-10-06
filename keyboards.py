from typing import List

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database import tables


def select_group_keyboard(groups: List[tables.Group]) -> InlineKeyboardBuilder:
    """Создание клавиатуры для выбора группы"""
    keyboard = InlineKeyboardBuilder()
    for g in groups:
        keyboard.row(InlineKeyboardButton(text=f"{g.title}", callback_data=f"{g.id}"))

    keyboard.adjust(2)
    keyboard.row(InlineKeyboardButton(text="❌ Отмена", callback_data=f"cancel"))
    return keyboard


def select_subgroup_keyboard(subgroups: List[tables.SubGroup]) -> InlineKeyboardBuilder:
    """Создание клавиатуры для выбора подгруппы"""
    keyboard = InlineKeyboardBuilder()
    for sg in subgroups:
        keyboard.row(InlineKeyboardButton(text=f"{sg.title}", callback_data=f"{sg.id}"))

    keyboard.adjust(2)
    keyboard.row(InlineKeyboardButton(text="<< Назад", callback_data=f"back_to-group"))
    keyboard.row(InlineKeyboardButton(text="❌ Отмена", callback_data=f"cancel"))
    return keyboard


def select_question_keyboard(questions: List[tables.Question]) -> InlineKeyboardBuilder:
    """Создание клавиатуры для выбора вопроса"""
    keyboard = InlineKeyboardBuilder()

    count = 1
    for q in questions:
        keyboard.row(InlineKeyboardButton(text=f"{count}", callback_data=f"{q.id}"))
        count += 1
    keyboard.adjust(3)

    keyboard.row(InlineKeyboardButton(text="<< Назад", callback_data=f"back_to-subgroup"))
    keyboard.row(InlineKeyboardButton(text="❌ Отмена", callback_data=f"cancel"))
    return keyboard


def back_to_question_keyboard() -> InlineKeyboardBuilder:
    """Создание клавиатуры для возвращения назад от пустого вопроса"""
    keyboard = InlineKeyboardBuilder()

    keyboard.row(InlineKeyboardButton(text="<< Назад", callback_data=f"back_to-question"))
    keyboard.row(InlineKeyboardButton(text="❌ Отмена", callback_data=f"cancel"))
    return keyboard


def create_group_keyboard(groups: List[tables.Group]) -> InlineKeyboardBuilder:
    """Создание клавиатуры для создания группы"""
    keyboard = InlineKeyboardBuilder()
    for g in groups:
        keyboard.row(InlineKeyboardButton(text=f"{g.title}", callback_data=f"{g.id}"))

    keyboard.adjust(2)
    keyboard.row(InlineKeyboardButton(text="❌ Отмена", callback_data=f"cancel"))
    return keyboard


def create_subgroup_keyboard(subgroups: List[tables.SubGroup]) -> InlineKeyboardBuilder:
    """Создание клавиатуры для создания подгруппы"""
    keyboard = InlineKeyboardBuilder()
    for sg in subgroups:
        keyboard.row(InlineKeyboardButton(text=f"{sg.title}", callback_data=f"{sg.id}"))

    keyboard.adjust(2)
    keyboard.row(InlineKeyboardButton(text="❌ Отмена", callback_data=f"cancel"))
    return keyboard


def create_question_keyboard(questions: List[tables.Question]) -> InlineKeyboardBuilder:
    """Создание клавиатуры для создания вопроса"""
    keyboard = InlineKeyboardBuilder()

    count = 1
    for q in questions:
        keyboard.row(InlineKeyboardButton(text=f"{count}", callback_data=f"{q.id}"))
        count += 1
    keyboard.adjust(3)

    keyboard.row(InlineKeyboardButton(text="❌ Отмена", callback_data=f"cancel"))
    return keyboard


def all_admins_keyboard(admins: list) -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()
    for admin in admins:
        text = ""
        if admin.phone:
            text += admin.phone
        else:
            text += admin.tg_id
        keyboard.row(InlineKeyboardButton(text=text, callback_data=f"delete_{admin.id}"))

    keyboard.row(InlineKeyboardButton(text="❌ Отмена", callback_data=f"cancel"))
    return keyboard


def confirm_keyboard() -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()
    keyboard.row(InlineKeyboardButton(text="Да", callback_data=f"confirm_yes"))
    keyboard.row(InlineKeyboardButton(text="Нет", callback_data=f"confirm_no"))
    keyboard.adjust(2)
    keyboard.row(InlineKeyboardButton(text="❌ Отмена", callback_data=f"cancel"))
    return keyboard


def select_group_to_delete_keyboard(groups: List[tables.Group]) -> InlineKeyboardBuilder:
    """Создание клавиатуры для выбора группы"""
    keyboard = InlineKeyboardBuilder()
    for g in groups:
        keyboard.row(InlineKeyboardButton(text=f"{g.title}", callback_data=f"{g.id}"))

    keyboard.adjust(2)
    keyboard.row(InlineKeyboardButton(text="❌ Отмена", callback_data=f"cancel"))
    return keyboard


def select_subgroup_to_delete_keyboard(subgroups: List[tables.SubGroup]) -> InlineKeyboardBuilder:
    """Создание клавиатуры для выбора подгруппы"""
    keyboard = InlineKeyboardBuilder()
    for sg in subgroups:
        keyboard.row(InlineKeyboardButton(text=f"{sg.title}", callback_data=f"{sg.id}"))

    keyboard.adjust(2)
    keyboard.row(InlineKeyboardButton(text="<< Назад", callback_data=f"back_to-groups"))
    keyboard.row(InlineKeyboardButton(text="❌ Отмена", callback_data=f"cancel"))
    return keyboard


def select_question_to_delete_keyboard(questions: List[tables.Question]) -> InlineKeyboardBuilder:
    """Создание клавиатуры для выбора вопроса"""
    keyboard = InlineKeyboardBuilder()

    count = 1
    for q in questions:
        keyboard.row(InlineKeyboardButton(text=f"{count}", callback_data=f"{q.id}"))
        count += 1
    keyboard.adjust(3)

    keyboard.row(InlineKeyboardButton(text="<< Назад", callback_data=f"back_to-subgroups"))
    keyboard.row(InlineKeyboardButton(text="❌ Отмена", callback_data=f"cancel"))
    return keyboard


def select_answer_to_delete_keyboard(answers: List[tables.Answer]) -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()

    count = 1
    for answer in answers:
        keyboard.row(InlineKeyboardButton(text=f"{count}", callback_data=f"{answer.id}"))
        count += 1
    keyboard.adjust(3)

    keyboard.row(InlineKeyboardButton(text="<< Назад", callback_data=f"back_to-questions"))
    keyboard.row(InlineKeyboardButton(text="❌ Отмена", callback_data=f"cancel"))
    return keyboard


def back_to_question_delete_keyboard() -> InlineKeyboardBuilder:
    """Создание клавиатуры для возвращения назад от пустого вопроса"""
    keyboard = InlineKeyboardBuilder()

    keyboard.row(InlineKeyboardButton(text="<< Назад", callback_data=f"back_to-questions"))
    keyboard.row(InlineKeyboardButton(text="❌ Отмена", callback_data=f"cancel"))
    return keyboard


def cancel_keyboard() -> InlineKeyboardBuilder:
    """Клавиатура для отмены создания ответа"""
    keyboard = InlineKeyboardBuilder()
    keyboard.row(InlineKeyboardButton(text="❌ Отмена", callback_data=f"cancel"))
    return keyboard




