from database import tables


def get_questions(questions: list[tables.Question], creation: bool = False) -> str:
    """Возвращает список вопросов enum"""
    if not questions:
        if creation:
            return "В этом разделе пока нет вопросов, отправьте вопрос текстом."
        else:
            return "В этом разделе пока нет вопросов."

    if creation:
        result = "Выберите <b>номер</b> вопроса или отправьте вопрос <b>текстом</b>, чтобы создать новый:\n\n"
    else:
        result = "Выберите <b>номер</b> вопроса из списка:\n\n"

    count = 1
    for quest in questions:
        result += f"<b>{count}.</b> {quest.title}\n"
        count += 1

    return result

