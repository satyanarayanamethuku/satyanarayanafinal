"""ppsproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from testapp import  views
from django.conf.urls import  url
from django.conf import settings
from django.conf.urls.static import static
from django.urls import reverse



urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/',views.home),
    path('dash/',views.dashbord),
    path('sub/',views.subject),
    path('vsub/',views.viewsubject,name='viewsubject1'),
    path('login/',views.login1),
    path('reg/',views.register),
    path('quiz/',views.quiz),
    path('admin1/',views.addadmin),
    path('profile/',views.adminprofile),
    path('student/',views.viewstudent),
    path('dash2/',views.dash2),
    path('state/',views.state),
    path('cbse/',views.cbse),
    path('noti/',views.notification),
    path('stuprofile/',views.studentprofileall,name='display'),
    url(r'^studelete/(?P<id>\d+)/$',views.studelete),
    url(r'^stuedit/(?P<pk>\d+)/$',views.StudentView.as_view()),
    path('application/',views.applicationFormCreate),
    path('stuapp/',views.StudentCreate),
    path('view/',views.view),
    path('apro/',views.viewprofile),
    path('all/',views.adminallprofile, name='add'),
    url(r'^admindelete/(?P<id>\d+)/$',views.admindeleteprofile),
    url(r'^adminedit/(?P<pk>\d+)/$',views.AdminUpdate.as_view()),
    path('examhome/',views.examhome),
    # path('examadd/',views.examcodeadd),
    path('examall/',views.examall, name='all'),
    url(r'^examdelete/(?P<id>\d+)/$',views.examcodedelete),
    url(r'^examupdate/(?P<pk>\d+)/$', views.ExamCodeUpdate.as_view()),
    path('sub1/',views.subject1),
    path('sub1all/',views.subject1all, name='sall'),
    url(r'^subject1del/(?P<id>\d+)/$',views.subject1del),
    url(r'^subjectupdate/(?P<pk>\d+)/$', views.SubjectCodeUpdate.as_view()),
    path('sub2/',views.subject2),
    path('addquestions/',views.addquestions),
    path('subcount/',views.subjectcodecount),
    path('pie/',views.ticket_class_view_3),
    path('count/',views.count),
    path('sbc/',views.statepie),
    path('qual/',views.qualification),
    path('mul/',views.multiplepiecharts),
    path('online/',views.onlineofflinecount),
    path('studentlogin/',views.studentloginCheck),
    path('get/',views.gettest),
    path('home/',views.home),
    path('vstu/',views.viewstudentprofile),
    path('escount/',views.totalexamcodewisecount),
    path('thank/',views.thankyou),
    path('viewallquestions/',views.viewallquestions, name='displayallquestions'),
    url(r'^questionsdelete/(?P<id>\d+)/$',views.questionsdelete),
    url(r'^questionsupdate/(?P<pk>\d+)/$',views.QuestionsUpdate.as_view()),
    path('upload/',views.uploadquestions),
    path('email123/',views.email123),
    path('forget/',views.forgetpassword),
    url(r'^multpleids/$', views.multpleids),
    path('notihome/',views.notification_screen),
    path('stunotification/',views.student_notication),
    path('logout/',views.logout),
    path('forgetlink/', views.forgetlink, name='forgetlink'),
    path('adminforget/',views.adminforget),
    path('sendsms/',views.sendsms)


    # url(r'^update/(?P<pk>\d+)/$', views.AdminUpdate.as_view()),

]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)