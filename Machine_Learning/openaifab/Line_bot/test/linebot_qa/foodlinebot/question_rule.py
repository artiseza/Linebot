# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 16:51:38 2021

@author: Alan Lin
"""
from .questionnaire import *
from django.conf import settings
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)

def q_bot(reply_token,Q):
    question=[]
    message=[]
    for i in range(len(Q)): #開始跑 第qtag題內 問題、選項
        question.append(Q[i]) #Q[0]:問題 ,Q[1]:選項1 ,Q[2]:選項2...                                                          
    print('\nquestion',question,'\nlen(question):',len(question))
    if len(question)==1:
        message.append(TextSendMessage(text=question[0]))
        line_bot_api.reply_message(reply_token,message)
    elif len(question)==2:
        message.append(topic_1(reply_token,question[0],question[1]))
    elif len(question)==3:
        message.append(topic_2(reply_token,question[0],question[1],question[2]))
    elif len(question)==4:
        message.append(topic_3(reply_token,question[0],question[1],question[2],question[3]))
    elif len(question)==5:
        message.append(topic_4(reply_token,question[0],question[1],question[2],question[3],question[4]))
    elif len(question)==6:
        message.append(topic_5(reply_token,question[0],question[1],question[2],question[3],question[4],question[5]))
    elif len(question)==7:
        message.append(topic_6(reply_token,question[0],question[1],question[2],question[3],question[4],question[5],question[6]))
    elif len(question)==8:
        message.append(topic_7(reply_token,question[0],question[1],question[2],question[3],question[4],question[5],question[6],question[7]))
    elif len(question)==8:
        message.append(topic_8(reply_token,question[0],question[1],question[2],question[3],question[4],question[5],question[6],question[7],question[8]))
    elif len(question)==10:
        message.append(topic_9(reply_token,question[0],question[1],question[2],question[3],question[4],question[5],question[6],question[7],question[8],question[9]))
    elif len(question)==11:
        message.append(topic_10(reply_token,question[0],question[1],question[2],question[3],question[4],question[5],question[6],question[7],question[8],question[9],question[10]))
    elif len(question)==12:
        message.append(topic_11(reply_token,question[0],question[1],question[2],question[3],question[4],question[5],question[6],question[7],question[8],question[9],question[10],question[11]))
    elif len(question)==13:
        message.append(topic_12(reply_token,question[0],question[1],question[2],question[3],question[4],question[5],question[6],question[7],question[8],question[9],question[10],question[11],question[12]))
    elif len(question)==14:
        message.append(topic_13(reply_token,question[0],question[1],question[2],question[3],question[4],question[5],question[6],question[7],question[8],question[9],question[10],question[11],question[12],question[13]))
    elif len(question)==15:
        message.append(topic_14(reply_token,question[0],question[1],question[2],question[3],question[4],question[5],question[6],question[7],question[8],question[9],question[10],question[11],question[12],question[13],question[14]))
    elif len(question)==16:
        message.append(topic_15(reply_token,question[0],question[1],question[2],question[3],question[4],question[5],question[6],question[7],question[8],question[9],question[10],question[11],question[12],question[13],question[14],question[15]))
    elif len(question)==17:
        message.append(topic_16(reply_token,question[0],question[1],question[2],question[3],question[4],question[5],question[6],question[7],question[8],question[9],question[10],question[11],question[12],question[13],question[14],question[15],question[16]))
    elif len(question)==18:
        message.append(topic_17(reply_token,question[0],question[1],question[2],question[3],question[4],question[5],question[6],question[7],question[8],question[9],question[10],question[11],question[12],question[13],question[14],question[15],question[16],question[17]))
    elif len(question)==19:
        message.append(topic_18(reply_token,question[0],question[1],question[2],question[3],question[4],question[5],question[6],question[7],question[8],question[9],question[10],question[11],question[12],question[13],question[14],question[15],question[16],question[17],question[18]))
    elif len(question)==20:
        message.append(topic_19(reply_token,question[0],question[1],question[2],question[3],question[4],question[5],question[6],question[7],question[8],question[9],question[10],question[11],question[12],question[13],question[14],question[15],question[16],question[17],question[18],question[19]))
    elif len(question)==21:
        message.append(topic_20(reply_token,question[0],question[1],question[2],question[3],question[4],question[5],question[6],question[7],question[8],question[9],question[10],question[11],question[12],question[13],question[14],question[15],question[16],question[17],question[18],question[19],question[20]))