# -*- encoding: utf-8 -*-
# @Time       : 2021/10/17 下午6:35
# @Author     : Tongqing Zhu
# @File       : strategy.py 
# @Description: 控牌策略

import random
from globalValues import *
from information import *
from linkKing import Value
import linkKing.Link as link

mypos=0
def getpos(_mypos):
    global mypos
    mypos=_mypos
def go(action1,msg):
    global mypos
    action_list=action1.copy()
    card_value = {"A": 13, "2": 1, "3": 2, "4": 3, "5": 4, "6": 5, "7": 6, "8": 7, "9": 8, "T": 9, "J": 10,
                  "Q": 11, "K": 12, "B": 15, "R": 16}
    card_value[msg["curRank"]]=14
    if len(msg["actionList"])==1:
        return 0
    else:
        if msg['stage']=='back':
            return 1
        if msg['greaterPos']==mypos or msg['greaterPos']==-1:
            for p in action_list:
                if p[0]=="ThreePair" or p[0]=="ThreeWithTwo" or p[0]== "TwoTrips" or p[0]=="Straight" or p[0]=="Bomb" or p[0]=="Trips" or p[0]=="Pair":
                    link1 = link.linkKing(msg["handCards"].copy())
                    for i in link1:
                        i.reverse()
                        for j in i:
                            if type(j) == float:
                                continue
                            for k in range(1,len(action_list)):
                                j.sort()
                                action_list[k][2].sort()
                                if j==action_list[k][2]:
                                    if len(j)==5 or len(j)==6:
                                        print(action_list[k][2])
                                        deletec=msg["handCards"].copy()
                                        for d in action_list[k][2]:
                                            deletec.remove(d)
                                        if len(deletec)==2 or len(deletec)==3:
                                            link2=link.linkKing(deletec)
                                            for b in link2:
                                                if len(b)==2:
                                                    return k
                                                else:
                                                    continue
                                        else:
                                            if action_list[k][1]=='A' or action_list[k][1]==msg['curRank']:
                                                continue
                                            else:
                                                return k

                                    else:
                                        continue
                    else:
                        return 1
                else:
                    continue
            else:#只有单张和对子
                for i in action_list:
                    if i[0]=="Pair":
                        if i[1]=="A" or i[1]==msg['curRank'] or i[1]=='R' or i[1]=='B':
                            continue
                        else:
                            return action_list.index(i)
                else:
                    return 1

        if msg['greaterPos']==(mypos+2)%4:
            if len(msg["handCards"])<=5:
                link1 = link.linkKing(msg["handCards"])
                for i in link1:
                    if len(i)==2 or len(i)==1:
                        for j in i:
                            if type(j) == float:
                                continue
                            for k in range(1, len(action_list)):
                                j.sort()
                                action_list[k][2].sort()
                                if j == action_list[k][2]:
                                    return k
                    else:
                        continue
                else:
                    return 0
            if msg['greaterAction'][0]=="Single" or msg['greaterAction'][0]=="Pair":
                if card_value[msg['greaterAction'][1]]<7:
                    link1 = link.linkKing(msg["handCards"])
                    for i in link1:
                        for j in i:
                            if type(j) == float:
                                continue
                            for k in range(1, len(action_list)):
                                j.sort()
                                action_list[k][2].sort()
                                if j == action_list[k][2]:
                                    return k
                    else:
                        return 1
                else:
                    return 0
            else:
                value = msg['greaterAction'][1]
                print(value)
                if card_value[value] < 6:
                    for p in range(len(action_list)):
                        if action_list[p][0] == "Bomb" or action_list[p][0] == "StraightFlush":
                            return p - 1
                    else:
                        return (len(action_list) - 1)
                else:
                    return 1
        else:
            for p in action_list:
                if p[0]=="ThreePair" or p[0]=="ThreeWithTwo" or p[0]== "TwoTrips" or p[0]=="Straight" or p[0]=="Bomb" or p[0]=="Trips" or p[0]=="Pair":
                    link1 = link.linkKing(msg["handCards"].copy())
                    for i in link1:
                        i.reverse()
                        for j in i:
                            if type(j) == float:
                                continue
                            for k in range(1,len(action_list)):
                                j.sort()
                                action_list[k][2].sort()
                                if j==action_list[k][2]:
                                    if len(j)==5 or len(j)==6:
                                        print(action_list[k][2])
                                        deletec=msg["handCards"].copy()
                                        for d in action_list[k][2]:
                                            deletec.remove(d)
                                        if len(deletec)==2 or len(deletec)==3:
                                            link2=link.linkKing(deletec)
                                            for b in link2:
                                                if len(b)==2:
                                                    return k
                                                else:
                                                    continue
                                        else:
                                            if action_list[k][1]=='A' or action_list[k][1]==msg['curRank']:
                                                continue
                                            else:
                                                return k

                                    else:
                                        continue
                    else:
                        return 1
                else:
                    continue
            else:#只有单张和对子
                for i in action_list:
                    if i[0]=="Pair":
                        if i[1]=="A" or i[1]==msg['curRank'] or i[1]=='R' or i[1]=='B':
                            continue
                        else:
                            return action_list.index(i)
                else:
                    return 1
            # if msg['greaterAction'][0] == "Bomb" or msg['greaterAction'][0]=="StraightFlush":
            #     if len(msg['handCards'])>18:
            #         return 0
            #     else:
            #         return 1
            # else:
            #     value=msg['greaterAction'][1]
            #     print(value)
            #     x=0
            #     if  card_value[value]<6:
            #         act1=action_list.copy()
            #         act1.reverse()
            #         for p in range(len(act1)-1):
            #             if act1[p][1]!=act1[p+1][1]:
            #                 if action_list[(len(act1)-1-p)][0]=="Bomb" or action_list[(len(act1)-1-p)][0]=="StraightFlush":
            #                     continue
            #                 else:
            #                     return len(act1)-1-p
            #         else:
            #             return 1
            #     else:
            #          if action_list[1][0]=='Bomb' or action_list[1][0]=='StraightFlush':
            #              if len(msg['handCards'])>18:
            #                  return 0
            #              else:
            #                  return 1
            #          else:
            #             return 1

