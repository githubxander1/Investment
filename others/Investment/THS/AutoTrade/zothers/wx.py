import itchat

# 登录微信
# itchat.auto_login(hotReload=True)

def login_callback():
    print("登录成功")

def exit_callback():
    print("退出登录")

# 登录微信.get_friends(update=True)
itchat.auto_login(hotReload=True, loginCallback=login_callback)
# itchat.auto_login(hotReload=True, loginCallback=login_callback, exitCallback=exit_callback)


# 获取好友列表
friends = itchat.get_friends(update=True)

# 打印好友列表
for friend in friends:
    print(friend['NickName'])

# 获取所有群聊
# groups = itchat.get_chatrooms(update=True)
# print(groups)
#
# # 获取所有群聊成员
# members = itchat.get_members(update=True)
#
# # 获取所有公众号
# mp_friends = itchat.get_mps(update=True)
# print(mp_friends)

# # 获取所有聊天记录
# messages = itchat.search_messages(update=True)
#
# # 获取所有未读消息
# unread = itchat.search_chats()

# 发送文本消息
# itchat.send('Hello, World!', 'filehelper')
#
# # 发送图片消息
# itchat.send_image('path/to/image.jpg', 'filehelper')