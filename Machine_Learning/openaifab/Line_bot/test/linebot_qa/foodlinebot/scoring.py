# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 13:59:09 2021

@author: Alan Lin
"""
from datetime import timedelta
from datetime import datetime 

def scoring(ans,hos,qnaire,Q_name): 
    # 沒答的題目先補零
    scan = Q_name
    for i in scan:
        if not(i in ans[hos][qnaire]):
            ans[hos][qnaire][i] = '0' 
    # Default 按鈕值
    if ans[hos][qnaire]['1'] =='0':
        ans[hos][qnaire]['1'] = '2200'
    if ans[hos][qnaire]['2'] =='0':
        ans[hos][qnaire]['2'] = '15'
    if ans[hos][qnaire]['3'] =='0':
        ans[hos][qnaire]['3'] = '0730'
    if ans[hos][qnaire]['4'] =='0':
        ans[hos][qnaire]['4'] = '6.5'    
    if ans[hos][qnaire]['DSM_5_1'] =='0':
        ans[hos][qnaire]['DSM_5_1'] = '12'
    if ans[hos][qnaire]['birthday'] =='0':
        ans[hos][qnaire]['birthday'] = '1960/1/1'
    if ans[hos][qnaire]['height'] =='0':
        ans[hos][qnaire]['height'] = '170'
    if ans[hos][qnaire]['weight'] =='0':
        ans[hos][qnaire]['weight'] = '50'
    if ans[hos][qnaire]['neck circumference'] =='0':
        ans[hos][qnaire]['neck circumference'] = '14'
    
    score_list={}    
    # ISI_T
    if ans[hos][qnaire]['5']=='0' : #5選很滿意
        score_list['ISI_T'] = '0'
    elif ans[hos][qnaire]['6A']=='3': #6A選沒有以上困擾
        score_list['ISI_T'] = str(int(ans[hos][qnaire]['5'])+int(ans[hos][qnaire]['7'])+int(ans[hos][qnaire]['8'])+int(ans[hos][qnaire]['9']))
    else:
        score_list['ISI_T'] = str(int(ans[hos][qnaire]['6-1-b'])+int(ans[hos][qnaire]['6-2.1-b'])+int(ans[hos][qnaire]['6-2.2-b'])+int(ans[hos][qnaire]['5'])+int(ans[hos][qnaire]['7'])+int(ans[hos][qnaire]['8'])+int(ans[hos][qnaire]['9']))
    
    # Sleep diary(時間計算未完成)
    TBT = time_sub(int(ans[hos][qnaire]['3'][0:2])+24,ans[hos][qnaire]['3'][2:],ans[hos][qnaire]['1'][0:2],ans[hos][qnaire]['1'][2:])
    score_list['TBT'] = TBT # 總躺床時間=起床時間-上床時間(hr) #3-1
    score_list['WASO'] = '0' #半夜醒來&早醒加總共多久時間，此問卷沒有問
    score_list['SOL'] = ans[hos][qnaire]['2'] # 花多久時間入睡(分鐘)
    
    st1 = time_add(ans[hos][qnaire]['1'][0:2],ans[hos][qnaire]['1'][2:],'00',ans[hos][qnaire]['2'])
    if len(st1) ==2:
        st = st1[0].split(':')
    else:
        st = st1.split(':')
    T = ans[hos][qnaire]['4'].split('.') #看4有沒有小數點
    if len(T) ==2:
        st1 = time_add(st[0],st[1],T[0],int(T[1])/10*60)
        st = st1.split(':')
    else:
        st1 = time_add(st[0],st[1],T[0],"0")
        st = st1.split(':')        
    # print('相加後醒來時間',st1) #1+2+4
    
    Stayin = time_sub(ans[hos][qnaire]['3'][0:2],ans[hos][qnaire]['3'][2:],st[0],st[1]) #3-(1+2+4)
    score_list['Stayin'] = str(Stayin) # 賴床時間(hr)(若選擇非早醒，即醒來時間-下床時間) 
    score_list['TST'] = str(float(score_list['TBT'])-int(score_list['WASO'])-float(score_list['SOL'])/60-float(score_list['Stayin'])) # 睡眠總時間
    score_list['SE'] = str(float(score_list['TST'])/float(score_list['TBT'])*100) # 睡眠效率

    # DURAT
    if float(ans[hos][qnaire]['4']) > 7:
        score_list['DURAT'] = '0'
    elif float(ans[hos][qnaire]['4']) > 6 and float(ans[hos][qnaire]['4']) < 7 :
        score_list['DURAT'] = '1'
    elif float(ans[hos][qnaire]['4']) > 5 and float(ans[hos][qnaire]['4']) < 6 :
        score_list['DURAT'] = '2'
    elif float(ans[hos][qnaire]['4']) < 5:
        score_list['DURAT'] = '3'
       
    # DISTB
    if ans[hos][qnaire]['6A'] =='3': #6A選沒有以上困擾
        if ans[hos][qnaire]['6B'] =='8': #6B選沒有以上困擾
            score_list['DISTB'] = '0'
        else:
            if int(ans[hos][qnaire]['6-5.1']) >= int(ans[hos][qnaire]['6-5.2']):
                item_5 = ans[hos][qnaire]['6-5.1']
            else:
                item_5 = ans[hos][qnaire]['6-5.2']
            score_list['DISTB'] = str(int(ans[hos][qnaire]['6-3'])+int(ans[hos][qnaire]['6-4'])+int(item_5)+int(ans[hos][qnaire]['6-6'])+int(ans[hos][qnaire]['6-7'])+int(ans[hos][qnaire]['6-8'])+int(ans[hos][qnaire]['6-9']))
    else:
        if ans[hos][qnaire]['6B'] =='8': #6B選沒有以上困擾
            score_list['DISTB'] = ans[hos][qnaire]['6-2.1-a']
        else:
            if int(ans[hos][qnaire]['6-5.1']) >= int(ans[hos][qnaire]['6-5.2']):
                item_5 = ans[hos][qnaire]['6-5.1']
            else:
                item_5 = ans[hos][qnaire]['6-5.2']
            score_list['DISTB'] = str(int(ans[hos][qnaire]['6-2.1-a']) + int(ans[hos][qnaire]['6-3'])+int(ans[hos][qnaire]['6-4'])+int(item_5)+int(ans[hos][qnaire]['6-6'])+int(ans[hos][qnaire]['6-7'])+int(ans[hos][qnaire]['6-8'])+int(ans[hos][qnaire]['6-9']))
    if int(score_list['DISTB']) == 0:
        score_list['DISTB'] = '0'
    elif int(score_list['DISTB']) >= 1 and int(score_list['DISTB']) < 9:
        score_list['DISTB'] = '1'
    elif int(score_list['DISTB']) >= 9 and int(score_list['DISTB']) < 18:
        score_list['DISTB'] = '2'
    elif int(score_list['DISTB']) >= 18 :
        score_list['DISTB'] = '3'  
        
    # LATEN    
    if int(ans[hos][qnaire]['2']) > 0 and int(ans[hos][qnaire]['2']) <= 15 :
        score_list['LATEN'] ='0'
    elif int(ans[hos][qnaire]['2']) > 15 and int(ans[hos][qnaire]['2']) <= 30 :
        score_list['LATEN'] ='1'
    elif int(ans[hos][qnaire]['2']) > 30 and int(ans[hos][qnaire]['2']) <= 60 :
        score_list['LATEN'] ='2'
    elif int(ans[hos][qnaire]['2']) > 60 :
        score_list['LATEN'] ='3'
    if ans[hos][qnaire]['6A']=='3': #選沒有以上困擾
        score_list['LATEN'] = score_list['LATEN']   
    else:
        score_list['LATEN'] = str(int(ans[hos][qnaire]['6-1-a']) + int(score_list['LATEN']))   
    if score_list['LATEN']=='0':
        score_list['LATEN'] = '0'
    elif int(score_list['LATEN']) >= 1 and int(score_list['LATEN']) <=2:
        score_list['LATEN'] = '1'
    elif int(score_list['LATEN']) >= 3 and int(score_list['LATEN']) <=4:
        score_list['LATEN'] = '2'
    elif int(score_list['LATEN']) >= 5 and int(score_list['LATEN']) <=6:
        score_list['LATEN'] = '3'

    # DAYDYS
    if int(ans[hos][qnaire]['10']) == 0 :
        score_list['DAYDYS'] ='0'
    elif int(ans[hos][qnaire]['10']) >= 1 and int(ans[hos][qnaire]['10']) <= 2 :
        score_list['DAYDYS'] ='1'
    elif int(ans[hos][qnaire]['10']) == 3 :
        score_list['DAYDYS'] ='2'
    elif int(ans[hos][qnaire]['10']) == 4 :
        score_list['DAYDYS'] ='3'        
    score_list['DAYDYS'] = str(int(score_list['DAYDYS']) + int(ans[hos][qnaire]['13']))   
    if int(score_list['DAYDYS']) == 0:
        score_list['DAYDYS'] = '0'
    elif int(score_list['DAYDYS']) >= 1 and int(score_list['DAYDYS']) <=2:
        score_list['DAYDYS'] = '1'
    elif int(score_list['DAYDYS']) >= 3 and int(score_list['DAYDYS']) <=4:
        score_list['DAYDYS'] = '2'
    elif int(score_list['DAYDYS']) >= 5 and int(score_list['DAYDYS']) <=6:
        score_list['DAYDYS'] = '3'
        
    # HSE
    count = time_sub(ans[hos][qnaire]['3'][0:2],ans[hos][qnaire]['3'][2:],ans[hos][qnaire]['1'][0:2],ans[hos][qnaire]['1'][2:])
    score_list['HSE'] = str(float(ans[hos][qnaire]['4'])/float(count)*100) 
    if float(score_list['HSE']) > 85 :
        score_list['HSE'] ='0'
    elif float(score_list['HSE']) > 75 and float(score_list['HSE']) <= 85 :
        score_list['HSE'] ='1'
    elif float(score_list['HSE']) > 65 and float(score_list['HSE']) <= 75 :
        score_list['HSE'] ='2'
    elif float(score_list['HSE']) <= 65 :
        score_list['HSE'] ='3'        
        
    # SLPQUAL
    if int(ans[hos][qnaire]['5']) == 0:
        score_list['SLPQUAL'] = '0'
    elif int(ans[hos][qnaire]['5']) >= 1 and int(ans[hos][qnaire]['5']) <=2:
        score_list['SLPQUAL'] = '1'
    elif int(ans[hos][qnaire]['5']) == 3 :
        score_list['SLPQUAL'] = '2'
    elif int(ans[hos][qnaire]['5']) == 4 :
        score_list['SLPQUAL'] = '3'
       
    # MEDS
    if int(ans[hos][qnaire]['11_1']) < int(ans[hos][qnaire]['11_2']) :
        score_list['MEDS'] = ans[hos][qnaire]['11_2']
    else:
        score_list['MEDS'] = ans[hos][qnaire]['11_1']
 
    # PSQI_T
    score_list['PSQI_T'] = str(int(score_list['DURAT']) + int(score_list['DISTB']) + int(score_list['LATEN']) + int(score_list['DAYDYS']) + int(score_list['HSE']) + int(score_list['SLPQUAL']) + int(score_list['MEDS']))

    # ESS_T
    score_list['ESS_T'] = str(int(ans[hos][qnaire]['13_1']) + int(ans[hos][qnaire]['13_2']) + int(ans[hos][qnaire]['13_3']) + int(ans[hos][qnaire]['13_4']) + int(ans[hos][qnaire]['13_5']) + int(ans[hos][qnaire]['13_6']) + int(ans[hos][qnaire]['13_7']) + int(ans[hos][qnaire]['13_8']))   
    
    # Bang_Stop_T
    # 性別(男:Code=1; 女:Code=0)
    if ans[hos][qnaire]['gender'] == '0':
        gend = 0 #女
        if int(ans[hos][qnaire]['neck circumference'])<16:
            neck = 0
        else:
            neck = 1
    else:
        gend = 1 #男
        if int(ans[hos][qnaire]['neck circumference'])<17:
            neck = 0
        else:
            neck = 1    
    # 頸圍(男>=17吋; 女>16吋:Code=1; 男<17吋; 女<16吋: Code=0)    
    # 年紀 (>=50:Code=1; <50:Code=0)
    Y = age(ans[hos][qnaire]['birthday'])
    if Y < 50:
        year = 0
    else:
        year = 1    
    # BMI(體重_kg/身高平方_m2，BMI>=35:Code=1; BMI<35:Code=0)
    BMI = int(ans[hos][qnaire]['weight'])/(int(ans[hos][qnaire]['height'])/100)**2
    if BMI < 35 :
        bmi = 0
    else:
        bmi = 1        
    # 高血壓(有1-3:Code=1; 沒有0: Code=0)
    if ans[hos][qnaire]['q1'] =='0':
        q1 = 0
    else:
        q1 = 1        
    # item 6-5.1 (>=3:Code=1; <3:Code=0)
    if ans[hos][qnaire]['6-5.1'] =='3':
        item_651 = 1
    else:
        item_651 = 0
    # item 13-1~13-8(加總分數>=12:Code=1; <12:Code=0)
    if int(ans[hos][qnaire]['13_1']) + int(ans[hos][qnaire]['13_2']) + int(ans[hos][qnaire]['13_3']) + int(ans[hos][qnaire]['13_4']) + int(ans[hos][qnaire]['13_5']) + int(ans[hos][qnaire]['13_6']) + int(ans[hos][qnaire]['13_7']) + int(ans[hos][qnaire]['13_8']) < 12:
        item_13 = 0
    else:
        item_13 = 1
    # item 12(是:Code=1; 否:Code=0)
    if ans[hos][qnaire]['12'] =='0':
        item_12 = 0
    else:
        item_12 = 1
    score_list['Bang_Stop_T'] = str(gend + bmi + neck + year + q1 + item_651 + item_12 + item_13)
    
    # GAD
    score_list['GAD']= str(int(ans[hos][qnaire]['14']) + int(ans[hos][qnaire]['15']) + int(ans[hos][qnaire]['16']) + int(ans[hos][qnaire]['17']) + int(ans[hos][qnaire]['18']) + int(ans[hos][qnaire]['19']) + int(ans[hos][qnaire]['20']))    
    
    # PHQ
    score_list['PHQ']= str(int(ans[hos][qnaire]['21']) + int(ans[hos][qnaire]['22']) + int(ans[hos][qnaire]['23']) + int(ans[hos][qnaire]['24']) + int(ans[hos][qnaire]['25']) + int(ans[hos][qnaire]['26']) + int(ans[hos][qnaire]['27']) + int(ans[hos][qnaire]['28']) + int(ans[hos][qnaire]['29']))    
    # score_list=[ISI_T,TBT,WASO,SOL,Stayin,TST,SE,PSQI_T,ESS_T,Bang_Stop_T,GAD,PHQ]
    print(score_list)
    return score_list

def time_sub(hour2,minute2,hour1,minute1):
    #小時:分 - 小時:分 >> T = 計算時差(hr)
    t2 = timedelta(hours=int(hour2), minutes=int(minute2))
    t1 = timedelta(hours=int(hour1), minutes=int(minute1))    
    A = str(t2-t1).split(',')
    if len(A) ==2:   
        if '-1 day' in A:
            x = A[1].split(':')
            d2 = timedelta(hours=24, minutes=0)    
            d1 = timedelta(hours=int(x[0]), minutes=int(x[1]))    
            A2 = str(d2-d1).split(':')
            T = int(A2[0])+int(A2[1])/60
        else:
            x = A[1].split(':')
            T = int(x[0])+int(x[1])/60
    else:
        x=A[0].split(':')
        T = int(x[0])+int(x[1])/60
    return str(T)
def time_add(hour2,minute2,hour1,minute1):
    #小時:分 + 分 >> T = 時間點(hh:mm) (str)
    t2 = timedelta(hours=int(hour2), minutes=int(minute2))
    t1 = timedelta(hours=int(hour1), minutes=int(minute1))    
    A = str(t2+t1).split(',')
    if len(A) ==2:
        T = str(A[1])
    else:
        T = str(A[0])
    return T
def age(my_date):
    b_date = datetime.strptime(my_date, '%Y/%m/%d')  
    years_old = (datetime.today() - b_date).days/365
    return years_old