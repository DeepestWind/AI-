from typing import List

from linkKing.Value import Score
from globalValues import card2num


class PersonalInformation(object):
    def __init__(self):
        self.my_pos = None  # 自己的座位号
        self.hand_card: List[str] = []  # 手牌
        # self.strength = None  # 牌力

    def set_pos(self, pos):
        """
        设置当前位置
        :param pos: 键入值
        """
        self.my_pos = pos
        # self.strength = Score(self.hand_card)
        # print(f"牌力：{self.strength}")

    def update_card(self, card):
        """
        更新当前手牌
        :param card: 键入手牌值
        """
        self.hand_card = card.copy()


class CardRecord(object):

    def __init__(self):
        self.card_recorder_reverse = None  # 逆向记牌器：其余三家还有多少牌
        self.card_recorder = None  # 正向记牌器：已经出了牌的个数
        self.all_cards = None  # 每人已经出的牌
        self.all_times = None  # 每人出手次数
        self.rest = None  # 每人剩余手牌数量

    def init_card_recorder(self, lst):
        """
        记牌器初始化
        :param lst: 初始手牌
        """
        self.card_recorder_reverse = [0, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 2, 2]
        self.card_recorder = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        self.all_cards = [[], [], [], []]
        self.all_times = [0, 0, 0, 0]
        self.rest = [0, 0, 0, 0]

        for i in lst:
            self.card_recorder_reverse[card2num[i]] -= 1

        print("记牌器：{}".format(self.card_recorder_reverse))

    def update_card_tribute(self, tribute_pos, receive_tribute_pos, card):
        if tribute_pos == person.my_pos:  # 进贡为自己
            self.card_recorder_reverse[card2num[card]] += 1
        if receive_tribute_pos == person.my_pos:  # 被别人进贡
            self.card_recorder_reverse[card2num[card]] -= 1

    def update_card_back(self, back_pos, receive_back_pos, card):
        if back_pos == person.my_pos:  # 回贡为自己
            self.card_recorder_reverse[card2num[card]] += 1
        if receive_back_pos == person.my_pos:  # 被别人回贡
            self.card_recorder_reverse[card2num[card]] -= 1

    def update_card_recorder(self, cur_pos, cur_action):
        """
        更新记牌器
        :param cur_pos: 当前玩家位置
        :param cur_action: 出牌情况
        """

        # lst = eval(cur_action)  # 字符串转队列
        lst = cur_action  # 获取出牌情况

        self.all_times[cur_pos] += 1  # 出手次数

        if lst[2] == "PASS" or cur_pos == person.my_pos:  # 不出牌或自己出牌，跳过记牌
            return

        for i in lst[2]:
            self.card_recorder_reverse[card2num[i]] -= 1
            self.card_recorder[card2num[i]] += 1  # 更新记牌器
            self.all_cards[cur_pos].append(i)  # 更新记录的出牌

        # 输出更新内容
        print("记牌器：{}".format(self.card_recorder_reverse))
        print("当前玩家出手次数：{}".format(self.all_times[cur_pos]))
        print("当前玩家已出牌：{}".format(self.all_cards[cur_pos]))

    def update_rest(self, public_info):
        """
        更新每家剩余手牌数量
        :param public_info: 公共信息
        """
        for i in range(4):
            self.rest[i] = public_info[i]["rest"]
            print("位置{}处的手牌数量为{}".format(i, self.rest[i]), end='')
        print()


person = PersonalInformation()  # 个人信息类

record = CardRecord()  # 记牌器类
