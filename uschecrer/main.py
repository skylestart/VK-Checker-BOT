import vk_api
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll
import peewee
import time
from datetime import datetime

class MyLongPoll(VkBotLongPoll):
    def listen(self):
        while True:
            try:
                for event in self.check():
                    yield event
            except Exception as e:
                print(e)


vk_session = vk_api.VkApi(token=tokenstand) #Token Standalone-приложения
tools = vk_api.VkTools(vk_session)
api = vk_session.get_api()

vk = vk_api.VkApi(token=tokengroup) #Token группы вк, от имени которой будет отправляться сообщение
longpoll = MyLongPoll(vk, 218528648)
vks = vk.get_api()

def send(id, text): # Функция отправки сообщения
    vk.method('messages.send', {'user_id': id, 'message': text, 'random_id': 0})


def main(): 
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            msg = event.object.message
            text = msg['text']
            userid = msg['from_id']
            if "/checkuser" in text: #Если пришло сообщение /checkuser
                text = text.split(" ") #Разделение сообщения на аргументы
                if text[0] == "/checkuser": #Если команда - первый аргумент
                    #Бот работает от тега ВК, поэтому проверяем его наличие
                    try:
                        if "@" not in text[1]:
                            send(userid, "Используйте [@tagvk] в качестве второго аргумента!")
                    except:
                        send(userid, "Используйте [@tagvk] в качестве второго аргумента!")
                    else:
                        text = text[1]
                        text = text.split("|")
                        text = text[0]
                        text = text[3:] #Получение ID VK пользователя, чей тег был указан в аргументе команды
                        user = vks.users.get(user_ids=(text),
                                             fields="activities, about,  status, can_post, can_see_audio, exports, career, city, bdate, music, online, activities, can_write_private_message, contacts, followers_count, is_no_index, last_seen, is_no_index")
                        name = vks.users.get(user_ids=(text), name_case="gen", fields="last_name, first_name")
                        try:
                            name = name[0]
                            user = user[0]
                            try:
                                if user['bdate'] != -1:
                                    bdate = user['bdate']
                            except:
                                bdate = 'скрыта'
                            try:
                                if user["followers_count"] != -1:
                                    follows = user["followers_count"]
                            except:
                                follows = "скрыто"
                            try:
                                city = user['city']['title']
                            except:
                                city = "Не указан"
                            platform = user['last_seen']['platform']
                            time = user['last_seen']['time']
                            time = datetime.utcfromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S') #Перевод времени из unixtime в readable date
                            if platform == 1:
                                platform = "мобильного браузера"
                            elif platform == 2:
                                platform = "iPhone"
                            elif platform == 3:
                                platform = "iPad"
                            elif platform == 4:
                                platform = "Android"
                            elif platform == 5:
                                platform = "Windows Phone"
                            elif platform == 6:
                                platform = "Laney (приложение для пк)"
                            elif platform == 7:
                                platform = "компьютера"

                            if user['status'] == "":
                                status = "не установлен"
                            else:
                                user['status'] == status
                            if user['online'] == 1:
                                time = "Онлайн"
                            else:
                                time = time
                            if user['can_write_private_message'] == 1:
                                canwrite = "да"
                            else:
                                canwrite = "нет"                      #В случае, если у пользователя не указан некоторый из запрашиваемых данных, то он не отображается в массиве. Поэтому проверяем
                            if user['is_closed'] == True:
                                is_closed = "закрыта"
                            else:
                                is_closed = 'открыта'
                            if user['is_no_index'] == 1:
                                isindex = "да"
                            else:
                                isindex = "нет"
                            if user['can_see_audio'] == 1:
                                canaudio = "открыта"
                            else:
                                canaudio = "закрыта"
                            if user['can_post'] == 1:
                                canpost = "можно"
                            else:
                                canpost = "нельзя" #Ниже отправляем сообщение с всеми получеными данными
                            send(userid, f"Информация о пользователе: {user['first_name']} {user['last_name']}\n\nСтраница {is_closed}\nМожно написать личное сообщение: {canwrite}\nСтатус: {status}\nГород: {city}\nДата рождения: {bdate}\nМузыка: {canaudio}\nДелать записи на стене {name['first_name']}: {canpost}\nКоличество подписчиков: {follows}\nИндексируется ли профиль поисковыми сайтами: {isindex}\nПоследний раз был в сети: {time} c {platform}")
                        except:
                            send(userid, "Тег ВК введен не верно")
                else:
                    send(userid, "Команда введена не верно!")#Если команда - НЕ первый аргумент







if __name__ == '__main__':
    main()