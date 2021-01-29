# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 14:03:17 2021

@author: Alan Lin
"""
from scoring import scoring

with open("C:/Users/User/Machine_Learning/openaifab/Line_bot/test/foodlinebot/question_list.txt", "r",encoding="utf-8") as f:    #開啟檔案
    Q = f.read()   #讀取檔案
Qdict = eval(Q[6:]) #str轉dict
Q_name = list(Qdict.keys())    #列出全部問題之name
ans={"Wanfang": {"PerMonth": {"q1": "0", "q2": "0", "q3": "0", "q4": "Test", "q5": "0", "q6": "0", "a": "1", "b": "1", "c": "1", "d": "1", "e": "1", "f": "1", "q7": "0", "q8": "0", "1": "2400", "2": "30", "3": "0900", "4": "8", "5": "3", "6A": "0", "6-1-a": "3", "6-1-b": "1", "6-2.1-a": "2", "6-2.1-b": "0", "6-2.2-a": "0", "6B": "0", "6-3": "2", "6-3-A": "0", "6-3-B": "0", "6-3-C": "1", "6-4": "0", "6-5.1": "1", "6-5.2": "3", "6-5.2-A": "1", "6-5.2-B": "1", "6-5.2-C": "1", "6-5.2-D": "0", "6-6": "0", "6-7": "0", "6-8": "0", "6-9": "0", "7": "1", "8": "1", "9": "2", "10": "1", "11_1": "1", "11_2": "0", "DSM_5_1": "3", "DSM_5_2": "1", "12": "0", "13": "0", "13_1": "1", "13_2": "1", "13_3": "1", "13_4": "2", "13_5": "2", "13_6": "2", "13_7": "1", "13_8": "1", "14": "0", "15": "0", "16": "3", "17": "3", "18": "3", "19": "3", "20": "3", "21": "3", "22": "3", "23": "3", "24": "3", "25": "3", "26": "3", "27": "3", "28": "3", "29": "3", "gender": "1", "birthday": "1996/1/1", "height": "170", "weight": "50", "neck circumference": "14", "education": "5", "Profession": "4", "marital": "0"}}}

score_list={}

hos="Wanfang"
qnaire="PerMonth"

score=''
ans[hos][qnaire]['score'] = scoring(ans,hos,qnaire,Q_name) # 回傳分數
for key, value in ans[hos][qnaire]['score'].items():
    temp = key+': '+value+'\n'
    score += temp
# for i in range(len(score)):
print('score: \n',score)
# message.append(TextSendMessage(text=score)) #顯示各參數值