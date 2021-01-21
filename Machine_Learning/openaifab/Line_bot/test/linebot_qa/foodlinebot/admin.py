from django.contrib import admin
from .models import *

class User_Info_Admin(admin.ModelAdmin):
    list_display = ('id','uid','name','pic_url','mtext','mdt','state','hos','qnaire','qname','qtag','ans')
admin.site.register(User_Info,User_Info_Admin)
