from django.db import models

# Create your models here.
class User_Info(models.Model):
    uid = models.CharField(max_length=50,null=False,default='')         #user_id
    name = models.CharField(max_length=255,blank=True,null=False)       #LINE名字
    pic_url = models.CharField(max_length=255,null=False)               #大頭貼網址
    mtext = models.JSONField(max_length=255,blank=True,null=True)      #文字訊息紀錄
    mdt = models.DateTimeField(auto_now=True)                           #物件儲存的日期時間
    state = models.CharField(max_length=255,blank=True,null=False)      #問卷填寫狀態(read/write)
    hos = models.CharField(max_length=255,default='', blank=True,null=True)   #醫院名
    qnaire = models.CharField(max_length=255,default='', blank=True,null=True)   #問卷名
    qname = models.CharField(max_length=255,default='', blank=True,null=True)   #題目name
    qtag = models.IntegerField(default=0, blank=True, editable=True)   #問卷List指標
    ans = models.JSONField(blank=True,default={})   #問卷答案
    
    def __str__(self):
        return self.uid
