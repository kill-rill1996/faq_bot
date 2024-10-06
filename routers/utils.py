import database.services as db


def is_group_already_created(group_title: str) -> bool:
    """Вернет True если группа с таким названием уже создана, иначе False"""
    all_groups = db.get_all_groups()
    for group in all_groups:
        if group.title.lower() == group_title.lower():
            return True
    return False


def is_subgroup_already_created(subgroup_title: str, group_id: int) -> bool:
    """Вернет True если подгруппа с таким названием уже создана, иначе False"""
    all_subgroups = db.get_all_subgroups_by_group_id(group_id)
    for subgroup in all_subgroups:
        if subgroup.title.lower() == subgroup_title.lower():
            return True
    return False


def is_question_already_created(question_title: str, subgroup_id: int) -> bool:
    """Вернет True если вопрос с таким названием уже создан, иначе False"""
    all_questions = db.get_all_questions_by_subgroup_id(subgroup_id)
    for question in all_questions:
        if question.title.lower() == question_title.lower():
            return True
    return False


def is_admin_exists(tg_id: str) -> bool:
    """Проверка на дублирование админа"""
    admin = db.get_admin_by_tg_id(tg_id)
    if admin:
        return True
    return False
