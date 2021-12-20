import sqlite3
import random
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

conn = sqlite3.connect('vkBot.db', check_same_thread=False)
cursor = conn.cursor()


def new_user_add(user_id):
    """
    Adding new user to the "members" database

    :param user_id:
    :type user_id: str
    :return None:
    """
    request = "INSERT INTO members(id, vk_id) VALUES(" + str(
        len(cursor.execute("SELECT * FROM tags").fetchall()) + 1) + f", \'{user_id}\')"
    cursor.execute(request)
    conn.commit()


def new_tag_add(name_tag):
    """
    Adding new tags to the "tags" database

    :param name_tag:
    :type name_tag: str
    :return None:
    """
    request = "INSERT INTO tags(id, name_tag) VALUES(" + str(
        len(cursor.execute("SELECT * FROM tags").fetchall()) + 1) + f", \'{name_tag}\')"
    cursor.execute(request)
    conn.commit()


def update_value(name_value, value, user_id):
    """
    Update value in "members" database

    :param user_id:
    :param name_value:
    :param value
    :return: None
    """
    if name_value == "step":
        request = f"""UPDATE members SET {name_value} = {value} WHERE vk_id={str(user_id)}"""
    else:
        request = f"UPDATE members SET " + f"'{name_value}'" + f" = '{value}' WHERE vk_id={str(user_id)}"
    cursor.execute(request)
    conn.commit()


def new_registration_user(vk, user_id, first_name, text="empty"):
    """
    Registration user in vk! and message send
    :param text:
    :param vk
    :param user_id
    :param first_name
    :return: None
    """
    keyboard = VkKeyboard(one_time=True)
    if text == "empty":
        keyboard.add_button("Регистрация пользователя", color=VkKeyboardColor.POSITIVE)
    elif text == "/startbot":
        keyboard.add_button("Регистрация пользователя", color=VkKeyboardColor.PRIMARY)
        keyboard.add_button("Поиск людей", color=VkKeyboardColor.POSITIVE)
    keyboard = keyboard.get_keyboard()
    msg = f"🤖 Привет, {first_name}!" + "\n\n" + "Этот бот предназначен для навигации по навыкам выпускников ЗС.\nНажмите на кнопку для выбора следущего шага :"
    vk.messages.send(user_id=user_id,
                     message=msg,
                     keyboard=keyboard,
                     random_id=random.randint(0, 2 ** 64))


def update_value_tag(number, user_id):
    value = f"SELECT members FROM tags WHERE id = {number}"
    value = cursor.execute(value).fetchall()
    if value[0][0] is None:
        value = str(user_id)
    else:
        value = str(value[0][0]) + " " + str(user_id)
    request = f"UPDATE tags SET members = '{value}' WHERE id = {number}"
    cursor.execute(request)
    conn.commit()


def get_members_in_tags(tag_id):
    result = cursor.execute(f"""SELECT * FROM tags WHERE id={tag_id}""").fetchall()[0]
    return result


def list_of_tags_f(vk, user_id):
    dict_of_tags = {i[0]: i[1] for i in cursor.execute("SELECT * FROM tags").fetchall()}
    list_of_tags = "🤖 Список доступных тегов :\n"
    for i in dict_of_tags:
        list_of_tags += str(i) + ": " + str(dict_of_tags[i]) + "\n"

    vk.messages.send(user_id=user_id,
                     message=list_of_tags,
                     random_id=random.randint(0, 2 ** 64))
