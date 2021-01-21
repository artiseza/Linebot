from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
 
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import *
import cv2
import random
import  string
from .image_processing import edge
from .Video_Processing import *
from .models import *
from .message_func import *
from .questionnaire import *
# from .question_list import *
from .question_rule import *
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
# 取得settings.py中的LINE Bot憑證來進行Messaging API的驗證。
domain = '6a3d9102dd10.ngrok.io'
import json

# uid_list = User_Info.objects.all()
# print(uid_list[1])
# # #push message to one user
# message = []
# message.append(questionnaire())
# line_bot_api.push_message('U7467d7c1fe13635ad38d2c97ac72d6e2',message)
#push message to multiple users

# line_bot_api.multicast(['user_id1', 'user_id2'],TextSendMessage(text='Hello World!'))

@csrf_exempt
def callback(request):   
    
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        try:
            events = parser.parse(body, signature)  # 傳入的事件
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()      
        for event in events:   
            if isinstance(event, MessageEvent):  # 如果有訊息事件(文字、圖片、位置、影片、貼圖、聲音、檔案)
                print('message',event.message)
                message = []
                if event.message.type=='text':
                    mtext=event.message.text
                    uid=event.source.user_id
                    profile=line_bot_api.get_profile(uid)
                    name=profile.display_name
                    pic_url=profile.picture_url
                    
                    if User_Info.objects.filter(uid=uid).exists()==False:
                        User_Info.objects.create(uid=uid,name=name,pic_url=pic_url,mtext='',state='',qtag=0) #一開始設空格
                        message.append(TextSendMessage(text='初次新增會員成功'))
                    elif User_Info.objects.filter(uid=uid).exists()==True:  
                        user_info = User_Info.objects.filter(uid=uid)
                        # print('user_info',user_info)
                        for user in user_info:
                            state = user.state #讀取先前: 問卷填寫狀態
                            hos = user.hos #讀取先前:醫院別
                            qnaire = user.qnaire #讀取先前:問卷別
                            qname = user.qname #讀取先前: 題目名稱
                            qtag = user.qtag #讀取先前:題目指標
                            ans = user.ans #讀取先前: 答案 (若要清空,建一空白陣列存server即可)
                        with open("C:/Users/User/Machine_Learning/openaifab/Line_bot/test/foodlinebot/question_list.txt", "r",encoding="utf-8") as f:    #開啟檔案
                            Q = f.read()   #讀取檔案
                        Qdict = eval(Q[6:]) #str轉dict
                        Q_name = list(Qdict.keys())    #列出全部問題之name
                        # print('Q_name:\n',Q_name)
                        
                        if '動作選單' in mtext:
                            message.append(quickreplybutton())   
                        elif '填寫問卷' in mtext:
                            message.append(questionhos())
                            User_Info.objects.filter(uid=uid).update(qtag=0) #從第0題開始做
                            User_Info.objects.filter(uid=uid).update(state='write')
                            # data2 = json.dumps({'a': 'Runoob', 'b': 7}, sort_keys=True, indent=4, separators=(',', ': '))
                        elif 'ShuangHo' in mtext:
                            ans[mtext]={} #存醫院大字典
                            message.append(questionnaire()) 
                            User_Info.objects.filter(uid=uid).update(hos=mtext) #存醫院別
                            User_Info.objects.filter(uid=uid).update(ans=ans) #存醫院字典到server 
                        elif 'TMUH' in mtext:
                            ans[mtext]={} #存醫院大字典
                            message.append(questionnaire()) 
                            User_Info.objects.filter(uid=uid).update(hos=mtext) #存醫院別
                            User_Info.objects.filter(uid=uid).update(ans=ans) #存醫院字典到server 
                        elif 'Wanfang' in mtext:
                            ans[mtext]={} #存醫院大字典
                            message.append(questionnaire()) 
                            User_Info.objects.filter(uid=uid).update(hos=mtext) #存醫院別
                            User_Info.objects.filter(uid=uid).update(ans=ans) #存醫院字典到server 
                        elif 'First' in mtext:     
                            ans[hos]={mtext:{}} #存醫院大字典                            
                            #開始問卷第一題
                            q_bot(event.reply_token,Qdict[Q_name[qtag]]) #問(第一次問卷)第Qtag題   
                            qtag +=1
                            User_Info.objects.filter(uid=uid).update(qtag=qtag) #存二層題號到server
                            User_Info.objects.filter(uid=uid).update(qnaire=mtext) #存問卷別
                            User_Info.objects.filter(uid=uid).update(qname=Q_name[qtag-1]) #存題目名稱
                            User_Info.objects.filter(uid=uid).update(ans=ans) #存問卷字典到server 
                        elif 'TwoWeeks' in mtext:     
                            ans[hos]={mtext:{}} #存醫院大字典                            
                            #開始問卷第一題
                            q_bot(event.reply_token,Qdict[Q_name[qtag]]) #問(兩週問卷)第Qtag題   
                            qtag +=1
                            User_Info.objects.filter(uid=uid).update(qtag=qtag) #存二層題號到server
                            User_Info.objects.filter(uid=uid).update(qnaire=mtext) #存問卷別
                            User_Info.objects.filter(uid=uid).update(qname=Q_name[qtag-1]) #存題目名稱
                            User_Info.objects.filter(uid=uid).update(ans=ans) #存問卷字典到server 
                        elif 'PerMonth' in mtext:   
                            ans[hos]={mtext:{}} #存醫院大字典                            
                            #開始問卷第一題
                            q_bot(event.reply_token,Qdict[Q_name[qtag]]) #問(每月問卷)第Qtag題   
                            qtag +=1
                            User_Info.objects.filter(uid=uid).update(qtag=qtag) #存二層題號到server
                            User_Info.objects.filter(uid=uid).update(qnaire=mtext) #存問卷別
                            User_Info.objects.filter(uid=uid).update(qname=Q_name[qtag-1]) #存題目名稱
                            User_Info.objects.filter(uid=uid).update(ans=ans) #存問卷字典到server 
                            
                        elif state=='write':     
                            ans[hos][qnaire][qname]=mtext #回答與先前題號存字典
                            if qtag < len(Q_name):
                                qtag_new,qname_new=rule(qtag,Qdict,Q_name,ans,hos,qnaire,qname,mtext,event.reply_token)
                                # print('\nqtag_new: ',qtag_new,'\nqname_new: ',qname_new)
                            elif qtag >= len(Q_name): #問卷結束
                                qtag_new = 0
                                qname_new='' #題目名稱歸零     
                                User_Info.objects.filter(uid=uid).update(hos='') #醫院別歸零
                                User_Info.objects.filter(uid=uid).update(qnaire='') #問卷別歸零                        
                                User_Info.objects.filter(uid=uid).update(state='read')
                                message.append(TextSendMessage(text='填寫問卷完畢'))
                                #回答存入本地
                                with open("C:/Users/User/Machine_Learning/openaifab/Line_bot/test/foodlinebot/ans.txt","w") as f:
                                    f.write(str(ans)) #dict轉str
                                
                            User_Info.objects.filter(uid=uid).update(qname=qname_new) #存題目名稱
                            User_Info.objects.filter(uid=uid).update(qtag=qtag_new) #存序號到server
                            User_Info.objects.filter(uid=uid).update(ans=ans) #存 題號:'答案' 到字典
                        elif '選單1' in mtext:
                            message.append(imagemap_message())
                        elif '選單2' in mtext:
                            message.append(buttons_message())
                        elif '選單3' in mtext:
                            message.append(Confirm_Template())
                        elif '選單4' in mtext:
                            message.append(Carousel_Template())
                        elif '選單5' in mtext:
                            message.append(image_carousel_message1())                        
                        else:
                            # 取得資料庫內容
                            user_info = User_Info.objects.filter(uid=uid)
                            for user in user_info:
                                info = user.mtext+'\n'
                            message.append(TextSendMessage(text='先前訊息:'+info))                       
                            mtext = info + mtext
                            User_Info.objects.filter(uid=uid).update(mtext=mtext)
                            message.append(TextSendMessage(text='資料庫內容:'+mtext))                     
                            # message.append(TextSendMessage(text='已經有建立會員資料囉'))                        
                    # message.append(TextSendMessage(text=event.message.text)) #TextSendMessage(text="收到訊息了")
                    line_bot_api.reply_message(event.reply_token,message)

                elif event.message.type=='image':                   
                    image_name = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(4))
                    image_content = line_bot_api.get_message_content(event.message.id)
                    image_name = image_name.upper()
                    path ='D:/LineBot_pic/static/'+image_name+'.jpg'
                    with open(path, 'wb') as fd:
                        for chunk in image_content.iter_content():
                            fd.write(chunk)      
                    path_edge = edge(path,image_name)
                    url = 'https://'+domain+'/'+path_edge
                    message.append(TextSendMessage(text='圖片處理中'))
                    message.append(ImageSendMessage(original_content_url=url,preview_image_url=url))    
                    line_bot_api.reply_message(event.reply_token,message)
                    
                elif event.message.type=='location':
                    message.append(TextSendMessage(text='位置訊息'))
                    line_bot_api.reply_message(event.reply_token,message)
                    
                elif event.message.type=='video':
                    video_name = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(4))
                    video_content = line_bot_api.get_message_content(event.message.id)
                    video_name = video_name.upper()
                    path ='D:/LineBot_pic/static/'+video_name+'.mp4'
                    with open(path, 'wb') as fd:
                        for chunk in video_content.iter_content():
                            fd.write(chunk)
                    #獲得縮圖URL與影片URL
                    image_path,video_path = video_processing(path,video_name)
                    message.append(TextSendMessage(text='影片處理中'))
                    message.append(VideoSendMessage(original_content_url='https://'+domain+'/'+video_path[:],
                                                    preview_image_url='https://'+domain+'/'+image_path[:]))                    
                    line_bot_api.reply_message(event.reply_token,message)
                elif event.message.type=='sticker':
                    message.append(TextSendMessage(text='貼圖訊息'))
                    line_bot_api.reply_message(event.reply_token,message)

                elif event.message.type=='audio':
                    message.append(TextSendMessage(text='聲音訊息'))
                    line_bot_api.reply_message(event.reply_token,message)

                elif event.message.type=='file':
                    message.append(TextSendMessage(text='檔案訊息'))
                    line_bot_api.reply_message(event.reply_token,message)

        return HttpResponse()
    else:
        return HttpResponseBadRequest()
    
def rule(qtag,Qdict,Q_name,ans,hos,qnaire,qname,mtext,reply_token):
    # print('qtag',qtag,'ans:',ans,'mtext:',mtext) 
    if qtag==(Q_name.index('6A')+1) and ans[hos][qnaire]['6A']=='0' : #當問到6A的下一題時，檢查選哪個選項.進入不同問題     
        if not('6-1-a' in ans[hos][qnaire]):        
            q_bot(reply_token,Qdict['6-1-a'])
            qname = '6-1-a'
            # qtag = Q_name.index('6-1-a')     
        elif '6-1-a' in ans[hos][qnaire]:    
            q_bot(reply_token,Qdict['6-1-b'])
            qname = '6-1-b'     
            qtag = Q_name.index('6B')     
    elif qtag==(Q_name.index('6A')+1) and ans[hos][qnaire]['6A']=='1' :
        if not('6-2.1-a' in ans[hos][qnaire]):
            q_bot(reply_token,Qdict['6-2.1-a'])
            qname = '6-2.1-a' 
            # qtag = Q_name.index('6-2.1-a')
        elif '6-2.1-a' in ans[hos][qnaire]:
            q_bot(reply_token,Qdict['6-2.1-b'])
            qname = '6-2.1-b'
            qtag = Q_name.index('6B') 
    elif qtag==(Q_name.index('6A')+1) and ans[hos][qnaire]['6A']=='2' :
        if not('6-2.2-a' in ans[hos][qnaire]):
            q_bot(reply_token,Qdict['6-2.2-a'])
            qname = '6-2.2-a' 
            # qtag = Q_name.index('6-2.2-a')
        elif '6-2.2-a' in ans[hos][qnaire]:
            q_bot(reply_token,Qdict['6-2.2-b'])
            qname = '6-2.2-b'
            qtag = Q_name.index('6B') 
    elif qtag==(Q_name.index('6A')+1) and ans[hos][qnaire]['6A']=='3' :     
        q_bot(reply_token,Qdict['6B'])        
        qname = '6B'
        qtag = Q_name.index('6B')  #問完後指標跳到下一題的名稱
            
    elif qtag==(Q_name.index('6B')+1) and ans[hos][qnaire]['6B']=='0' : #當問到6B的下一題時，檢查選哪個選項.進入不同問題
        if not('6-3' in ans[hos][qnaire]):
            q_bot(reply_token,Qdict['6-3'])
            qname = '6-3' 
        elif not('6-3-A' in ans[hos][qnaire]):
            q_bot(reply_token,Qdict['6-3-A'])
            qname = '6-3-A'
        elif not('6-3-B' in ans[hos][qnaire]):    
            q_bot(reply_token,Qdict['6-3-B'])
            qname = '6-3-B'
        elif not('6-3-C' in ans[hos][qnaire]):    
            q_bot(reply_token,Qdict['6-3-C'])
            qname = '6-3-C'
            qtag = Q_name.index('7') 
    elif qtag==(Q_name.index('6B')+1) and ans[hos][qnaire]['6B']=='1' : 
        if not('6-4' in ans[hos][qnaire]):
            q_bot(reply_token,Qdict['6-4'])
            qname = '6-4' 
            qtag = Q_name.index('7') 
    elif qtag==(Q_name.index('6B')+1) and ans[hos][qnaire]['6B']=='2' : 
        if not('6-5.1' in ans[hos][qnaire]):
            q_bot(reply_token,Qdict['6-5.1'])
            qname = '6-5.1' 
            qtag = Q_name.index('7')
    elif qtag==(Q_name.index('6B')+1) and ans[hos][qnaire]['6B']=='3' : 
        if not('6-5.2' in ans[hos][qnaire]):
            q_bot(reply_token,Qdict['6-5.2'])
            qname = '6-5.2' 
        elif not('6-5.2-A' in ans[hos][qnaire]):
            q_bot(reply_token,Qdict['6-5.2-A'])
            qname = '6-5.2-A'
        elif not('6-5.2-B' in ans[hos][qnaire]):    
            q_bot(reply_token,Qdict['6-5.2-B'])
            qname = '6-5.2-B'
        elif not('6-5.2-C' in ans[hos][qnaire]):    
            q_bot(reply_token,Qdict['6-5.2-C'])
            qname = '6-5.2-C'
        elif not('6-5.2-D' in ans[hos][qnaire]):    
            q_bot(reply_token,Qdict['6-5.2-D'])
            qname = '6-5.2-D' 
            qtag = Q_name.index('7') 
    elif qtag==(Q_name.index('6B')+1) and ans[hos][qnaire]['6B']=='4' : 
        if not('6-6' in ans[hos][qnaire]):
            q_bot(reply_token,Qdict['6-6'])
            qname = '6-6' 
            qtag = Q_name.index('7') 
    elif qtag==(Q_name.index('6B')+1) and ans[hos][qnaire]['6B']=='5' : 
        if not('6-7' in ans[hos][qnaire]):
            q_bot(reply_token,Qdict['6-7'])
            qname = '6-7' 
            qtag = Q_name.index('7') 
    elif qtag==(Q_name.index('6B')+1) and ans[hos][qnaire]['6B']=='6' : 
        if not('6-8' in ans[hos][qnaire]):
            q_bot(reply_token,Qdict['6-8'])
            qname = '6-8' 
            qtag = Q_name.index('7') 
    elif qtag==(Q_name.index('6B')+1) and ans[hos][qnaire]['6B']=='7' : 
        if not('6-9' in ans[hos][qnaire]):
            q_bot(reply_token,Qdict['6-9'])
            qname = '6-9' 
            qtag = Q_name.index('7') 
    elif qtag==(Q_name.index('6B')+1) and ans[hos][qnaire]['6B']=='8' : 
        q_bot(reply_token,Qdict['7'])
        qname = '7' 
        qtag = Q_name.index('8') #問完後指標跳到下一題的名稱
    
    elif qtag==(Q_name.index('11_2')+1): #當問到11_2的下一題時，檢查選哪個選項.進入不同問題     
        if '5' in ans[hos][qnaire]:
            if '6-1-a' in ans[hos][qnaire]:
                if (ans[hos][qnaire]['5'] =='3' or ans[hos][qnaire]['5'] =='4') and ans[hos][qnaire]['6-1-a'] =='2':        
                    if not('DSM_5_1' in ans[hos][qnaire]):
                        q_bot(reply_token,Qdict['DSM_5_1'])
                        qname = 'DSM_5_1'
                    elif not('DSM_5_2' in ans[hos][qnaire]):  
                        q_bot(reply_token,Qdict['DSM_5_2'])
                        qname = 'DSM_5_2'     
                        qtag = Q_name.index('12')     
            elif '6-2.1-a' in ans[hos][qnaire]:
                if (ans[hos][qnaire]['5'] =='3' or ans[hos][qnaire]['5'] =='4') and ans[hos][qnaire]['6-2.1-a'] =='2':  
                    if not('DSM_5_1' in ans[hos][qnaire]):
                        q_bot(reply_token,Qdict['DSM_5_1'])
                        qname = 'DSM_5_1'
                    elif not('DSM_5_2' in ans[hos][qnaire]):  
                        q_bot(reply_token,Qdict['DSM_5_2'])
                        qname = 'DSM_5_2'     
                        qtag = Q_name.index('12')
            elif '6-2.2-a' in ans[hos][qnaire]:
                if (ans[hos][qnaire]['5'] =='3' or ans[hos][qnaire]['5'] =='4') and ans[hos][qnaire]['6-2.2-a'] =='2':        
                    if not('DSM_5_1' in ans[hos][qnaire]):
                        q_bot(reply_token,Qdict['DSM_5_1'])
                        qname = 'DSM_5_1'
                    elif not('DSM_5_2' in ans[hos][qnaire]):  
                        q_bot(reply_token,Qdict['DSM_5_2'])
                        qname = 'DSM_5_2'     
                        qtag = Q_name.index('12')
            else:
                q_bot(reply_token,Qdict['12'])
                qname = '12'     
                qtag = Q_name.index('13') #問完後指標跳到下一題的名稱
            
    else: #其他一般問題
        q_bot(reply_token,Qdict[Q_name[qtag]])
        qname = Q_name[qtag] #目前題目名稱
        # print('qtag_old',qtag,'qname_old',qname)
        qtag = qtag+1 #下一題之指標
        
    return qtag,qname
