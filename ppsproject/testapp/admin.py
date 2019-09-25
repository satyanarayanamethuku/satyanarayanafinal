from django.contrib import admin
from .models import Subject,Register,Quiz,AdminRegister,ApplicationFormClass,Question,Score,Notification,Image
# Register your models here.
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['sub_id','name']

admin.site.register(Subject,SubjectAdmin)

class RegisterAdmin(admin.ModelAdmin):
    list_display = ['name', 'password','bord']

admin.site.register(Register,RegisterAdmin)

admin.site.register(Quiz)
class Adminside(admin.ModelAdmin):
    list_display = ['id','name','password']
admin.site.register(AdminRegister,Adminside)

admin.site.register(ApplicationFormClass)

admin.site.register(Question)

class AdminScore(admin.ModelAdmin):
    list_display = ['name', 'score']

admin.site.register(Score, AdminScore)

admin.site.register(Notification)

admin.site.register(Image)