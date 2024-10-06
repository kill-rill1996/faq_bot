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


def get_questions_to_delete(questions: list[tables.Question], creation: bool = False) -> str:
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


def get_answers_to_delete(answers: list[tables.Answer], quest_text: str) -> str:
    result = f"Выберите <b>номер</b> ответа из списка  на вопрос: <b>{quest_text}</b>\n\n"

    count = 1
    for answer in answers:
        result += f"<b>{count}.</b> {answer.text}\n"
        count += 1

    return result


def get_questions_text(questions: list[tables.Question]) -> str:
    """Список вопросов для отдельного создания вопросов"""
    result = "Выберите <b>номер</b> вопроса из списка:\n\n"

    count = 1
    for quest in questions:
        result += f"<b>{count}.</b> {quest.title}\n"
        count += 1

    return result


def get_help_message() -> str:
    """Help message"""
    message = "<b>Возможности бота:</b>\n" \
              "- Отвечает на вопросы и по бухгалтерии\n" \
              "- Имеет возможность добавления новых тематических разделов и вопросов (функция доступна только для администраторов)\n\n" \
              "<b>Инструкция использования:</b>\n" \
              "- Для начала работы отправьте команду /start и следуйте инструкциям\n" \
              "- Чтобы найти ответ на интересующий вопрос отправьте команду /answers или нажмите на кнопку во вкладке 'Меню', последовательно выберите группу, подгруппу и вопрос\n" \
              "- Используйте команду /help для получения информации о функционале бота\n\n" \
              "<b>Для администраторов:</b>\n" \
              "- Используйте команды /add_group, /add_subgroup, /add_question и /add_answer для создания групп, подгрупп, вопросов и ответов на них\n" \
              "- Используйте команду /delete_answer для удаления ответов на вопросы\n" \
              "- Используйте команды /add_admin и /delete_admin для добавления нового и удаления существующего администратора\n\n" \
              "<b>Контакт поддержки:</b>\n" \
              "Если у вас есть вопросы или предложения, свяжитесь с нашей поддержкой в телеграм: @Buhgalter_Rf"
    return message


