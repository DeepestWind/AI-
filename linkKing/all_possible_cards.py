# S黑桃（spade） H红桃（heart） C梅花（club） D方块（diamond）
import json
import random
import copy
import operator
import numpy
import linkKing.judgeCard

# 中英文对照表
ENG2CH = {
    "Single": "单张",
    "Pair": "对子",
    "Trips": "三张",
    "ThreePair": "三连对",
    "ThreeWithTwo": "三带二",
    "TwoTrips": "钢板",
    "Straight": "顺子",
    "StraightFlush": "同花顺",
    "Bomb": "炸弹",
    "PASS": "过"
}
# 牌到点数的映射
card2num = {
    "SA": 1, "HA": 1, "CA": 1, "DA": 1, "A": 1,
    "S2": 2, "H2": 2, "C2": 2, "D2": 2, "2": 2,
    "S3": 3, "H3": 3, "C3": 3, "D3": 3, "3": 3,
    "S4": 4, "H4": 4, "C4": 4, "D4": 4, "4": 4,
    "S5": 5, "H5": 5, "C5": 5, "D5": 5, "5": 5,
    "S6": 6, "H6": 6, "C6": 6, "D6": 6, "6": 6,
    "S7": 7, "H7": 7, "C7": 7, "D7": 7, "7": 7,
    "S8": 8, "H8": 8, "C8": 8, "D8": 8, "8": 8,
    "S9": 9, "H9": 9, "C9": 9, "D9": 9, "9": 9,
    "ST": 10, "HT": 10, "CT": 10, "DT": 10, "T": 10,
    "SJ": 11, "HJ": 11, "CJ": 11, "DJ": 11, "J": 11,
    "SQ": 12, "HQ": 12, "CQ": 12, "DQ": 12, "Q": 12,
    "SK": 13, "HK": 13, "CK": 13, "DK": 13, "K": 13,
    "SB": 15,  # 小王映射成14，大王映射成15
    "HR": 16,
    "PASS": 0  # PASS 映射成0
}
allCards = [
    "SA", "HA", "CA", "DA",
    "S2", "H2", "C2", "D2",
    "S3", "H3", "C3", "D3",
    "S4", "H4", "C4", "D4",
    "S5", "H5", "C5", "D5",
    "S6", "H6", "C6", "D6",
    "S7", "H7", "C7", "D7",
    "S8", "H8", "C8", "D8",
    "S9", "H9", "C9", "D9",
    "ST", "HT", "CT", "DT",
    "SJ", "HJ", "CJ", "DJ",
    "SQ", "HQ", "CQ", "DQ",
    "SK", "HK", "CK", "DK",
    "SB", "HR",

    "SA", "HA", "CA", "DA",
    "S2", "H2", "C2", "D2",
    "S3", "H3", "C3", "D3",
    "S4", "H4", "C4", "D4",
    "S5", "H5", "C5", "D5",
    "S6", "H6", "C6", "D6",
    "S7", "H7", "C7", "D7",
    "S8", "H8", "C8", "D8",
    "S9", "H9", "C9", "D9",
    "ST", "HT", "CT", "DT",
    "SJ", "HJ", "CJ", "DJ",
    "SQ", "HQ", "CQ", "DQ",
    "SK", "HK", "CK", "DK",
    "SB", "HR", ]


def Create_New_Cards():
    k = 4
    every_len = 27
    card_flag = []
    random_num = []
    index = 0
    for i in range(len(allCards)):
        card_flag.append(True)
        random_num.append(index)
        index += 1
    random.shuffle(random_num)

    result_arr = []
    every_arr = []
    index = 0
    for i in range(0, len(allCards) - 1, every_len):
        index += 1
        for j in range(every_len):
            every_arr.append(allCards[random_num[i]])
            i += 1
        result_arr.append(every_arr)
        every_arr = []
        if index >= k:
            break

    for i in range(len(random_num) - len(result_arr) * every_len):
        result_arr[i].append(allCards[random_num[len(allCards) - 1 - i]])
    return result_arr


'''
result_arr=Create_New_Cards()
result_arr[0].sort()
print(result_arr[0])
rest_cards=result_arr[0]
'''


# result_arr[1].sort()
# result_arr[2].sort()
# result_arr[3].sort()

# print(result_arr[1])
# print(result_arr[2])
# print(result_arr[3])


# for k in sorted(card_count):
# print(k,card_count[k])


# 以下的Find。。。函数中，可用指令删除同类项
def FindAll(rest_cards):
    Single = []
    Pairs = []
    Trips = []
    Bombs = []
    ThreePairs = []
    ThreeWithTwo = []
    TwoTrips = []
    Straight = []
    StraightFlush = []
    AllTypes = {'Single': Single, 'Pairs': Pairs, 'Trips': Trips, 'Bombs': Bombs, 'ThreePairs': ThreePairs,
                'ThreeWithTwo': ThreeWithTwo, 'TwoTrips': TwoTrips, 'Straight': Straight,
                'StraightFlush': StraightFlush}
    Bombs1 = []
    Bombs2 = []
    Bombs3 = []
    Bombs4 = []

    def count(list):
        target_dict = {}
        for item in list:
            item = card2num[item]
            target_dict[item] = target_dict.get(item, 0) + 1

        return target_dict

    card_count = count(rest_cards)  # 获取剩余卡牌的各点数卡牌数量

    # card_count = copy.deepcopy(card_count_copy) #拷贝操作 方便复用

    # 输入一个数字，返回该数字点数的牌面
    def shaixuan(num, list):
        temp = []
        if num >= 2 and num <= 9:
            for card in list:
                if str(num) in card:
                    temp.append(card)
        elif num == 1:
            for card in list:
                if "A" in card:
                    temp.append(card)
        elif num == 10:
            for card in list:
                if "T" in card:
                    temp.append(card)
        elif num == 11:
            for card in list:
                if "J" in card:
                    temp.append(card)
        elif num == 12:
            for card in list:
                if "Q" in card:
                    temp.append(card)
        elif num == 13:
            for card in list:
                if "K" in card:
                    temp.append(card)
        elif num == 15:
            for card in list:
                if card == "SB":
                    temp.append(card)
        elif num == 16:
            for card in list:
                if card == "HR":
                    temp.append(card)
        return temp

    def CardPoint(dict, list):  # 按点数进行分类 形如 6:'D6','D6','C6'
        target_dict = {}
        for item in dict:
            target_dict[item] = shaixuan(item, list)
        return target_dict

    card_points = CardPoint(card_count, rest_cards)

    def clear_same(list):
        if len(list) > 0:
            i = 0
            temp = list[i]
            while temp != list[-1]:
                i += 1
                temp = list[i]

                # print(temp)
                sign = 0
                for j in range(len(list[i])):
                    if list[i][j] != list[i - 1][j]:  # 有不同就改变sign，sign改变过则说明不需要删除
                        sign = 1
                if sign == 0:  # 说明完全相同
                    del list[i - 1]
                    i -= 1
                    temp = list[i]

    def FindSingle():
        for i in card_points:
            if len(card_points[i]) >= 1:
                for j in range(len(card_points[i])):
                    Single.append(card_points[i][j])

    def FindPairs():
        for i in card_points:
            if len(card_points[i]) >= 2:
                for j in range(len(card_points[i]) - 1):
                    for k in range(j + 1, len(card_points[i])):
                        Pairs.append([card_points[i][j], card_points[i][k]])
        clear_same(Pairs)

    def FindTrips():
        for i in card_points:
            if len(card_points[i]) >= 3:
                for j in range(len(card_points[i]) - 2):
                    for k in range(j + 1, len(card_points[i]) - 1):
                        for l in range(k + 1, len(card_points[i])):
                            Trips.append([card_points[i][j], card_points[i][k], card_points[i][l]])
        clear_same(Trips)

    def FindBombs():

        for i in card_points:
            if len(card_points[i]) >= 4:
                for j in range(len(card_points[i]) - 3):
                    for k in range(j + 1, len(card_points[i]) - 2):
                        for l in range(k + 1, len(card_points[i]) - 1):
                            for m in range(l + 1, len(card_points[i])):
                                Bombs1.append(
                                    [card_points[i][j], card_points[i][k], card_points[i][l], card_points[i][m]])

            if len(card_points[i]) >= 5:
                for j in range(len(card_points[i]) - 4):
                    for k in range(j + 1, len(card_points[i]) - 3):
                        for l in range(k + 1, len(card_points[i]) - 2):
                            for m in range(l + 1, len(card_points[i]) - 1):
                                for n in range(m + 1, len(card_points[i])):
                                    Bombs2.append(
                                        [card_points[i][j], card_points[i][k], card_points[i][l], card_points[i][m],
                                         card_points[i][n]])
            if len(card_points[i]) >= 6:
                for j in range(len(card_points[i]) - 5):
                    for k in range(j + 1, len(card_points[i]) - 4):
                        for l in range(k + 1, len(card_points[i]) - 3):
                            for m in range(l + 1, len(card_points[i]) - 2):
                                for n in range(m + 1, len(card_points[i]) - 1):
                                    for o in range(n + 1, len(card_points[i])):
                                        Bombs3.append(
                                            [card_points[i][j], card_points[i][k], card_points[i][l], card_points[i][m],
                                             card_points[i][n], card_points[i][o]])
            if len(card_points[i]) >= 7:
                for j in range(len(card_points[i]) - 6):
                    for k in range(j + 1, len(card_points[i]) - 5):
                        for l in range(k + 1, len(card_points[i]) - 4):
                            for m in range(l + 1, len(card_points[i]) - 3):
                                for n in range(m + 1, len(card_points[i]) - 2):
                                    for o in range(n + 1, len(card_points[i]) - 1):
                                        for p in range(o + 1, len(card_points[i])):
                                            Bombs4.append([card_points[i][j], card_points[i][k], card_points[i][l],
                                                           card_points[i][m], card_points[i][n], card_points[i][o],
                                                           card_points[i], [p]])
        if len(Bombs1) != 0:
            clear_same(Bombs1)
            for i in range(len(Bombs1)):
                Bombs.append(Bombs1[i])
        if len(Bombs2) != 0:
            clear_same(Bombs2)
            for i in range(len(Bombs2)):
                Bombs.append(Bombs2[i])
        if len(Bombs3) != 0:
            clear_same(Bombs3)
            for i in range(len(Bombs3)):
                Bombs.append(Bombs3[i])
        if len(Bombs4) != 0:
            clear_same(Bombs4)
            for i in range(len(Bombs4)):
                Bombs.append(Bombs4[i])

    def FindThreePairs():
        for i in range(len(Pairs)):
            temp = card2num[Pairs[i][0]]
            for j in range(len(Pairs)):
                if card2num[Pairs[j][0]] == temp + 1:
                    for k in range(len(Pairs)):
                        if card2num[Pairs[k][0]] == temp + 2:
                            ThreePairs.append([Pairs[i], Pairs[j], Pairs[k]])

    def FindTwoTrips():
        for i in range(len(Trips)):
            temp = card2num[Trips[i][0]]
            for j in range(len(Trips)):
                if card2num[Trips[j][0]] == temp + 1:
                    TwoTrips.append([Trips[i], Trips[j]])

    def FindThreeWithTwo():
        for i in range(len(Trips)):
            for j in range(len(Pairs)):
                if Pairs[j][0][1] != Trips[i][0][1]:
                    ThreeWithTwo.append([Trips[i], Pairs[j]])

    def FindStraight():
        for i in card_points:
            if i <= 9:  # 只能规定到9 10 J Q K ，带A另外考虑
                for j in range(len(card_points[i])):
                    if i + 1 in card_points:
                        for k in range(len(card_points[i + 1])):
                            if i + 2 in card_points:
                                for l in range(len(card_points[i + 2])):
                                    if i + 3 in card_points:
                                        for m in range(len(card_points[i + 3])):
                                            if i + 4 in card_points:
                                                for n in range(len(card_points[i + 4])):
                                                    Straight.append([card_points[i][j], card_points[i + 1][k],
                                                                     card_points[i + 2][l], card_points[i + 3][m],
                                                                     card_points[i + 4][n]])
            elif i == 10:
                if i + 1 in card_points and i + 2 in card_points and i + 3 in card_points and i + 4 in card_points:
                    for j in range(len(card_points[i])):
                        for k in range(len(card_points[i + 1])):
                            for l in range(len(card_points[i + 2])):
                                for m in range(len(card_points[i + 3])):
                                    for n in range(len(card_points[i + 4])):
                                        Straight.append(
                                            [card_points[i][j], card_points[i + 1][k], card_points[i + 2][l],
                                             card_points[i + 3][m], card_points[i + 4][n]])

    def FindStraightFlush():
        for i in range(len(Straight)):
            if 'H' in Straight[i][0] and 'H' in Straight[i][1] and 'H' in Straight[i][2] and 'H' in Straight[i][
                3] and 'H' in Straight[i][4]:
                StraightFlush.append(Straight[i])
            elif 'S' in Straight[i][0] and 'S' in Straight[i][1] and 'S' in Straight[i][2] and 'S' in Straight[i][
                3] and 'S' in Straight[i][4]:
                StraightFlush.append(Straight[i])
            elif 'C' in Straight[i][0] and 'C' in Straight[i][1] and 'C' in Straight[i][2] and 'C' in Straight[i][
                3] and 'C' in Straight[i][4]:
                StraightFlush.append(Straight[i])
            elif 'D' in Straight[i][0] and 'D' in Straight[i][1] and 'D' in Straight[i][2] and 'D' in Straight[i][
                3] and 'D' in Straight[i][4]:
                StraightFlush.append(Straight[i])

    FindSingle()
    FindPairs()
    FindTrips()
    FindBombs()
    FindThreePairs()
    FindTwoTrips()
    FindThreeWithTwo()
    FindStraight()
    FindStraightFlush()
    _Single = [['Single', i[1], i] for i in Single]
    _Pairs = [['Pair', i[0][1], i] for i in Pairs]
    _Trips = [['Trips', i[0][1], i] for i in Trips]
    _Bombs = [['Bomb', i[0][1], i] for i in Bombs]
    _ThreePairs = [['ThreePair', i[0][1][1], i] for i in ThreePairs]
    _ThreeWithTwo = [['ThreeWithTwo', i[0][1][1], i] for i in ThreeWithTwo]
    _TwoTrips = [['TwoTrips', i[0][1][1], i] for i in TwoTrips]
    _Straight = [['Straight', i[0][1], i] for i in Straight]
    _StraightFlush = [['StraightFlush', i[0][1], i] for i in StraightFlush]
    _AllTypes = {'Single': _Single, 'Pairs': _Pairs, 'Trips': _Trips, 'Bombs': _Bombs, 'ThreePairs': _ThreePairs,
                 'ThreeWithTwo': _ThreeWithTwo, 'TwoTrips': _TwoTrips, 'Straight': _Straight,
                 'StraightFlush': _StraightFlush}
    _AllCards = _Single + _Pairs + _Trips + _Bombs + _ThreePairs + _ThreeWithTwo + _TwoTrips + _Straight + _StraightFlush
    return _AllCards


# 重置card_count 和card_point 并且将各个列表都清空
# def re_set(count, point):
#     card_count.clear()
#     card_points.clear()
#     for i in count:
#         card_count[i] = count[i]
#     for i in point:
#         card_points[i] = point[i]
#     Single.clear()
#     Pairs.clear()
#     Trips.clear()
#     Bombs.clear()
#     ThreePairs.clear()
#     ThreeWithTwo.clear()
#     TwoTrips.clear()
#     Straight.clear()
#     StraightFlush.clear()
#     Bombs1.clear()
#     Bombs2.clear()
#     Bombs3.clear()
#     Bombs4.clear()


# print(f"单张有：{Single}")
# print(f"对子有{Pairs}")
# print(f"三张有{Trips}")
# print(f"三连对有{ThreePairs}")
# print(f"钢板有{TwoTrips}")
# print(f"三带二有{ThreeWithTwo}")
# print(f"炸弹有{Bombs}")  
# print(f"顺子有{Straight}")
# print(f"同花顺有{StraightFlush}")


# 对每个生成牌列表进行格式转换

# print(f"单张有：{_Single}")
# print(f"对子有{_Pairs}")
# print(f"三张有{_Trips}")
# print(f"三连对有{_ThreePairs}")
# print(f"钢板有{_TwoTrips}")
# print(f"三带二有{_ThreeWithTwo}")
# print(f"炸弹有{_Bombs}")  
# print(f"顺子有{_Straight}")
# print(f"同花顺有{_StraightFlush}")
'''
_AllCards = FindAll(rest_cards)
print(f"所有可能牌型有：{_AllCards}")
target=random.choice(_AllCards)
print(target)
#player1
print(f"剩余牌面{rest_cards}")
'''


# def actionList(_target):  # 对接收到的牌面进行生成可打的牌列表，返回一个列表
#     actionlist = []
#     if target[0] != 'PASS' and target[0] != 'tribute' and target[0] != 'back':
#         for i in _AllTypes[target[0]]:
#             if judgeCard.judge(target, i) == 0:
#                 actionlist.append(i)
#         for i in _Bombs:
#             actionlist.append(i)
#         for i in _StraightFlush:
#             actionlist.append(i)
#
#         return actionlist
#     else:
#         pass
    # AllTypes 不可用，直接使用AllCards解决
    # 只用参数

# print(f"对于{target},能打出的牌有：{actionList(target)}")

# print(f"一共有{len(_AllCards)}种牌型")


# All_link
