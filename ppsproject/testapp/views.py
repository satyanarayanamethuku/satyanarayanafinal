from django.shortcuts import render,redirect
from .models import  Subject,Register,Quiz,AdminRegister,ApplicationFormClass,ExamCode,SubjectCode,Score,Notification,Image
from django.views.generic import UpdateView
from .models import Question
import csv
import os
import io
from django.core.mail import send_mail
from django.http import  HttpResponse
from django.db.models import Q
from django.shortcuts import render_to_response
import random
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
import http.client


# Create your views here.
# name=''
# pas=' '
# username1=''
# dob1=''


def home(request):
    return render(request,'testapp/home.html')

def dashbord(request):
    return render(request,'testapp/dash.html')

def subject(request):
    if request.method=='POST':
        id=request.POST['id1']
        name=request.POST['name']
        sub=Subject.objects.create(sub_id=id, name=name)
        sub.save()
        return redirect('/vsub')
    return render(request,'testapp/subject.html')

def viewsubject(request):
    form=Subject.objects.all()
    return  render(request,'testapp/viewsubject.html',{'form':form})


def login1(request):
    if request.method=='POST':
        # global name, pas
        name = request.POST['t1']
        name1=request.session['name1']=name
        pas = request.POST['t2']
        try:
            dbuser=AdminRegister.objects.get(name=name,password=pas)
            if dbuser:
                return render(request,'testapp/dash.html',{'name':name, 'access':dbuser.access})
            else:
                return HttpResponse('login fail')
        except AdminRegister.DoesNotExist:
            messages.error(request, "username and passwod does not match")
            return  render(request,'testapp/login.html')

    return render(request,'testapp/login.html')


def register(request):
    if request.method=='POST':
        name = request.POST['p1']
        pas  = request.POST['p2']
        bord = request.POST['p3']
        if Register.objects.filter(name=name).exists():
            return HttpResponse('this name already exist in database use another name')
        else:
            reg=Register(name=name, password=pas,bord=bord)
            reg.save()
            return redirect('/login')

    return  render(request, 'testapp/reg.html')

# def quiz(request):
#     return render(request,'testapp/quiz.html')

def quiz(request):
	questions = Quiz.objects.all()
	context = {'questions':questions}
	return render(request, 'testapp/quiz.html', context)

def addadmin(request):
    if request.method=='POST':

        name1=request.POST['a1']
        password1=request.POST['a2']
        access=request.POST['a3']
        add=AdminRegister(name=name1, password=password1,access=access)
        add.save()
        return HttpResponse('sucessfully add admin')
    return  render(request,'testapp/addadmin.html')


def adminprofile(request):
    return render(request, 'testapp/profile.html')

def viewstudent(request):
    form=Register.objects.all()
    return render(request,'testapp/disp.html',{'form':form})

def dash2(request):
    form=Register.objects.filter(bord='sate')
    return render(request,'testapp/dash2.html',{'form':form})

def state(request):
    form = ApplicationFormClass.objects.filter(board='SB')
    return render(request, 'testapp/state.html', {'form': form})

def cbse(request):
    form = ApplicationFormClass.objects.filter(board='CBSE')
    return render(request, 'testapp/cbse.html', {'form': form})


# @login_required(login_url='/login/')
def notification(request):
    return  render(request,'testapp/noti.html')


def studentprofileall(request):
    user_list=ApplicationFormClass.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(user_list, 5)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(request,'testapp/spro.html',{'users':users})

def studelete(request,id):
    stu=ApplicationFormClass.objects.get(id=id)
    messages.info(request,'deleted this student profile')
    stu.delete()
    return redirect('/stuprofile')

class StudentView(SuccessMessageMixin,UpdateView):
    model = ApplicationFormClass
    fields =['firstName','lastName']
    success_message = "student profile suessfully updated"



def applicationFormCreate(request):
    if request.method=='POST':
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        dob = request.POST.get('dob')
        board = request.POST.get('board')
        father = request.POST.get("father")
        mother = request.POST.get("mother")
        qualification = request.POST.get('qualification')
        sname = request.POST.get('sname')
        saddress = request.POST.get('saddress')
        haddress = request.POST.get('haddress')
        anum = request.POST.get('aadharnum')
        phonenum = request.POST.get('phonenum')
        email = request.POST.get('email')
        personphoto =request.FILES['personphoto']
        signaturephoto = request.FILES['signaturephoto']
        state = request.POST.get('state')
        number = '19'+'{:03d}'.format(random.randrange(1, 999))
        username = (state + board + qualification+ number)
        status=request.POST['hidden1']
        # password = dob
        af = ApplicationFormClass(firstName = fname, lastName = lname, date_of_birth = dob, board = board, fatherName = father, motherName = mother, qualification = qualification, schoolName = sname, schoolAddress = saddress, homeAddress = haddress, aadharNumber = anum, phoneNumber = phonenum, emailID = email, personPhoto = personphoto,  signaturePhoto = signaturephoto,state = state, username = username, status=status)
        af.save()
        sub="Email From Best Scholarship"
        msg = "Hello Mr/Ms." + fname + "." + "\n" + "\n"+ "Your Application for Best Scholarship has been submitted successfully"+"\n"+ "Username:" + username + "\n" + "Password:" + dob + "\n" + "Please use the above Username and Dob to login" + "\n" + "Good Luck" + "\n" + "-Team Best Scholarship"
        send_mail(sub,msg,'dontreply@ibest.co.in',[email])

        return HttpResponse('mail sent successfully')
        # return redirect('/stuprofile')

    return render(request,'testapp/application.html')


def StudentCreate(request):
    if request.method=='POST':
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        dob = request.POST.get('dob')
        board = request.POST.get('board')
        father = request.POST.get("father")
        mother = request.POST.get("mother")
        qualification = request.POST.get('qualification')
        sname = request.POST.get('sname')
        saddress = request.POST.get('saddress')
        haddress = request.POST.get('haddress')
        anum = request.POST.get('aadharnum')
        phonenum = request.POST.get('phonenum')
        request.session['number']=phonenum
        email = request.POST.get('email')
        personphoto = request.FILES['personphoto']
        signaturephoto = request.FILES['signaturephoto']
        state = request.POST.get('state')
        number = '19'+'{:03d}'.format(random.randrange(1, 999))
        username = (state + board + qualification+ number)
        status = request.POST['hidden1']

        if ApplicationFormClass.objects.filter(emailID=email).exists():
            return HttpResponse('email id taken in database use another emaild')
        else:
            af = ApplicationFormClass(firstName = fname, lastName = lname, date_of_birth = dob, board = board, fatherName = father, motherName = mother, qualification = qualification, schoolName = sname, schoolAddress = saddress, homeAddress = haddress, aadharNumber = anum, phoneNumber = phonenum, emailID = email, personPhoto = personphoto,  signaturePhoto = signaturephoto,state = state, username = username,status=status)
            af.save()
            subject="Email From Best Scholarship"
            from_email='best.scholarstest@gmail.com'
            to=email
            html_content = render_to_string('testapp/stuonline.html', {'varname':username ,'id':dob})
            text_content = strip_tags(html_content)
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            # return redirect('/sendsms')
            return HttpResponse('mail sent successfully')






    return render(request,'testapp/application12.html')


def view(request):
    if request.method=='POST':
        # name=request.POST['b1']
        name=request.session['name1']
        password=request.POST['b2']
        a=AdminRegister.objects.get(name=name)
        a.password=password
        a.save()
        return redirect('/login')
    return render(request,'testapp/listpro.html')

def viewprofile(request):
    name=request.session['name1']
    db=AdminRegister.objects.get(name=name)
    return render(request,'testapp/apro.html',{'db':db})

def adminallprofile(request):
    form=AdminRegister.objects.all()
    return render(request,'testapp/adllpro.html',{'form':form})

def admindeleteprofile(request,id):
    form=AdminRegister.objects.get(id=id)
    form.delete()
    return redirect('/all')

class AdminUpdate(UpdateView):
    model  = AdminRegister
    fields = ['name','password','access']


def examhome(request):
    if request.method=='POST':
        c1=request.POST['t1']
        c2=request.POST['t2']
        c3=request.POST['t3']
        c=c1+c2+c3
        if ExamCode.objects.filter(code=c).exists():
            messages.info(request, 'this exam code already is created')
            return  redirect('/examhome')
            # return render(request, 'testapp/examhome.html',{'msg':"this exam code already is created"})
        else:
            add=ExamCode(code=c)
            add.save()
            return redirect('/examall')
    return render(request,'testapp/examhome.html')

# def examcodeadd(request):
#     return render(request,'testapp/examadd.html')

def examall(request):
    form=ExamCode.objects.all()
    return render(request,'testapp/examall.html',{'form':form})

def examcodedelete(request,id):
    form=ExamCode.objects.get(id=id)
    form.delete()
    return redirect('/examall')

class ExamCodeUpdate(UpdateView):
    model  = ExamCode
    fields = ['code']


def subject1(request):
    if request.method=='POST':
        s1 = request.POST['p1']
        s2 = request.POST['p2']
        s3 = request.POST['p3']
        s  = s1 + s2 + s3
        if SubjectCode.objects.filter(scode=s).exists():
            messages.info(request, 'this subject code is already created')
            return  redirect('/sub1')
        else:
            add=SubjectCode(scode=s)
            add.save()
            return redirect('/sub1all')

    return render(request,'testapp/subject1.html')

def subject1all(request):
    form=SubjectCode.objects.all()
    return render(request,'testapp/subject1all.html',{'form':form})

def subject1del(request,id):
    form=SubjectCode.objects.get(id=id)
    form.delete()
    return redirect('/sub1all')

class SubjectCodeUpdate(SuccessMessageMixin, UpdateView):
    model = SubjectCode
    fields = ['scode']
    success_message = 'this subject code  successfully updated'


def subject2(request):
    code=ExamCode.objects.all()
    scode=SubjectCode.objects.all()
    return render(request,'testapp/subject2.html',{"code":code,"scode":scode})



def addquestions(request):
    if request.method=='POST':
        name=request.POST['c1']
        a=SubjectCode.objects.filter(scode__iexact=name).count()
        if a >= 1:
            return HttpResponse("we cant add more than five questions")
        else:
            q = request.POST['q1']
            a = request.POST['o1']
            b = request.POST['o2']
            c = request.POST['o3']
            d = request.POST['o4']
            e = request.POST['o5']
            f = request.POST['a1']
            add=Quiz(question=q,choice_one=a,choice_two=b,choice_three=c,choice_four=d,choice_five=e,answer=f)
            add.save()
            return HttpResponse('add sucessully')
    return render(request,'testapp/subject2.html')


def subjectcodecount(request):
    form  = SubjectCode.objects.filter(scode='gk09CBSE').count()
    form1 = SubjectCode.objects.filter(scode='sc10ICSE').count()
    return render(request,'testapp/subcount.html',{'form':form,'form1':form1})


def count(request):  # total number students register count
    form=ApplicationFormClass.objects.all().count()
    return  HttpResponse(form)


def ticket_class_view_3(request): # student reister each state wise count and represent in pie chart
    a  = ApplicationFormClass.objects.filter(state='AP').count()
    k  = ApplicationFormClass.objects.filter(state='KA').count()
    t  = ApplicationFormClass.objects.filter(state='TS').count()
    ar = ApplicationFormClass.objects.filter(state='AR').count()
    as1= ApplicationFormClass.objects.filter(state='AS').count()
    br = ApplicationFormClass.objects.filter(state='BR').count()
    cg = ApplicationFormClass.objects.filter(state='CG').count()
    dl = ApplicationFormClass.objects.filter(state='DL').count()
    ga = ApplicationFormClass.objects.filter(state='GA').count()
    gj = ApplicationFormClass.objects.filter(state='GJ').count()
    hr = ApplicationFormClass.objects.filter(state='HR').count()
    hp = ApplicationFormClass.objects.filter(state='HP').count()
    jk = ApplicationFormClass.objects.filter(state='JK').count()
    gh = ApplicationFormClass.objects.filter(state='JH').count()
    kl = ApplicationFormClass.objects.filter(state='KL').count()
    mp = ApplicationFormClass.objects.filter(state='MP').count()
    mh = ApplicationFormClass.objects.filter(state='MH').count()
    mn = ApplicationFormClass.objects.filter(state='MN').count()
    ml = ApplicationFormClass.objects.filter(state='ML').count()
    mz = ApplicationFormClass.objects.filter(state='MZ').count()
    nl = ApplicationFormClass.objects.filter(state='NL').count()
    or1= ApplicationFormClass.objects.filter(state='OR').count()
    pb = ApplicationFormClass.objects.filter(state='PB').count()
    rj = ApplicationFormClass.objects.filter(state='RJ').count()
    skm= ApplicationFormClass.objects.filter(state='SK').count()
    tn = ApplicationFormClass.objects.filter(state='TN').count()
    tr = ApplicationFormClass.objects.filter(state='TR').count()
    up = ApplicationFormClass.objects.filter(state='UP').count()
    uk = ApplicationFormClass.objects.filter(state='UK').count()
    wb = ApplicationFormClass.objects.filter(state='WB').count()
    xdata = ["Andhra Pradesh","Karnataka","telagan",'Arunachal Pradesh','Assam','Bihar','Chhattisgarh','Delhi','Goa','Gujarat','Haryana','Himachal Pradesh','Jammu and Kashmir','Jharkhand','Kerala','Madhya Pradesh','Maharashtra','Manipur','Meghalaya','Mizoram','Nagaland','Orissa','Punjab','Rajasthan','Sikkim','Tamil Nadu','Tripura','Uttar Pradesh','Uttarakhand','West Bengal']
    ydata = [a,k,t,ar,as1,br,cg,dl,ga,gj,hr,hp,jk,gh,kl,mp,mh,mn,ml,mz,nl,or1,pb,rj,skm,tn,tr,up,uk,wb]
    extra_serie = {"tooltip": {"y_start": "", "y_end": "total"}}
    chartdata = {'x': xdata, 'y1': ydata, 'extra1': extra_serie}
    charttype = "pieChart"


    data = {
        'charttype': charttype,
        'chartdata': chartdata,
        'extra': {
            'x_is_date': False,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': False,
            'chart_attr': {
                'labelType': '\"percent\"',
            }
        }

    }
    return render_to_response('testapp/ticket_class.html', data)

def statepie(request): # student register board wise count represents in pie chart
    s = ApplicationFormClass.objects.filter(board='SB').count()
    c = ApplicationFormClass.objects.filter(board='CBSE').count()
    i = ApplicationFormClass.objects.filter(board='ICSE').count()
    xdata1 = ["state", "cbse", "icse"]
    ydata1 = [s, c, i]

    extra_serie = {"tooltip": {"y_start": "", "y_end": " total"}}
    chartdata = {'x': xdata1, 'y1': ydata1, 'extra1': extra_serie}
    charttype = "pieChart"

    data = {
        'charttype': charttype,
        'chartdata': chartdata,
        'extra': {
            'x_is_date': False,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': False,
            'chart_attr': {
                'labelType': '\"percent\"',
            }
    }
    }
    return render_to_response('testapp/ticket_class1.html', data)

def qualification(request): # student each claass count and presents in pie charts using django-nvd3
    six   = ApplicationFormClass.objects.filter(qualification='06').count()
    seven = ApplicationFormClass.objects.filter(qualification='07').count()
    eight = ApplicationFormClass.objects.filter(qualification='08').count()
    nine  = ApplicationFormClass.objects.filter(qualification='09').count()
    ten   = ApplicationFormClass.objects.filter(qualification='10').count()
    xdata1= ["six class", "seven class", "eight class","nine class","ten class"]
    ydata1= [six,seven,eight,nine,ten]

    extra_serie = {"tooltip": {"y_start": "", "y_end": " total"}}
    chartdata = {'x': xdata1, 'y1': ydata1, 'extra1': extra_serie}
    charttype = "pieChart"

    data = {
        'charttype': charttype,
        'chartdata': chartdata,
        'extra': {
            'x_is_date': False,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': False,

            'chart_attr': {

                'labelType': '\"percent\"',
            }
        }
    }
    return render_to_response('testapp/ticket_class2.html', data)

def multiplepiecharts(request): # here within one page we can display two pie charts
    s = ApplicationFormClass.objects.filter(board='SB').count()
    c = ApplicationFormClass.objects.filter(board='CBSE').count()
    i = ApplicationFormClass.objects.filter(board='ICSE').count()
    xdata1 = ["state", "cbse", "icse"]
    ydata1 = [s, c, i]

    extra_serie = {"tooltip": {"y_start": "", "y_end": " cal"}}
    chartdata = {'x': xdata1, 'y1': ydata1, 'extra1': extra_serie}
    charttype = "discreteBarChart"
    six   = ApplicationFormClass.objects.filter(qualification='06').count()
    seven = ApplicationFormClass.objects.filter(qualification='07').count()
    eight = ApplicationFormClass.objects.filter(qualification='08').count()
    nine  = ApplicationFormClass.objects.filter(qualification='09').count()
    ten   = ApplicationFormClass.objects.filter(qualification='10').count()
    xdata2 = ["six class", "seven class", "eight class", "nine class", "ten class"]
    ydata2 = [six, seven, eight, nine, ten]

    extra_serie1 = {"tooltip": {"y_start": "", "y_end": " cal"}}
    chartdata2   = {'x': xdata2, 'y1': ydata2, 'extra2': extra_serie1}
    charttype2   = "pieChart"

    data = {
        'charttype': charttype,
        'chartdata': chartdata,

        'chartdata2':chartdata2,
        'charttype2':charttype2,
        'extra2': {
            'x_is_date': False,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': False,

            'chart_attr': {

                'labelType': '\"percent\"',
            }
        }

    }
    return render_to_response('testapp/multiplepie.html', data)


def onlineofflinecount(request):   # pie chart represents about the numbers of people register offline and online count by django_nvd3 module
    on  = ApplicationFormClass.objects.filter(status='online').count()  # count inbuilt function in orm
    off = ApplicationFormClass.objects.filter(status='offline').count()

    xdata1 = ["online", "offline"]
    ydata1 = [on,off]

    extra_serie = {"tooltip": {"y_start": "", "y_end": " total"}}   # total is variable name any name can used
    chartdata   = {'x': xdata1, 'y1': ydata1, 'extra1': extra_serie}
    charttype   = "pieChart"

    data = {
        'charttype': charttype,
        'chartdata': chartdata,
        'extra': {
            'x_is_date': False,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': False,
            'chart_attr': {
                'labelType': '\"percent\"',
            }
    }
    }
    return render_to_response('testapp/ticket_class3.html', data)

 # if request.method == 'GET':
    #     return render(request, 'testapp/ssss.html')
def home(request):  # questions can upload csv file and manual questions can add and all questions are stored in database

    if request.method=='POST':
        try:
            csv_file = request.FILES['file']
            if not csv_file.name.endswith('.csv'):
                return render(request, 'testapp/ssss.html', {'msg': 'only csv file accepts'})

            data_set = csv_file.read().decode('UTF-8')
            io_string = io.StringIO(data_set)
            next(io_string)
            for row in csv.reader(io_string, delimiter=',', quotechar="|"):
                a = Question.objects.filter(examcode=row[6]).count()
                if a >= 12: # doing testing 12 to change 120 questions total
                    return render(request, 'testapp/ssss.html',{"msg4": "we can not add more than 12 questions in csv file this code"})
                else:
                    b = Question.objects.filter(subcode=row[7]).count()
                    if b >= 3: # doing testing 3  to change 30 questions total
                        return render(request, 'testapp/ssss.html', {"msg5": "completed 3 questions from this subject code"})
                    else:
                        created = Question(question=row[0], option1=row[1], option2=row[2], option3=row[3], option4=row[4],
                                           answer=row[5], examcode=row[6], subcode=row[7])
                        created.save()
            return HttpResponse("sucessfully file upload")

        except:


            g = request.POST['e1']
            h = request.POST['s1']

            total = Question.objects.filter(examcode=g).count()
            if total >= 12:  # doing testing 12 to change 120 questions total
                return render(request, 'testapp/subject2.html', {"msg1": "more than 12 question we cant be add this exam code"})
            else:
                b = Question.objects.filter(subcode=h).count()
                if b >= 3: # doing testing 3 to change 30 question total
                    return render(request, 'testapp/subject2.html', {"msg2": "we cont add more than 3 question this subject code"})
                else:
                    a = request.POST['q']
                    b = request.POST['q1']
                    c = request.POST['q2']
                    d = request.POST['q3']
                    e = request.POST['q4']
                    answer = request.POST['a']
                    if answer == 'ans1':
                        answer = b
                    elif answer == 'ans2':
                        answer = c
                    elif answer == 'ans3':
                        answer = d
                    elif answer == 'ans4':
                        answer = e
                    else:
                        return HttpResponse("<h4> please select answer</h4>")

                    add = Question(question=a, option1=b, option2=c, option3=d, option4=e, answer=answer, examcode=g,
                                   subcode=h)
                    add.save()
                    messages.success(request,"sucessfullu upload questions")



    return render(request, 'testapp/ssss.html',)


def studentloginCheck(request):  # student username and password checking from databse if not exists then error wel come
    if request.method=='POST':
        # global username1,dob1
        username1 = request.POST.get('username')
        request.session['username1']=username1
        dob1 = request.POST['dob']
        afc = ApplicationFormClass.objects.filter(username=username1, date_of_birth=dob1)
        if afc:
            return render(request,"testapp/studentscreen.html",{'afc':afc})
        else:
            messages.error(request,'username and password does not match')
            return redirect('/studentlogin')
        # return render(request,"testapp/studentloginpage.html",{"msg":"Invalid login credentials"})
    return render(request, 'testapp/studentloginpage.html')


def gettest(request):  # student login sucessfully take test click based on username exam question wel come
    time  = datetime.now()
    t     = datetime.strftime(time,"%Y")[2:4]
    # print(t)
    name  = request.session['username1']
    a     =  ApplicationFormClass.objects.get(username=name)
    query = a.qualification+a.board+t
    # print(query)
    s  = Question.objects.filter(examcode__iexact=query)
    return  render(request,'testapp/a.html',{'contacts':s,'query':query,'a':a,})

def viewstudentprofile(request):     # student after login sucessfully if view the profile display information using session
    studentusername = request.session['username1']
    dbuser          = ApplicationFormClass.objects.get(username=studentusername)
    return render(request,'testapp/v.html',{"dbuser":dbuser})

def totalexamcodewisecount(request):   #here counting each examcode and subject code how many questions are there
    if request.method=='POST':
        query  = request.POST['name1']
        sum    = Question.objects.filter(examcode__iexact=query).count() | Question.objects.filter(subcode__iexact=query).count()
        return render(request, 'testapp/e1.html', {'sum': sum, 'query': query})

    return render(request,'testapp/ssss.html')

def thankyou(request):  #here validating answer and score wel be store in database
    questions = Question.objects.all()
    # image1 = Image.objects.all()
    # global score
    score = 0

    for question in questions:
        correct_answer = question.answer
        # print(correct_answer)
        entered_answer = request.POST.get(str(question.id))
        if (entered_answer == correct_answer):
            score += 1
    # except:
    #
    #     for img in image1:
    #         co_answer= img.answer
    #         print(co_answer)
    #         entered1_answer = request.POST.get(str(question.id))
    #         if (entered1_answer == co_answer):
    #             score+=1
    name=request.session['username1']
    add=Score(name=name,score=score)
    add.save()
    return render(request, 'testapp/thank.html',{'score':score})


def viewallquestions(request):     # all questions retrive from database and pagination used in table formate
    form      = Question.objects.all()
    page      = request.GET.get('page', 1)
    paginator = Paginator(form, 5)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(request, 'testapp/questions.html',{'users':users})

def questionsdelete(request, id):   # questions can delete by using orm
    form = Question.objects.get(id=id)
    form.delete()
    return redirect('/viewallquestions')


class QuestionsUpdate(UpdateView):  # questions can update by using class based view
    model  = Question
    fields = ['question', 'option1', 'option2', 'option3', 'option4', 'answer', 'examcode','subcode']


def uploadquestions(request):
    return render(request, 'testapp/upload.html')



def email123(request): # html template file can send to the email
    subject, from_email, to = 'Subject', 'best.scholarstest@gmail.com', 'satyanarayanamethuku7259@gmail.com'

    html_content = render_to_string('testapp/mail_template.html', {'varname': 'vinod kumar','id':'KACBSE092019385'})  # render with dynamic value
    text_content = strip_tags(html_content)  # Strip the html tag. So people can see the pure text at least.

    # create the email, and attach the HTML version as well.
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    return HttpResponse("sucessfully sent")


def forgetpassword(request):  #student can forget the username and email to send the details
    if request.method=="POST":
        try:
            email  = request.POST['email']
            dbuser = ApplicationFormClass.objects.get(emailID=email)
            sub    = "Email From Best Scholarship"
            msg    = "Your regid id is"+'\n'+'\n'+dbuser.username+'\n'+"password"+'\n'+str(dbuser.date_of_birth)
            send_mail(sub,msg,"best.scholarstest@gmail.com", [email])
            return render(request, 'testapp/forgetemail.html')

        except ApplicationFormClass.DoesNotExist:
            messages.info(request, "your email id is not exists in database and  first register and login")
            return render(request, "testapp/forget.html")

    return render(request, 'testapp/forget.html')

def multpleids(request):  # here multiple ids deleteing at time
    if request.method=='POST':
        add = request.POST.getlist('t1')

        ApplicationFormClass.objects.filter(id__in=add).delete()
        return redirect('/stuprofile')
    return render(request, 'testapp/spro.html')


def notification_screen(request):  # here notication screen adding data in database
    if request.method=='POST':
        subject = request.POST['t1']
        date = request.POST['d1']
        info = request.POST['c1']
        add = Notification(subject=subject, date=date, body=info)
        add.save()
        messages.success(request, "sucessfully upload data")
    return render(request, 'testapp/notihome.html')

def student_notication(request):  # here student well get notification after login sucess
    form = Notification.objects.all()
    return render(request, 'testapp/stunotication.html',{"form":form})

def logout(request):
    try:
        del request.session['username1']

    except KeyError:
        pass

    return render(request, 'testapp/studentloginpage.html')


def forgetlink(request):   #
    if request.method=='POST':
        password=request.POST['p1']
        password1=request.POST['p2']
        if password==password1:
            a=AdminRegister.objects.get(name='ssss')
            a.password=password
            a.save()
            return HttpResponse("your password sucessfully and login")
        else:
            return HttpResponse("both password does not match")
    return  render(request, 'testapp/forgetlink.html')


def adminforget(request):
    return  render(request, 'testapp/adminforget.html')

def sendsms(request):


    conn = http.client.HTTPSConnection("api.msg91.com")
    payload = '''{
          "sender": "BESTQT",
          "route": "4",
          "country": "91",
          "sms": [
            {
              "message": "messsge sending from django application",
              "to": [
               '7259837437'

              ]
            }
          ]
        }'''

    headers = {
        'authkey': "241022AVD5q0z2z5bb5d749",
        'content-type': "application/json"
    }

    conn.request("POST", "/api/v2/sendsms?country=91", payload, headers)

    res = conn.getresponse()
    data = res.read()
    return HttpResponse(data.decode("utf-8"))










