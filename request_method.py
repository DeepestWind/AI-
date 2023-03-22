# -*- coding: utf-8 -*-
# @Time       : 2021/09/05
# @Author     : yanggang yangguang
# @Description: 对接掼蛋游戏平台接口

import requests
import websocket
import json
# 解析状态
import globalValues
import strategy
from state import State

# 账号、密码部分根据报名后反馈的邮件给予的账密进行修改
# 桌子和座位，按照测试的实际情况进行修改
# 账号(user_name),密码(pwd),选择桌子(table_id),座位(indexes)(请根据自己的实现修改该部位代码)
user_name = '100'
pwd = '100'
table_id = 0
indexes = 0

# 请求路径
url_head = "http://221.226.81.54:41003/"
url = url_head + "Login"

# 登录并记录cookies
session = requests.session()
f = session.post(url, {'user_name': user_name, 'pwd': pwd})
cookie_jar = f.cookies
print("登录反馈信息：", json.loads(f.text))
# cookie格式转换
cookie = requests.utils.dict_from_cookiejar(cookie_jar)
print(cookie)


# 定义websocket连接回调函数
# 连接到服务器, 触发on_open事件
def on_open(ws):
    # 1.加入游戏大厅
    print("on_open:加入")
    db = {
        'class': 'operation',
        'handler': 'hall',
        'module': 'add',
    }
    ws.send(json.dumps(db))


# 服务器推送数据
def on_message(ws, message):
    message = json.loads(str(message))

    # 游戏进入阶段
    if message['class'] == 'operation':
        if message['handler'] == 'hall':
            if message['module'] == 'add' and message['code'] == 1000:
                # 成功进入大厅
                # 2.加入牌桌,选择桌子(table_id)和座位(indexes)
                ws.send(json.dumps({
                    'class': 'operation',
                    'handler': 'card_table',
                    'module': 'add',
                    'table_id': table_id,
                    'indexes': indexes,

                }))
        if message['handler'] == 'card_table':
            if message['module'] == 'add' and message['code'] == 1000:
                # 成功进入牌桌
                # 3.准备游戏
                ws.send(json.dumps({
                    'class': 'game',
                    'sign': '1',
                }))

    # 游戏开始阶段
    if message['class'] == 'game':
        if 'sign' not in message:
            # 调用状态对象来解析状态
            msg=State.parse(message)

        # message游戏信息,可观察通知消息等
        # 出牌动作
        if "actionList" in message:
            # TODO: 可以出的牌型服务器已经给出（和去年类似），再通过算法得出actIndex类似于去年的action
            actIndex = strategy.act(globalValues.person.my_pos, message["actionList"], message["indexRange"])

            # ***4.出牌动作(请根据自己的实现使用message信息,输出actIndex反馈服务器)***
            # "actIndex":反馈服务器AI所选出牌组合的ID,当前案例脚本反馈最大出牌组合ID(message["indexRange"])
            ws.send(json.dumps({'class': 'game',
                                "sign": "0",
                                "actIndex": actIndex}))

        if "type" in message:
            # 小局结束,准备状态
            if message["type"] == "notify" and message["stage"] == "episodeOver":
                # 5.小局结束,准备游戏
                ws.send(json.dumps({'class': 'game',
                                    "sign": "1"}))
            # 6.对战结束
            if message["type"] == "notify" and message["stage"] == "gameResult":
                ws.on_close()
                pass


# 程序报错
def on_error(ws, error):
    print("error: ", error)


def on_close(ws):
    print("on_close ")


# 开启调试信息
websocket.enableTrace(True)
# cookie数据格式整理
cookie_str = ""
for key, value in cookie.items():
    cookie_str = key + "=" + value + ";"

# 创建websocket连接
ws = websocket.WebSocketApp("ws://221.226.81.54:41003/PlayGameClass",
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close,
                            cookie=cookie_str)
ws.on_open = on_open
ws.run_forever()
