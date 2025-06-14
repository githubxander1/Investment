
# 登录微信

# 发送文本消息给文件传输助手
import itchat
wechat_user = 'filehelper'  # 文件传输助手
itchat.auto_login(hotReload=False)

def send_wechat_message(candidates):
    itchat.auto_login(hotReload=False)
    message = "今日精选股池:\n\n" + candidates.to_string(index=False)
    itchat.send(message, toUserName='filehelper')


# # 可选：发送图片
# # itchat.send_image("daily_hot_stocks.png", toUserName=wechat_user)
# from WeChatPYAPI import WeChatPY
# wechat = WeChatPY()
#
# # 登录微信
# wechat.login_wx()
#
# # 发送文本消息
# wechat.send_text_msg(to_user="filehelper", content="今日精选股池：" + candidates.to_string(index=False))
