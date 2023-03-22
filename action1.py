# -*- coding: utf-8 -*-
# @Time       : 2020/10/1 21:32
# @Author     : Duofeng Wu
# @File       : action.py
# @Description: 动作类

from random import randint
import globalValues
import strategy


class Action(object):

    def __init__(self):
        """
        初始化
        """
        self.action = []
        self.act_range = -1

    def parse(self, msg):
        """
        解析信息
        1、获取出牌列表
        2、获取出牌索引上限
        3、获取出牌
        :param msg: 消息字典
        :return:出牌索引
        """
        self.action = msg["actionList"]
        # print(msg)
        self.act_range = msg["indexRange"]
        print(self.action)
        index = eval(input("可选动作范围为：0至{}\n".format(self.act_range)))
        return index
