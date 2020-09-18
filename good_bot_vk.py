from vk_api import VkApi #python ver.(2.7-3.7)
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import requests, random
from bs4 import BeautifulSoup
import numpy as np
import datetime
import time

vk_session = VkApi(token="fc20224f088b91e889f7df4f51bb0e222a369d654eb577f1d21ecc5145601724c94229e8f6896e2140007") #token_API
longpoll = VkBotLongPoll(vk_session, "192416672") #id группы
vk = vk_session.get_api()
keyboard = VkKeyboard(one_time=True)
                
keyboard.add_button('1',color=VkKeyboardColor.PRIMARY,payload=None )
keyboard.add_button('2', color=VkKeyboardColor.PRIMARY)
keyboard.add_button('3', color=VkKeyboardColor.PRIMARY)
keyboard.add_button('4', color=VkKeyboardColor.PRIMARY)

keyboard.add_line()  # Переход на вторую строку
keyboard.add_location_button()

keyword = ' '
name = 'Имя'

minutes = 0 #время для таймера

def extract_name(line):
    result = ""
    not_skip = True
    for i in list(line):
        if not_skip:
            if i == "<":
                not_skip = False
            else:
                result += i
        else:
            if i == ">":
                not_skip = True
    return result.split()[0]

def _get_user_name_from_vk_id(user_id):
    request = requests.get("https://vk.com/id"+str(user_id))
    bs = BeautifulSoup(request.text, "html.parser")
    
    #user_name = _clean_all_tag_from_str(bs.findAll("title")[0]) 
    user_name = (bs.find_all("title")[0])
    #print(extract_name(user_name))

    #return user_name.split()[0]
    return extract_name(user_name)

slovar = np.genfromtxt("W:\\progect\\dataset.txt",dtype='str')               

for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat:
        if event.object.text.lower() == 'правила':
            vk.messages.send(peer_id = event.object['peer_id'], message="[Бот выбирает 4 слова и присылает в лс]", random_id=0)
        if event.object.text.lower() == 'игра': # пишешь игра в чат и в лс получаешь 4 варианта
            name = _get_user_name_from_vk_id(event.object.from_id)
            vk.messages.send(peer_id = event.object['peer_id'], message = name + " Выбирает слово...", random_id=0)
            a  = np.array(random.sample(range(0, 34010), 4))
            vk.messages.send(peer_id = event.object.from_id, message = "1. "+ slovar[a[0]] + " 2. " + slovar[a[1]] + " 3. " + slovar[a[2]] + " 4. " + slovar[a[3]] , random_id=0, keyboard=keyboard.get_keyboard())
            for _ in range(60):
                minutes+=1
                time.sleep(1)
        if event.object.text.lower() == keyword:
            name = _get_user_name_from_vk_id(event.object.from_id)
            vk.messages.send(peer_id = event.object['peer_id'], message= name + " Победил", random_id=0)
            keyword = " "
        if event.object.text.lower() != keyword and minutes > 20 and keyword != ' ':
            vk.messages.send(peer_id = event.object['peer_id'], message = "Время истекло, правильное слово " + keyword , random_id=0)
            keyword = " "
    if event.type == VkBotEventType.MESSAGE_NEW and event.from_user:
            if event.type == VkBotEventType.MESSAGE_NEW and event.object.text == '1':
                keyword = slovar[a[0]]
            elif event.type == VkBotEventType.MESSAGE_NEW and event.object.text == '2':
                keyword = slovar[a[1]]
            elif event.type == VkBotEventType.MESSAGE_NEW and event.object.text == '3':
                keyword = slovar[a[2]]
            elif event.type == VkBotEventType.MESSAGE_NEW and event.object.text == '4':
                keyword = slovar[a[3]]
                
                







        