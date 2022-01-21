#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 20 00:40:17 2021

@author: apple
"""

class Pitcher:
    def __init__(self, name):
        self.name = name
        self.strike = 0
        self.ball = 0
        self.er = 0
        self.k = 0
        self.o = 0
        self.go = 0
        self.ao = 0
        self.bb = 0
        self.h = 0
        self.hr = 0
    def ip(self): #投球局數
        ip = self.o // 3 + self.o % 3 / 10
        return ip
    def pitch(self): #總投球數
        pitch = self.strike + self.ball
        return pitch
        
class Batter:
    def __init__(self, name, batnum):
        self.name = name
        self.batnum = batnum
        self.single = 0
        self.double = 0
        self.triple = 0
        self.homerun = 0
        self.rbi = 0
        self.runs = 0
        self.bb = 0
        self.so = 0
        self.go = 0
        self.ao = 0
    def h(self): #總安打數
        h = self.single + self.double + self.triple + self.homerun
        return h
    def ab(self): #打數
        ab = self.h() + self.so + self.go + + self.ao
        return ab
    def pa(self): #打席
        pa = self.ab() + self.bb
        return pa

def numberkeyin(i): #確認輸入是否為數字
    try:
        return int(input(i))
    except:
        print('請輸入正整數！')
        return numberkeyin(i)

def listtostr(i): #列表內容去括號
    return ', '.join(map(str, i))
  
def onepa(pit, pited, bat): #一打席結果
    atbat = bat.pop(0)
    print('場上投手為{}, {}準備上場打擊'.format(pit[0].name, atbat.name))
    s , b = 0 , 0
    while True:
        print("目前球數：{}好球,{}壞球".format(s, b))
        p = str(input('請輸入此球結果(S:好球,B:壞球,F:界外,Ｈ:安打,AO:高飛,GO:滾地,O:選項)：'))
        result = p.lower()
        base = 0
        if result == 'o':
            option = str(input('請輸入選項(P:場上投手數據,B:場上打者數據,C:換投,或任意鍵返回):'))
            o = option.lower()
            if o == 'p':
                print("{}：IP:{}, H:{}, ER:{}, BB:{}, SO:{}, 球數:{}({}好,{}壞)\n"
                      .format(pit[0].name, pit[0].ip(), pit[0].h,
                              pit[0].er, pit[0].bb, pit[0].k,
                              pit[0].pitch(), pit[0].strike, pit[0].ball))
                continue
            elif o == 'b':
                print("{}棒 {}：AB:{}, R:{}, H:{}, Hr:{}, RBI:{}, BB:{}, SO:{}\n"
                      .format(atbat.batnum, atbat.name, atbat.ab(), atbat.runs,
                              atbat.h(), atbat.homerun, atbat.rbi, atbat.bb, atbat.so)) 
                continue
            elif o == 'c':
                chpit = str(input('請輸入接替投手姓名或輸入"C"取消:'))
                if chpit == 'c' or chpit == 'C':
                    print('取消換投！')
                    continue
                else:
                    check = str(input('場上投手{}更換為{},確認要更換嗎？(Y:確認,或任意鍵返回):'
                                      .format(pit[0].name, chpit)))
                    if check == 'y' or check == 'Y':
                        print('投手更換為{}'.format(chpit))
                        pited.append(pit.pop(0))
                        pit.append(Pitcher(chpit))     
                        continue
                    else:
                        print('取消換投！')
                        continue
            else:
                continue          
        elif result == 's':
            s += 1
            pit[0].strike += 1
            if s == 3:
                pit[0].k += 1
                pit[0].o += 1
                atbat.so += 1
                print('三振！')
                break
        elif result == 'f':
            if s < 2:
                s += 1
                pit[0].strike += 1
            else:
                pit[0].strike += 1
        elif result == 'b':
            b += 1
            pit[0].ball += 1
            if b == 4:
                pit[0].bb += 1
                atbat.bb += 1
                base = 1
                print('四壞保送！')
                break
        elif result == 'h':
            base = numberkeyin('請輸入安打結果(1:一壘,2:二壘,3:三壘,4:全壘打)：')
            if base == 1:
                atbat.single += 1
                pit[0].h += 1
                pit[0].strike += 1
                print('一壘安打！')
            elif base == 2:
                atbat.double += 1
                pit[0].h += 1
                pit[0].strike += 1
                print('二壘安打！')
            elif base == 3:
                atbat.triple += 1
                pit[0].h += 1
                pit[0].strike += 1
                print('三壘安打！')
            elif base == 4:
                atbat.homerun += 1
                pit[0].hr += 1
                pit[0].h += 1
                pit[0].strike += 1
                print('全壘打！')
            else:
                print('輸入錯誤！')
                continue
            break
        elif result == 'ao':
            pit[0].o += 1
            pit[0].strike += 1
            pit[0].ao += 1
            atbat.ao += 1
            print('高飛球出局！')
            break
        elif result == 'go':
            pit[0].o += 1
            pit[0].strike += 1
            pit[0].go += 1
            atbat.go += 1
            print('滾地球出局！')
            break
        else:
            print('輸入錯誤！')
            continue
    bat.append(atbat)
    return result, base

def halfinning(pit, pited, bat): #一個半局
    runner , runs = [] , []
    out = 0
    point = 0
    while out < 3:
        result, base = onepa(pit, pited, bat)
        if result == 'ao' or result == 'go' or result == 's':
            out += 1
            if len(runner) > 0:
                if result == 'ao' and runner[-1] == 3 and out < 3:
                    sf = str(input("是否為高飛犧牲打？(Y:確認,或任意鍵繼續):"))
                    if sf == 'y' or sf == 'Y':
                        runner.pop(-1)
                        point += 1
                        pit[0].er += 1
                        bat[-1].rbi += 1
                        runs[-1].runs += 1
                        print('{}回來得分,目前單局得{}分'.format(runs[-1].name, point))
                        runs.pop(-1)
                elif result == 'go' and out < 3:
                    dp = str(input("是否發動雙殺守備？(Y:確認,或任意鍵繼續):"))
                    if dp == 'y' or dp == 'Y':
                        runner.pop(-1)
                        runs.pop(-1)
                        pit[0].o += 1
                        out += 1
                        print('雙殺守備!')
            if runner == []:
                print('{}人出局\n'.format(out))  
            else:
                print('{}人出局, {}壘有人\n'.format(out, listtostr(runner)))
        elif result == 'b':
            runner.sort()
            for i in range(len(runner)):
                if runner[i] == i + 1:
                    runner[i] += 1
                if runner[i] > 3:
                    runner.pop(i)
                    point += 1
                    pit[0].er += 1
                    bat[-1].rbi += 1
                    runs[-1].runs += 1
                    print('{}回來得分,目前單局得{}分'.format(runs[-1].name, point))
                    runs.pop(-1)
            runner.insert(0, 1)
            runs.insert(0, bat[-1])
            print('{}人出局, {}壘有人\n'.format(out, listtostr(runner)))
        else:
            runs.insert(0, bat[-1])
            if runner == []:
                runner.append(base)
            else:
                for i in range(len(runner)):
                    runner[i] += base  
                runner.append(base)
                runner.sort()
            for i in range(len(runner)):
                if runner[i] > 3:
                    point += len(runner[i:])
                    pit[0].er += len(runner[i:])
                    bat[-1].rbi += len(runner[i:])
                    for j in runs[i:]:
                        j.runs += 1
                        print(j.name, end = ' ')
                    print('回來得分,目前單局得{}分'.format(point))
                    del runner[i:]
                    del runs[i:]
                    break
            if runner == []:
                print('{}人出局\n'.format(out))
            else:
                print('{}人出局, {}壘有人\n'.format(out, listtostr(runner)))
    print('攻守交換！')
    return point

def lasthalf(pit, pited, bat, homepoint, awaypoint): #9局下半
    runner , runs = [] , []
    out = 0
    while out < 3:
        if homepoint > awaypoint:
            break
        result, base = onepa(pit, pited, bat)
        if result == 'ao' or result == 'go' or result == 's':
            out += 1
            if len(runner) > 0:
                if result == 'ao' and runner[-1] == 3 and out < 3:
                    sf = str(input("是否為高飛犧牲打？(Y:確認,或任意鍵繼續):"))
                    if sf == 'y' or sf == 'Y':
                        runner.pop(-1)
                        homepoint += 1
                        pit[0].er += 1
                        bat[-1].rbi += 1
                        runs[-1].runs += 1
                        if homepoint > awaypoint:
                            print("再見高飛犧牲打！")
                            break
                        print('{}回來得分,目前比數主隊{}:客隊{}！'.format(runs[-1].name, homepoint, awaypoint))  
                        runs.pop(-1)
                elif result == 'go' and out < 3:
                    dp = str(input("是否發動雙殺守備？(Y:確認,或任意鍵繼續):"))
                    if dp == 'y' or dp == 'Y':
                        runner.pop(-1)
                        runs.pop(-1)
                        pit[0].o += 1
                        out += 1
                        print('雙殺守備!')
            if runner == []:
                print('{}人出局\n'.format(out))  
            else:
                print('{}人出局, {}壘有人\n'.format(out, listtostr(runner)))
        elif result == 'b':
            runner.sort()
            for i in range(len(runner)):
                if runner[i] == i + 1:
                    runner[i] += 1
                if runner[i] > 3:
                    runner.pop(i)
                    homepoint += 1
                    pit[0].er += 1
                    bat[-1].rbi += 1
                    runs[-1].runs += 1
                    runs.pop(-1)
                    if homepoint > awaypoint:
                        print("再見保送！")
                        break
                    print("{}回來得分,目前比數主隊{}:客隊{}！".format(runs[-1].name, homepoint, awaypoint))
            if homepoint > awaypoint:
                break
            runner.insert(0, 1)
            runs.insert(0, bat[-1])
            print('{}人出局, {}壘有人\n'.format(out, listtostr(runner)))
        else:    
            runs.insert(0, bat[-1])
            if len(runner) == 0:
                runner.append(base)
            else:
                for i in range(len(runner)):
                    runner[i] += base  
                runner.append(base)
                runner.sort()
            for i in range(len(runner)):
                if runner[i] > 3:
                    homepoint += len(runner[i:])
                    pit[0].er += len(runner[i:])
                    bat[-1].rbi += len(runner[i:])
                    for j in runs[i:]:
                        j.runs += 1
                        print(j.name, end = ' ')
                    print("回來得分,目前比數主隊{}:客隊{}！".format(homepoint, awaypoint))
                    if homepoint > awaypoint:
                        if base == 4:
                            print("再見全壘打！")
                        else:
                            print("再見安打！")
                        break
                    del runner[i:]
                    del runs[i:]
                    break
            if homepoint > awaypoint:
                break
            if runner == []:
                print('{}人出局\n'.format(out))
            else:
                print('{}人出局, {}壘有人\n'.format(out, listtostr(runner)))
    return homepoint


def main(): #比賽運行
    while True:
        inning = numberkeyin('請輸入比賽局數：')
        if inning <= 0:
            print('請輸入正整數！')
        else:
            break
    homepoint, awaypoint = 0, 0
    print()
    #主隊名單
    homepit, homepited, homebat = [], [], []
    homepit.append(Pitcher(input('請輸入主隊先發投手姓名：')))
    while True:
        homebatnum = numberkeyin('請輸入主隊打者人數：')
        if homebatnum <= 0:
            print('請輸入正整數！')
        else:
            break
    for i in range(homebatnum):
        homebat.append(Batter(input('請輸入主隊打者姓名({}棒)：'.format(i+1)), i+1))
    print('主隊先發投手:' , homepit[0].name)
    print('主隊打者名單:')
    for i in range(len(homebat)):
        print(i+1 , "棒：" , homebat[i].name)
    print()
    #客隊名單
    awaypit, awaypited, awaybat = [], [], []
    awaypit.append(Pitcher(input('請輸入客隊先發投手姓名：')))
    while True:
        awaybatnum = numberkeyin('請輸入客隊打者人數：')
        if awaybatnum <= 0:
            print('請輸入正整數！')
        else:
            break
    for i in range(awaybatnum):
        awaybat.append(Batter(input('請輸入客隊打者姓名({}棒)：'.format(i+1)), i+1))
    print('客隊先發投手:' , awaypit[0].name)
    print('客隊打者名單:')  
    for i in range(len(awaybat)):
        print(i+1 , "棒：" , awaybat[i].name)
    #比賽開始
    for i in range(inning * 2):
        inn = (i + 2) // 2
        if (i + 1) == (inning * 2):
            if homepoint > awaypoint:
                print("主隊領先進入下半局")
                break
            else:
                pit, pited = awaypit, awaypited
                bat = homebat
                print("\n比賽來到{}局下半, 比數主隊{}:客隊{}！".format(inn, homepoint, awaypoint))
                homepoint = lasthalf(pit, pited, bat, homepoint, awaypoint)
                break
        if (i + 1) % 2 == 1: #上半局
            pit, pited = homepit, homepited
            bat = awaybat
            print("\n比賽來到{}局上半, 比數主隊{}:客隊{}！".format(inn, homepoint, awaypoint))
            awaypoint += halfinning(pit, pited, bat)
        else: #下半局
           pit, pited = awaypit, awaypited
           bat = homebat
           print("\n比賽來到{}局下半, 比數主隊{}:客隊{}！".format(inn, homepoint, awaypoint))
           homepoint += halfinning(pit, pited, bat)
    while True:
        if homepoint == awaypoint:
            print("比賽進入延長!")
            inning += 1
            print("\n比賽來到{}局上半, 比數主隊{}:客隊{}！".format(inning, homepoint, awaypoint))
            pit, pited = homepit, homepited
            bat = awaybat
            awaypoint += halfinning(pit, pited, bat)
            print("\n比賽來到{}局下半, 比數主隊{}:客隊{}！".format(inning, homepoint, awaypoint))
            pit, pited = awaypit, awaypited
            bat = homebat
            homepoint = lasthalf(pit, pited, bat, homepoint, awaypoint)
        else:
            break
    homepited += homepit ; awaypited += awaypit 
    homebat.sort(key = lambda s:s.batnum); awaybat.sort(key = lambda s:s.batnum)
    print("\n比賽結束！\n最終比數主隊{}:客隊{}！".format(homepoint, awaypoint))
    while True:
        result = str(input('請輸入想查詢的隊伍數據(HP:主隊投手,AP:客隊投手,HB:主隊打者,AB:客隊打者,或任意鍵結束比賽):'))
        r = result.lower()
        if r == 'hp':
            for i in range(len(homepited)):
                print("{}：IP:{}, H:{}, ER:{}, BB:{}, SO:{}, 球數:{}({}好,{}壞)"
                      .format(homepited[i].name, homepited[i].ip(), homepited[i].h,
                              homepited[i].er, homepited[i].bb, homepited[i].k,
                              homepited[i].pitch(), homepited[i].strike, homepited[i].ball))
            print()
        elif r == 'ap':
            for i in range(len(awaypited)):
                print("{}：IP:{}, H:{}, ER:{}, BB:{}, SO:{}, 球數:{}({}好,{}壞)"
                      .format(awaypited[i].name, awaypited[i].ip(), awaypited[i].h,
                              awaypited[i].er, awaypited[i].bb, awaypited[i].k,
                              awaypited[i].pitch(), awaypited[i].strike, awaypited[i].ball))
            print()
        elif r == 'hb':
            for i in range(len(homebat)):
                if homebat[i].homerun > 0:
                     print(i+1, "棒 {}：AB:{}, R:{}, H:{}, Hr:{}, RBI:{}, BB:{}, SO:{}"
                      .format(homebat[i].name, homebat[i].ab(), homebat[i].runs,
                              homebat[i].h(), homebat[i].homerun, homebat[i].rbi,
                              homebat[i].bb, homebat[i].so)) 
                else:
                    print(i+1, "棒 {}：AB:{}, R:{}, H:{}, RBI:{}, BB:{}, SO:{}"
                          .format(homebat[i].name, homebat[i].ab(), homebat[i].runs,
                                  homebat[i].h(), homebat[i].rbi, homebat[i].bb, 
                                  homebat[i].so))    
            print()
        elif r == 'ab':
            for i in range(len(awaybat)):
                if awaybat[i].homerun > 0:
                    print(i+1, "棒 {}：AB:{}, R:{}, H:{}, Hr:{}, RBI:{}, BB:{}, SO:{}"
                      .format(awaybat[i].name, awaybat[i].ab(), awaybat[i].runs, 
                              awaybat[i].h(),  awaybat[i].homerun, awaybat[i].rbi, 
                              awaybat[i].bb, awaybat[i].so))
                else:
                    print(i+1, "棒 {}：AB:{}, R:{}, H:{}, RBI:{}, BB:{}, SO:{}"
                      .format(awaybat[i].name, awaybat[i].ab(), awaybat[i].runs, 
                              awaybat[i].h(), awaybat[i].rbi, awaybat[i].bb, 
                              awaybat[i].so))
            print()
        else:
           check = str(input('確認要結束遊戲嗎？(Y:確認,或任意鍵返回):'))
           c2 = check.lower()
           if c2 == 'y':
               break
           else:
               continue
                       
if __name__ == '__main__': 
    main()