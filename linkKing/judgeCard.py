# 14为逢人配
def judge(_cards1, _cards2, super='2'):  # （己方牌，对方牌，登基牌）右边为对方的牌，左边我自己的牌，如果<= 返回0，反之返回1
    card_value = {"A": 13, "2": 1, "3": 2, "4": 3, "5": 4, "6": 5, "7": 6, "8": 7, "9": 8, "T": 9, "J": 10,
                  "Q": 11, "K": 12, "B": 15, "R": 16}
    if _cards1[0] == "Bomb" or _cards1[0] == "StraightFlush":
        if (_cards2[0] != "Bomb" and _cards2[0] != "StraightFlush") or _cards1[1] == 'B':
            return 1
        else:
            if _cards2[1] == 'B':
                return 0
            else:
                sum_1 = len(_cards1[2])
                sum_2 = len(_cards2[2])
                if sum_2 == 5:
                    if _cards1[0] != "StraightFlush" and _cards2[0] != "StraightFlush":
                        if sum_1 == sum_2:
                            card_value[super] = 14
                            if card_value[_cards1[1]] > card_value[_cards2[1]]:
                                return 1
                            else:
                                return 0
                        elif sum_1 < sum_2:
                            return 0

                        else:
                            return 1
                    elif _cards1[0] != "StraightFlush" and _cards2[0] == "StraightFlush":
                        if sum_1 > 5:
                            return 1
                        else:
                            return 0
                    elif _cards1[0] == "StraightFlush" and _cards2[0] == "StraightFlush":
                        if _cards2[1] == "A":
                            if _cards1[1] != "A":
                                return 1
                            else:
                                return 0
                        else:
                            if _cards1[1] == "A":
                                return 0
                            else:
                                if card_value[_cards1[1]] > card_value[_cards2[1]]:
                                    return 1
                                else:
                                    return 0
                    else:
                        return 1
                elif sum_2 < 5:
                    if sum_1 >= 5:
                        return 1
                    else:
                        card_value[super] = 14
                        if card_value[_cards1[1]] > card_value[_cards2[1]]:
                            return 1
                        else:
                            return 0
                else:
                    if sum_1 <= 5:
                        return 0
                    else:
                        if sum_1 < sum_2:
                            return 0
                        elif sum_1 > sum_2:
                            return 1
                        else:
                            card_value[super] = 14
                            if card_value[_cards1[1]] > card_value[_cards2[1]]:
                                return 1
                            else:
                                return 0

    else:
        if _cards2[0] == "Bomb" or _cards2[0] == "StraightFlush":
            return 0
        else:
            if _cards2[0] == "ThreePair" or _cards2[0] == "TwoTrips" or _cards2[0] == "Straight":
                if _cards2[1] == "A":
                    if _cards1[1] != "A":
                        return 1
                    else:
                        return 0
                else:
                    if _cards1[1] == "A":
                        return 0
                    else:
                        if card_value[_cards1[1]] > card_value[_cards2[1]]:
                            return 1
                        else:
                            return 0
            else:
                card_value[super] = 14
                if card_value[_cards1[1]] > card_value[_cards2[1]]:
                    return 1
                else:
                    return 0
