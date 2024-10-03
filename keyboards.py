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
    keyboard.row(InlineKeyboardButton(text="Отмена", callback_data=f"cancel"))
    return keyboard


def select_subgroup_keyboard(subgroups: List[tables.SubGroup]) -> InlineKeyboardBuilder:
    """Создание клавиатуры для выбора подгруппы"""
    keyboard = InlineKeyboardBuilder()
    for sg in subgroups:
        keyboard.row(InlineKeyboardButton(text=f"{sg.title}", callback_data=f"{sg.id}"))

    keyboard.adjust(2)
    keyboard.row(InlineKeyboardButton(text="<< Назад", callback_data=f"back_to-group"))
    keyboard.row(InlineKeyboardButton(text="Отмена", callback_data=f"cancel"))
    return keyboard


def select_question_keyboard(questions: List[tables.Question]) -> InlineKeyboardBuilder:
    """Создание клавиатуры для выбора вопроса"""
    keyboard = InlineKeyboardBuilder()
    for q in questions:
        keyboard.row(InlineKeyboardButton(text=f"{q.title}", callback_data=f"{q.id}"))

    keyboard.row(InlineKeyboardButton(text="<< Назад", callback_data=f"back_to-subgroup"))
    keyboard.row(InlineKeyboardButton(text="Отмена", callback_data=f"cancel"))
    return keyboard


def pagination_questions_keyboard(current_page: int, num_pages: int) -> InlineKeyboardBuilder:
    """Keyboard for message pagination"""
    keyboard = InlineKeyboardBuilder()
    keyboard.row(InlineKeyboardButton(text="<", callback_data=f"pagination_prev_{current_page}_{num_pages}"))
    keyboard.row(InlineKeyboardButton(text=">", callback_data=f"pagination_next_{current_page}_{num_pages}"))
    keyboard.adjust(2)
    return keyboard

