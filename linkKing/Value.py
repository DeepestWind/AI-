import copy

from linkKing import all_possible_cards

card_value_init = {"A": 14, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "T": 10, "J": 11, "Q": 12,
                   "K": 13, "B": 15, "R": 16}

card_value = {}
CurrentPoint = "2"
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


def init(cur_rank: str):
    global CurrentPoint, card_value
    CurrentPoint = cur_rank  # 等级更新
    card_value = card_value_init.copy()  # 初始化card_value

    start = card_value[CurrentPoint]
    for k, v in card_value.items():  # 更新card_value
        if start < v < 15:
            card_value[k] = v - 1

    card_value[CurrentPoint] = 14

    print("当前牌值为：{}".format(card_value))


def find_same(cards1, cards2):
    same_cards = []
    for i in cards1:
        if i in cards2:
            same_cards.append(i)
    return same_cards


def TonghuaSunPoint(cards):  # 同花顺得分（传递过来的玩家牌组）
    gailv = 1 / 13
    result = 0
    all_cards = all_possible_cards.FindAll(cards)
    tonghuasun = []
    new_tonghuasun = []
    for i in all_cards:
        if i[0] == 'StraightFlush':
            tonghuasun.append(i)
    # print("同花顺前：",tonghuasun)
    for i in tonghuasun:
        if new_tonghuasun.count(i) < 1:
            new_tonghuasun.append(i)
    new_tonghuasun.sort(key=lambda x: card2num[x[1]], reverse=True)  # 将它从大到小进行排序
    # print("没有操作前：同花顺：",new_tonghuasun)
    dic = {}
    for i in cards:
        if i in dic:
            dic[i] = 2
        else:
            dic.setdefault(i, 1)
    delete_cards = []
    for i in range(0, (len(new_tonghuasun) - 1)):
        if len(new_tonghuasun) != 1:  # 防止下标越界操作
            if card2num[new_tonghuasun[i][1]] - card2num[new_tonghuasun[i + 1][1]] <= 4:
                same_cards = find_same(new_tonghuasun[i][2], new_tonghuasun[i + 1][2])
                flag = True
                for j in same_cards:
                    if dic[j] != 2:
                        flag = False
                        break
                if not flag:
                    lst = copy.deepcopy(new_tonghuasun[i + 1])

                    delete_cards.append(lst)
    # print('dic:',dic)
    for i in delete_cards:
        new_tonghuasun.remove(i)
    # print("操作后：",new_tonghuasun)
    for i in new_tonghuasun:
        jiazhi = 69 + card_value[i[1]]
        result = result + gailv * jiazhi
    return result


def DangDuiPoint(cards, current_point):  # 单对(牌组，当前打的分值牌)
    sum_score = 0  # 记当局分值牌几张
    sum1 = 0  # 记小王几张
    sum2 = 0  # 记大王几张
    gailv = (1.0 * 1) / 54  # 概率
    jiazhi = 12  # 价值
    result = 0  # 最后得分
    for i in range(len(cards)):
        if cards[i][1] == current_point:
            sum_score = sum_score + 1
        if cards[i] == 'SB':
            sum1 = sum1 + 1
        if cards[i] == 'HR':
            sum2 = sum2 + 1
    if sum_score == 2 or sum_score == 3:
        result = gailv * jiazhi
    if sum_score == 4 or sum_score == 5:
        result = gailv * jiazhi * 2
    if sum_score == 6 or sum_score == 7:
        result = gailv * jiazhi * 3
    if sum_score == 8:
        result = gailv * jiazhi * 4
    if sum1 == 2:
        jiazhi = 13
        result += gailv * jiazhi
    if sum2 == 2:
        jiazhi = 14
        result += gailv * jiazhi
    return result


def BombPoint(cards):  # 炸弹得分
    result = 0
    S = []
    new_Cards = []
    for i in range(len(cards)):
        new_Cards.append(cards[i][1])
    new_Cards.sort()
    for i in new_Cards:
        if i not in S:
            if new_Cards.count(i) == 4:
                gailv = 1 / 26
                jiazhi = 43 + card_value[i]
                result += gailv * jiazhi
                S.append(i)
            if new_Cards.count(i) > 4:
                num = new_Cards.count(i)
                gailv = 1 / 13
                jiazhi = 43 + (num - 4) * 13 + 1 * card_value[i]
                result += gailv * jiazhi
                S.append(i)
    return result


def ThreeZhangPoint(cards):  # 三张得分
    result = 0
    gailv = (1.0 * 1) / 26
    S = []
    new_Cards = []
    for i in range(len(cards)):
        new_Cards.append(cards[i][1])
    new_Cards.sort()
    # print(new_Cards)
    for i in new_Cards:
        if new_Cards.count(i) >= 3:
            if i not in S:
                jiazhi = card_value[i]
                result = result + jiazhi * gailv
                S.append(i)
    return result


def DangZhang(cards):  # 单张(大小王)
    sum_score = 0
    for i in range(len(cards)):
        if cards[i] == 'HR':
            sum_score = sum_score + (1.0 * 1) / 108 * 14
        if cards[i] == 'SB':
            sum_score = sum_score + (1.0 * 1) / 108 * 13
    return sum_score


def Score(cards):
    n_1 = DangZhang(cards)  # 单张
    n_2 = ThreeZhangPoint(cards)  # 三张
    n_3 = BombPoint(cards)  # 炸弹
    n_4 = DangDuiPoint(cards, CurrentPoint)  # 单对
    n_5 = TonghuaSunPoint(cards)  # 同花顺
    sum_score = n_1 + n_2 + n_3 + n_4 + n_5  # 总分
    return sum_score
