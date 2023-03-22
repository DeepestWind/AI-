from treelib import *
# S黑桃（spade） H红桃（heart） C梅花（club） D方块（diamond）
import json
from random import *
import copy
import operator
import numpy
from linkKing.judgeCard import *
import time
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
def getValue(Cards):
    num_weight = 0.3  # 牌的数量的权重
    level_weight = 0.3  # 牌级的权重
    model_weight = 0.4  # 牌组本身的价值权重
    num_weight_dic = {"Single": 1, "Pairs": 2, "Trips": 3, "ThreePairs": 6, "ThreeWithTwo": 5, "TwoTrips": 6,
                      "Straight": 5, "StraightFlush": 5, "Bombs": 4, "PASS": 0}
    level_weight_dic = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "T": 10, "J": 11, "Q": 12,
                        "K": 13, "A": 14, "B": 16, "R": 17}
    model_weight_dic = {'Single': 1, 'Pairs': 2, 'Trips': 3, 'ThreePairs': 5, 'ThreeWithTwo': 5.5, 'TwoTrips': 4,
                        'Straight': 5.3, 'Bombs': 20, 'StraightFlush': 8, 'PASS': 0}

    card_value = num_weight * num_weight_dic[Cards[0]] + level_weight * level_weight_dic[Cards[1]] + model_weight * \
                 model_weight_dic[Cards[0]]
    return card_value



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
# orig = ['H9', 'D4', 'SQ', 'S2', 'S6', 'H7', 'HT', 'HQ', 'HQ', 'CJ', 'H5', 'SA', 'DT', 'D8', 'DA', 'H8', 'DJ', 'S2', 'HT', 'S8', 'H6', 'S9', 'DK', 'C2', 'S5', 'H9', 'C8']
# orig=['C4', 'C6', 'C9', 'CA', 'CK', 'CK', 'D3', 'D4', 'D7', 'D8', 'D9', 'DJ', 'DK', 'DQ', 'H3', 'H4', 'H8', 'HA', 'HQ', 'HR', 'S3', 'S4', 'S8', 'S9', 'SA', 'SJ', 'SQ']
# orig=['C2', 'C6', 'C9', 'CA', 'CJ', 'D3', 'D5', 'D9', 'DA', 'DJ', 'DQ', 'H3', 'H4', 'H7', 'H9', 'HJ', 'HJ', 'HQ', 'HR', 'S4', 'S6', 'S9', 'SA', 'SA', 'SB', 'SJ', 'SK']#报错
# orig=['C3', 'C4', 'C8', 'CJ', 'CJ', 'CK', 'D2', 'D4', 'D5', 'D6', 'D7', 'DA', 'H5', 'H7', 'H9', 'HA', 'HQ', 'HR', 'HT', 'S4', 'S5', 'S6', 'S8', 'S9', 'SA', 'SJ', 'ST']
# orig=['C5', 'C7', 'C7', 'C9', 'C9', 'CK', 'CT', 'D3', 'D4', 'D6', 'D6', 'D7', 'DT', 'H3', 'H6', 'H8', 'H9', 'HK', 'HT', 'S3', 'S3', 'S4', 'S6', 'S8', 'SJ', 'SK', 'SQ']
# orig=['D6','HK','D5','HQ','D4','H3','CT','CJ','DJ','C8','H8','D7','D7','H7','HT','ST','C7','S7','C4','C4','H4','DQ','SQ','C5','C5','H5','S5']
# orig=['C3', 'C4', 'C7', 'C8', 'D3', 'D3', 'D4', 'D5', 'D5', 'D8', 'DK', 'DK', 'H3', 'H3', 'H6', 'H7', 'H9', 'HJ', 'S2', 'S3', 'S3', 'S6', 'S8', 'SB', 'SJ', 'SK', 'SQ']
all11=[]
seventimes = []
eighttimes = []
ninetimes = []
tentimes = []
eletimes = []
tweltimes = []
thirtimes = []
def linkKing(orig):
    start = time.perf_counter()
    global seventimes
    global eighttimes
    global ninetimes
    global tentimes
    global eletimes
    global tweltimes
    global thirtimes
    global all11
    all11.clear()
    seventimes.clear()
    eighttimes.clear()
    ninetimes.clear()
    tentimes.clear()
    eletimes.clear()
    tweltimes.clear()
    thirtimes.clear()
    tree = Tree()
    rest = 27
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
                'ThreeWithTwo': ThreeWithTwo, 'TwoTrips': TwoTrips, 'Straight': Straight, 'StraightFlush': StraightFlush}
    Bombs1 = []
    Bombs2 = []
    Bombs3 = []
    Bombs4 = []

    def combo(orig):
        orig.sort()
        rest_cards = orig
        rest_cards_copy = copy.deepcopy(rest_cards)
        def count(list):
            target_dict = {}
            for item in list:
                item = card2num[item]
                target_dict[item] = target_dict.get(item, 0) + 1

            return target_dict


        card_count = count(orig)

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


        card_points = CardPoint(card_count, orig)
        # 以下的Find。。。函数中，可用指令删除同类项
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
                                    Bombs1.append([card_points[i][j], card_points[i][k], card_points[i][l], card_points[i][m]])

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
                                                Bombs4.append(
                                                    [card_points[i][j], card_points[i][k], card_points[i][l], card_points[i][m],
                                                     card_points[i][n], card_points[i][o], card_points[i][p]])
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
                    if Trips[i][0][1] != Pairs[j][0][1]:
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
                                                        Straight.append(
                                                            [card_points[i][j], card_points[i + 1][k], card_points[i + 2][l],
                                                             card_points[i + 3][m], card_points[i + 4][n]])
                elif i == 10:
                    if i + 1 in card_points and i + 2 in card_points and i + 3 in card_points and i + 4 in card_points:
                        for j in range(len(card_points[i])):
                            for k in range(len(card_points[i + 1])):
                                for l in range(len(card_points[i + 2])):
                                    for m in range(len(card_points[i + 3])):
                                        for n in range(len(card_points[i + 4])):
                                            Straight.append([card_points[i][j], card_points[i + 1][k], card_points[i + 2][l],
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


        # 重置card_count 和card_point 并且将各个列表都清空
        def re_set(count, point):
            card_count.clear()
            card_points.clear()
            for i in count:
                card_count[i] = count[i]
            for i in point:
                card_points[i] = point[i]
            Single.clear()
            Pairs.clear()
            Trips.clear()
            Bombs.clear()
            ThreePairs.clear()
            ThreeWithTwo.clear()
            TwoTrips.clear()
            Straight.clear()
            StraightFlush.clear()
            Bombs1.clear()
            Bombs2.clear()
            Bombs3.clear()
            Bombs4.clear()


        def clear_same(list):
            if len(list)!=0:
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
                    # print(f"xiugaihou{list}")

        def FindAll():
            FindSingle()
            FindPairs()
            FindTrips()
            FindBombs()
            FindThreePairs()
            FindTwoTrips()
            FindThreeWithTwo()
            FindStraight()
            FindStraightFlush()


        FindAll()
        Single.sort()
        Pairs.sort()
        Trips.sort()
        ThreePairs.sort()
        TwoTrips.sort()
        ThreeWithTwo.sort()
        Bombs.sort()
        Straight.sort()
        StraightFlush.sort()
        clear_same(Single)
        clear_same(Pairs)
        clear_same(Trips)
        clear_same(ThreePairs)
        clear_same(TwoTrips)
        clear_same(ThreeWithTwo)
        # clear_same(Bombs)
        clear_same(Straight)
        clear_same(StraightFlush)

    combo(orig)
    def clearC():
        Single.clear()
        Pairs.clear()
        Trips.clear()
        Bombs.clear()
        ThreePairs.clear()
        ThreeWithTwo.clear()
        TwoTrips.clear()
        Straight.clear()
        StraightFlush.clear()
        Bombs1.clear()
        Bombs2.clear()
        Bombs3.clear()
        Bombs4.clear()


    tree.create_node(tag='root',identifier='root',data='root')
    flag=0
    sum=1
    total=[]
    while(flag==0):
        global Single_range
        global Pairs_range
        global Trips_range
        global ThreePairs_range
        global TwoTrips_range
        global ThreeWithTwo_range
        global Bombs_range
        global Straight_range
        global StraightFlush_range
        flag=1
        orig2=orig.copy()
        for i in tree.leaves():
            orig1=orig.copy()
            deleteC = []
            for j in tree.rsearch(i.identifier):
                key=tree.get_node(j)

                if key.tag=='root':
                    continue
                elif key.tag=='ThreeWithTwo' or key.tag=='TwoTrips' or key.tag=='ThreePairs':
                    for m in key.data:
                        for n in m:
                            deleteC.append(n)
                elif  key.tag=='Single':
                    deleteC.append(key.data)
                else:
                    for k in key.data:
                        deleteC.append(k)
            # print(deleteC)
            for k in deleteC:
                orig1.remove(k)
            if len(orig1)==0:
                continue
            clearC()#清除所有牌型
            combo(orig1)

            if sum < 5:


                Single_range = len(Single)*(1/(100-sum))
                Straight_range = len(Straight) * (1 / (50- sum*2))

                Pairs_range = len(Pairs)*(1/(22-sum))
                ThreePairs_range = len(ThreePairs)*(1/(22-sum))

                Trips_range = len(Trips)*(1/(22-sum))
                TwoTrips_range = len(TwoTrips) * (1 / (sum))
                if TwoTrips_range>=20:
                    TwoTrips_range*=1/10
                ThreeWithTwo_range = len(ThreeWithTwo)*(1/(50-sum*2))
                Bombs_range = len(Bombs)
                StraightFlush_range = len(StraightFlush)
                # if len(ThreeWithTwo)>150:
                #     ThreeWithTwo_range = len(ThreeWithTwo) * (1 / (40 - sum))
                #     Pairs_range = len(Pairs) * (1 / (20 - sum))
                #     Bombs_range = len(Bombs)//2
                if len(orig2) <=20 and len(orig1)>12:
                    Single_range = len(Single)*(1/(20-sum))
                    Straight_range = len(Straight)*(1/(5-sum))
                    Pairs_range = len(Pairs)*(1/(7-sum))
                    ThreePairs_range = len(ThreePairs)

                    Trips_range = len(Trips)*(1/sum)
                    TwoTrips_range = len(TwoTrips)
                    ThreeWithTwo_range = len(ThreeWithTwo)*(1/(5-sum))
                    Bombs_range = len(Bombs)
                    StraightFlush_range = len(StraightFlush)
                    sum+=10
                if len(orig2)<=12:
                    Single_range = len(Single)
                    Straight_range = len(Straight)

                    Pairs_range = len(Pairs)
                    ThreePairs_range = len(ThreePairs)

                    Trips_range = len(Trips)
                    TwoTrips_range = len(TwoTrips)
                    ThreeWithTwo_range = len(ThreeWithTwo)
                    Bombs_range = len(Bombs)
                    StraightFlush_range = len(StraightFlush)
                    sum+=10
            elif sum>=5 and sum<9:
                Single_range = len(Single) * (1 / (100 - sum))
                Straight_range = len(Straight) * (1 / (22 - sum))

                Pairs_range = len(Pairs) * (1 / (16 - sum))
                ThreePairs_range = len(ThreePairs)

                Trips_range = len(Trips) * (1 / (10 - sum))
                TwoTrips_range = len(TwoTrips) * (1 / (sum))
                ThreeWithTwo_range = len(ThreeWithTwo) * (1/(22-sum))
                if ThreeWithTwo_range>=26:
                    ThreeWithTwo_range*=1/4
                Bombs_range = len(Bombs)

                StraightFlush_range = len(StraightFlush)
            else:
                if len(Bombs)==0 and len(ThreeWithTwo)==0 :
                    if len(Straight)==0:
                        if len(Pairs)==0:
                            if len(Single)==0:
                                Single_range = len(Single)
                                Pairs_range = len(Pairs)
                                Trips_range = len(Trips)
                                ThreePairs_range = len(ThreePairs)
                                TwoTrips_range = len(TwoTrips)
                                ThreeWithTwo_range = len(ThreeWithTwo)
                                Bombs_range = len(Bombs)
                                Straight_range = len(Straight)
                                StraightFlush_range = len(StraightFlush)
                            else:
                                Single_range = 1
                                Pairs_range = len(Pairs)
                                Trips_range = len(Trips)
                                ThreePairs_range = len(ThreePairs)
                                TwoTrips_range = len(TwoTrips)
                                ThreeWithTwo_range = len(ThreeWithTwo)
                                Bombs_range = len(Bombs)
                                Straight_range = len(Straight)
                                StraightFlush_range = len(StraightFlush)
                        else:
                            Single_range = 0
                            Pairs_range =1
                            Trips_range = len(Trips)
                            ThreePairs_range = len(ThreePairs)
                            TwoTrips_range = len(TwoTrips)
                            ThreeWithTwo_range = len(ThreeWithTwo)
                            Bombs_range = len(Bombs)
                            Straight_range = len(Straight)
                            StraightFlush_range = len(StraightFlush)
                    else:
                        Single_range = 0
                        Pairs_range = 0
                        Trips_range = len(Trips)
                        ThreePairs_range = len(ThreePairs)
                        TwoTrips_range = len(TwoTrips)
                        ThreeWithTwo_range = len(ThreeWithTwo)
                        Bombs_range = len(Bombs)
                        Straight_range = len(Straight)
                        StraightFlush_range = len(StraightFlush)
                else:
                    Single_range=0
                    Pairs_range =0
                    Trips_range = len(Trips)
                    ThreePairs_range = len(ThreePairs)
                    TwoTrips_range = len(TwoTrips)
                    ThreeWithTwo_range = len(ThreeWithTwo)
                    Bombs_range = len(Bombs)
                    Straight_range = len(Straight)
                    StraightFlush_range = len(StraightFlush)
            ks=0
            end=time.perf_counter()
            if start-end>=25:
                return 0
            for s in sample(Single, int(Single_range)):
                flag=0
                node1 = Node(tag='Single', data=s)
                tree.add_node(node1, parent=i.identifier)
            for s in sample(Pairs,int(Pairs_range)):
                flag = 0
                node1 = Node(tag='Pairs', data=s)
                tree.add_node(node1, parent=i.identifier)
            for s in sample(Trips,int(Trips_range)):
                flag = 0
                node1 = Node(tag='Trips', data=s)
                tree.add_node(node1, parent=i.identifier)
            for s in sample(ThreePairs,int(ThreePairs_range)):
                flag = 0
                node1 = Node(tag='ThreePairs', data=s)
                tree.add_node(node1, parent=i.identifier)
            for s in sample(TwoTrips,int(TwoTrips_range)):
                flag = 0
                node1 = Node(tag='TwoTrips', data=s)
                tree.add_node(node1, parent=i.identifier)
            for s in sample(ThreeWithTwo,int(ThreeWithTwo_range)):
                flag = 0
                node1 = Node(tag='ThreeWithTwo', data=s)
                tree.add_node(node1, parent=i.identifier)
            for s in sample(Bombs,int(Bombs_range)):
                flag = 0
                node1 = Node(tag='Bombs', data=s)
                tree.add_node(node1, parent=i.identifier)
            for s in sample(Straight,int(Straight_range)):
                flag = 0
                node1 = Node(tag='Straight', data=s)
                tree.add_node(node1, parent=i.identifier)
            for s in sample(StraightFlush,int(StraightFlush_range)):
                flag = 0
                node1 = Node(tag='StraightFlush', data=s)
                tree.add_node(node1, parent=i.identifier)
        sum+=1
        print(sum)
        print(len(tree.leaves()))
    deleteC = []
    for i in tree.leaves():
        _score = 0
        for j in tree.rsearch(i.identifier):
            key=tree.get_node(j)
            sc = []
            if key.tag=='root':
                continue
            elif key.tag=='ThreeWithTwo' or key.tag=='TwoTrips' or key.tag=='ThreePairs':

                if key.tag=='ThreeWithTwo' or key.tag=='TwoTrips':
                    k=[]
                    for m in key.data:
                        for n in m:
                            k.append(n)
                    deleteC.append(k)
                    del k
                    sc.append(key.tag)
                    sc.append(key.data[0][0][1])
                    sc.append(key.data)
                    _score+=getValue(sc)
                else:
                    k = []
                    for m in key.data:
                        for n in m:
                            k.append(n)
                    deleteC.append(k)
                    del k
                    sc.append(key.tag)
                    sc.append(key.data[0][0][1])
                    sc.append(key.data)
                    _score+=getValue(sc)
            elif  key.tag=='Single':
                deleteC.append([key.data])
                sc.append(key.tag)
                sc.append(key.data[1])
                sc.append(key.data)
                _score+=getValue(sc)
            else:
                if key.tag=='Bombs':
                    deleteC.append(key.data)
                    sc.append(key.tag)
                    sc.append(key.data[0][1])
                    sc.append(key.data)
                    _score+=getValue(sc)
                elif key.tag=='Pairs':
                    deleteC.append(key.data)
                    sc.append(key.tag)
                    sc.append(key.data[0][1])
                    sc.append(key.data)
                    _score+=getValue(sc)
                elif key.tag=='Trips':
                    deleteC.append(key.data)
                    sc.append(key.tag)
                    sc.append(key.data[0][1])
                    sc.append(key.data)
                    _score+=getValue(sc)
                elif key.tag=='Straight':
                    deleteC.append(key.data)
                    sc.append(key.tag)
                    sc.append(key.data[0][1])
                    sc.append(key.data)
                    _score += getValue(sc)
                else:
                    deleteC.append(key.data)
                    sc.append(key.tag)
                    sc.append(key.data[0][1])
                    sc.append(key.data)
                    _score+=getValue(sc)
            sc.clear()
        # deleteC.append('\t')
        deleteC.append(_score/((tree.level(i.identifier)+1)))
        # print(deleteC)
        all11.append(deleteC.copy())
        # if tree.level(i.identifier)==7:
        #     seventimes.append(deleteC.copy())
        # if tree.level(i.identifier)==8:
        #     eighttimes.append(deleteC.copy())
        # if tree.level(i.identifier)==9:
        #     ninetimes.append(deleteC.copy())
        # if tree.level(i.identifier) == 10:
        #     tentimes.append(deleteC.copy())
        # if tree.level(i.identifier)==11:
        #     eletimes.append(deleteC.copy())
        # if tree.level(i.identifier)==12:
        #     tweltimes.append(deleteC.copy())
        # if tree.level(i.identifier) == 13:
        #     thirtimes.append(deleteC.copy())
        deleteC.clear()

    # seventimes=sorted(seventimes,key=lambda x:x[-1],reverse=True)
    # eighttimes=sorted(eighttimes,key=lambda x:x[-1],reverse=True)
    # ninetimes=sorted(ninetimes,key=lambda x:x[-1],reverse=True)
    # tentimes=sorted(tentimes,key=lambda x:x[-1],reverse=True)
    # eletimes=sorted(eletimes,key=lambda x:x[-1],reverse=True)
    # tweltimes=sorted(tweltimes,key=lambda x:x[-1],reverse=True)
    # thirtimes=sorted(thirtimes,key=lambda x:x[-1],reverse=True)

    del tree
    all11= sorted(all11, key=lambda x: x[-1], reverse=True)
    # with open("jiayou.txt", "a") as f:
    #     for i in all11:
    #         for j in i:
    #             if type(j)==float:
    #                 f.write(str(j))
    #                 continue
    #             for k in j:
    #                 f.write(str(k))
    #                 f.write(" ")
    #             f.write("* ")
    #         f.write("\n")
    # return all11
    for i in all11:
        print(i)
    return all11
    # for i in seventimes:
    #     print(i)
    # print()
    # for i in eighttimes:
    #     print(i)
    # print()
    # for i in ninetimes:
    #     print(i)
    # print()
    # for i in tentimes:
    #     print(i)
    # print()
    # for i in eletimes:
    #     print(i)
    # print()
    # for i in tentimes:
    #     print(i)
    # print()
    # for i in eletimes:
    #     print(i)
    # print()
    # for i in tweltimes:
    #     print(i)
    # print()
    # for i in thirtimes:
    #     print(i)
    # print()

# linkKing(orig=['S3', 'D3', 'D4', 'S5', 'S5', 'H5', 'H6', 'C6', 'S7', 'H7', 'H8', 'S9', 'H9', 'C9', 'HT', 'HJ', 'CJ', 'DQ'])
#不会组10 J Q

# orig=['S3', 'D3', 'D4', 'S5', 'S5', 'H5', 'H6', 'C6', 'S7', 'H7', 'H8', 'S9', 'H9', 'C9', 'HT', 'HJ', 'CJ', 'DQ']
# orig=orig.sort()
# print(orig)



