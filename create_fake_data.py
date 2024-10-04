from database.services import create_group, create_answer, create_question, create_subgroup


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


create_fake_data()