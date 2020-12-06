import vk_api, traceback, random as r
from vk_api.longpoll import VkEventType, VkLongPoll

TOKEN_ME = "" #vkme token

vk_me = vk_api.VkApi(token=TOKEN_ME)
longpoll = VkLongPoll(vk_me)

def sms(p=None,t=None):
    vk_me.method('messages.send', {'peer_id': p, 'message': t, 'random_id': r.randint(1,2048)})


def edit_msg(peer_id, textsend, evv, textlink=''):
    vk_me.method("messages.edit",
                 {"peer_id": peer_id,
                  "message": textsend,
                  "message_id": evv,
                  "attachment": textlink})


def kick_msg(chat_id, user_id):
    vk_me.method('messages.removeChatUser', {'chat_id': chat_id, 'user_id': user_id})


def reply(e):
    x = vk_me.method('messages.getById', {'message_ids': e})
    reply = x["items"][0]["reply_message"]
    return reply


def nam(ids):
    usero = vk_me.method('users.get', {'user_ids': ids})[0]
    name = usero['first_name'] + ' ' + usero['last_name']
    result = f'@id{ids} ({name})'
    return result


def join(chat_id, user_id):
    vk_me.method('messages.addChatUser',
                 {'chat_id': chat_id,
                  'user_id': user_id})
while True:
    try:
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.from_me:
                cm = event.text
                p = event.peer_id
                mid = event.message_id
                us = event.user_id
                chat_id = p - 2000000000
                pf = 'у'
                try:
                    if event.raw[6]['mentions']:
                        vk_id = str(event.raw[6]['mentions'][0])
                    else:
                        vk_id = str(reply(mid)['from_id'])
                except:
                    pass
                if cm == f'{pf} пинг':
                    try:
                        sms(p=p,t='пОнГ\nКря-Кря я работаю')
                    except Exception as eror:
                        continue
                if cm == f'{pf} утка':
                    edit_msg(p, f' 🦆', mid)
                if cm == f'{pf} хе':
                    edit_msg(p, f' 🌚', mid)
                if cm == f'{pf} камень':
                    edit_msg(p,f'👉👈',mid)
                if cm == f'{pf} хе':
                    edit_msg(p,f'👉👈',mid)
                if cm.startswith(f'{pf} вернуть'):
                    try:
                        join(chat_id, vk_id)
                    except:
                        edit_msg(p, f'| Алё где айди ёпт', mid)
                if cm.startswith(f'{pf} кик'):
                    try:
                        kick_msg(chat_id, vk_id)
                    except:
                        edit_msg(p, f'| Не достаточно полномочий для кика {nam(vk_id)}', mid)
    except Exception as eror:
        traceback.print_exc()
