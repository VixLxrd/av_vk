from function_file import new_tag_add as new_tag, new_user_add as new_user, update_value as update_v
from function_file import new_registration_user as new_reg_user
from function_file import update_value_tag as update_tag
from function_file import get_members_in_tags as get_mit
from function_file import list_of_tags_f
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import random
import sqlite3

TOKEN = "b79d7adce685daea38dba6fb4da1add9dd6d567ad8bf593948cdb2ef5a60a9f204502482f2fdf74d20f34"
group_id = 196670048

conn = sqlite3.connect('vkBot.db', check_same_thread=False)
cursor = conn.cursor()


# tags = [i[1] for i in cursor.execute("SELECT * FROM tags").fetchall()]
# [{'first_name': 'Владислав', 'id': 358712250, 'last_name': 'Очнев', 'can_access_closed': True, 'is_closed': False}]

def main():
    vk_session = vk_api.VkApi(token=TOKEN)
    vk = vk_session.get_api()
    print(1)
    for event in VkBotLongPoll(vk_session, group_id).listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            try:
                text = event.obj.message['text'].lower()
                print(text)
                user_id = event.obj.message['from_id']
                first_name = vk.users.get(user_ids=user_id)[0]['first_name']
                if vk.groups.isMember(group_id=group_id, user_id=user_id):
                    result = cursor.execute(
                        """SELECT step FROM members WHERE vk_id=""" + str(user_id)).fetchall()
                    # if text != "/startbot":
                    #     pass
                    # el
                    if len(result) == 0:
                        new_user(user_id)
                        update_v("step", 0, user_id)
                        new_reg_user(vk, user_id, first_name)
                    else:
                        step = result[0][0]
                        if text == "/startbot":
                            update_v("step", 1, user_id)
                            new_reg_user(vk, user_id, first_name, "/startbot")
                        elif step == 0:
                            if text == "регистрация пользователя":
                                update_v("step", 3, user_id)
                                vk.messages.send(user_id=user_id,
                                                 message=f"🤖 {first_name}, указанные данные не будут подлежать передаче и разглашению." + "\n\n" + "Введите ваше ФИО полностью :",
                                                 random_id=random.randint(0, 2 ** 64))
                            else:
                                update_v("step", 0, user_id)
                                new_reg_user(vk, user_id, first_name, "/startbot")
                        elif step == 3:
                            update_v("step", 4, user_id)
                            update_v("full_name", text, user_id)
                            vk.messages.send(user_id=user_id,
                                             message=f"🤖 {first_name}, введите вашу дату рождения." + "\n\n" + "Формат данных дд.мм.гггг :",
                                             random_id=random.randint(0, 2 ** 64))
                        elif step == 4:
                            update_v("step", 5, user_id)
                            update_v("birthday", text, user_id)
                            vk.messages.send(user_id=user_id,
                                             message=f"🤖 {first_name}, введите ваш номер телефона." + "\n\n" + "Формат данных +79536061463 :",
                                             random_id=random.randint(0, 2 ** 64))
                        elif step == 5:
                            update_v("step", 6, user_id)
                            update_v("phone", text, user_id)
                            vk.messages.send(user_id=user_id,
                                             message=f"🤖 {first_name}, введите название учебного заведения, в котором вы сейчас учитесь." + "\n\n" + "Если на данный момент вы не учитесь, напишите 'не учусь' :",
                                             random_id=random.randint(0, 2 ** 64))
                        elif step == 6:
                            update_v("step", 7, user_id)
                            update_v("edu_inst", text, user_id)
                            vk.messages.send(user_id=user_id,
                                             message=f"🤖 {first_name}, теперь напишите немного о себе." + "\n\n" + "Напишите об умениях и навыках, которыми вы бы могли помочь ассоциации, и/или хотели бы научиться.\nПожалуйста, уместите всю информацию в одно сообщение :",
                                             random_id=random.randint(0, 2 ** 64))
                        elif step == 7:
                            update_v("step", 8, user_id)
                            update_v("about", text, user_id)
                            vk.messages.send(user_id=user_id,
                                             message=f"""🤖 {first_name}, выберите теги, соответствующие вашему роду занятий и/или хотели бы научиться.""",
                                             random_id=random.randint(0, 2 ** 64))

                            dict_of_tags = {i[0]: i[1] for i in cursor.execute("SELECT * FROM tags").fetchall()}
                            list_of_tags = ""
                            for i in dict_of_tags:
                                list_of_tags += str(i) + ": " + str(dict_of_tags[i]) + "\n"

                            vk.messages.send(user_id=user_id,
                                             message=list_of_tags,
                                             random_id=random.randint(0, 2 ** 64))

                            keyboard = vk_api.keyboard.VkKeyboard(one_time=True)
                            keyboard.add_button("Добавить новый тег")
                            keyboard = keyboard.get_keyboard()
                            vk.messages.send(user_id=user_id,
                                             message=f"🤖 Напишите номера тегов в порядке возрастания через пробел." + "\n\n" + "Если соответствующего тега не существует, нажмите кнопку 'Добавить новый тег' :",
                                             keyboard=keyboard,
                                             random_id=random.randint(0, 2 ** 64))
                        elif step == 8:
                            if text == "добавить новый тег":
                                update_v("step", 9, user_id)
                                vk.messages.send(user_id=user_id,
                                                 message=f"🤖 {first_name}, напишите название нового тега." + "\n\n" + "Перед тем как написать, хорошо подумайте над названием",
                                                 random_id=random.randint(0, 2 ** 64))
                            else:
                                print(text)
                                tags_input = text.split()
                                print(tags_input)
                                update_v("tags", ' '.join(tags_input), user_id)

                                for elem in tags_input:
                                    update_tag(elem, user_id)
                                vk.messages.send(user_id=user_id,
                                                 message=f"🤖 Спасибо, {first_name}, регистрация закончена!" + "\n\n" + "Теперь напиши : /startBot",
                                                 random_id=random.randint(0, 2 ** 64))
                        elif step == 9:
                            new_tag(text)
                            vk.messages.send(user_id=user_id,
                                             message="🤖 Новый тeг добавлен!",
                                             random_id=random.randint(0, 2 ** 64))
                            update_v("step", 8, user_id)
                            vk.messages.send(user_id=user_id,
                                             message=f"""🤖 {first_name}, выберите теги, соответствующие вашему роду занятий и/или хотели бы научиться.""",
                                             random_id=random.randint(0, 2 ** 64))
                            list_of_tags_f(vk, user_id)
                            keyboard = vk_api.keyboard.VkKeyboard(one_time=True)
                            keyboard.add_button("Добавить новый тег")
                            keyboard = keyboard.get_keyboard()
                            vk.messages.send(user_id=user_id,
                                             message=f"🤖 {first_name}, напишите номера тегов в порядке возрастания через пробел." + "\n\n" + "Если соответствующего тега не существует, нажмите кнопку 'Добавить новый тег' :",
                                             keyboard=keyboard,
                                             random_id=random.randint(0, 2 ** 64))
                        elif step == 10:
                            if text == "назад":
                                update_v("step", 1, user_id)
                                new_reg_user(vk, user_id, first_name, "/startbot")
                            else:
                                update_v("step", 3, user_id)
                                vk.messages.send(user_id=user_id,
                                                 message=f"🤖 {first_name}, указанные данные не будут подлежать передаче и разглашению." + "\n\n" + "Введите ваше ФИО полностью :",
                                                 random_id=random.randint(0, 2 ** 64))
                        elif step == 11:
                            list_of_tags = text.split()
                            data_output = ""
                            for tag in list_of_tags:
                                db_info = get_mit(tag)
                                data_output += f"{tag}: {db_info[1]}" + "\n"
                                list_index = str(db_info[2]).split()
                                for member in list_index:
                                    full_name = cursor.execute(f"SELECT full_name FROM members WHERE vk_id={member}").fetchall()[0][0]
                                    data_output += "\t" + str(list_index.index(member) + 1) + ": @id" + str(member) + f" ({full_name})" + "\n"
                                data_output += "\n"

                            vk.messages.send(user_id=user_id,
                                             message="Подходящие вам люди:",
                                             random_id=random.randint(0, 2 ** 64))
                            if not data_output:
                                vk.messages.send(user_id=user_id,
                                                 message="К сожалению, нет подходящих людей :(",
                                                 random_id=random.randint(0, 2 ** 64))
                            else:
                                vk.messages.send(user_id=user_id,
                                                 message=data_output,
                                                 random_id=random.randint(0, 2 ** 64))
                            list_of_tags_f(vk, user_id)
                            vk.messages.send(user_id=user_id,
                                             message="Напишите номера тегов в порядке возрастания через пробел, или напишите /startBot",
                                             random_id=random.randint(0, 2 ** 64))
                        elif step == 1:
                            print(901)
                            if text == "регистрация пользователя":
                                print(90)
                                update_v("step", 10, user_id)
                                keyboard = vk_api.keyboard.VkKeyboard(one_time=True)
                                keyboard.add_button("Назад")
                                keyboard.add_button("Заполнить анкету заново")
                                keyboard = keyboard.get_keyboard()
                                result = cursor.execute(
                                    """SELECT * FROM members WHERE vk_id=""" + str(user_id)).fetchall()[0]

                                if not result[2]:
                                    data = "🤖 Вы еще не заполнили анкету :("
                                else:
                                    data = f"ФИО: {result[3]}" + "\n" + f"Дата рождения: {result[5]}" + "\n" + f"Номер телефона: {result[4]}" + "\n" + f"Учебное заведение: {result[6]}" + "\n" + f"О себе: {result[7]}" + "\n" + f"Теги: {result[8]}"

                                vk.messages.send(user_id=user_id,
                                                 message="🤖 Ваша анкета:\n" + data,
                                                 keyboard=keyboard,
                                                 random_id=random.randint(0, 2 ** 64))
                            elif text == "поиск людей":
                                update_v("step", 11, user_id)
                                list_of_tags_f(vk, user_id)
                                vk.messages.send(user_id=user_id,
                                                 message="🤖 Напишите номер тегов в порядке возрастания через пробел.",
                                                 random_id=random.randint(0, 2 ** 64))
                            else:
                                vk.messages.send(user_id=user_id,
                                                 message="🤖 Введите /startBot для работы с ботом",
                                                 random_id=random.randint(0, 2 ** 64))
                else:
                    print("else")
            except Exception as e:
                vk.messages.send(user_id=user_id,
                                 message="🤖 Произошла ошибка. Напишите /startBot",
                                 random_id=random.randint(0, 2 ** 64))
                print(e)




while True:
    try:
        if __name__ == '__main__':
            main()
    except Exception as E:
        print(E)
