from django.db import models
from django.urls import reverse

# Create your models here.

class Subject(models.Model):
    sub_id=models.CharField(max_length=64)
    name = models.CharField(max_length=254)

    def __str__(self):
        return self.name

class Register(models.Model):
    name = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    bord=models.CharField(max_length=64)


class Quiz(models.Model):
    question = models.CharField(max_length = 200)
    choice_one = models.CharField(max_length = 200)
    choice_two = models.CharField(max_length = 200)
    choice_three = models.CharField(max_length = 200)
    choice_four = models.CharField(max_length = 200)
    choice_five = models.CharField(max_length = 200)
    answer = models.CharField(max_length = 200)


    def __str__(self):
        return self.question


class AdminRegister(models.Model):
    name = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    access=models.CharField(max_length=50)

    def __str__(self):
        return  self.name

    def get_absolute_url(self):
        return reverse('add')

class ApplicationFormClass(models.Model):
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    date_of_birth = models.DateField(default=False)
    board = models.CharField(max_length=20, default=False)
    fatherName = models.CharField(max_length=100)
    motherName = models.CharField(max_length=100)
    qualification = models.CharField(max_length=30)
    schoolName = models.CharField(max_length=30)
    schoolAddress = models.CharField(max_length=200)
    homeAddress = models.CharField(max_length=200)
    state = models.CharField(max_length=30)
    aadharNumber = models.CharField(max_length=15)
    phoneNumber = models.CharField(max_length=12)
    emailID = models.EmailField(max_length=40)
    personPhoto = models.ImageField(upload_to='images/')
    signaturePhoto = models.ImageField(upload_to='images/')
    username = models.CharField(max_length=30, unique=True)
    status = models.CharField(max_length=64)


    def __str__(self):
        return self.firstName

    def get_absolute_url(self):
        return reverse('display')


class ExamCode(models.Model):
    code = models.CharField(max_length=120)

    def __str__(self):
        return self.code

    def get_absolute_url(self):
        return reverse('all')

class SubjectCode(models.Model):
    scode = models.CharField(max_length=120)


    def __str__(self):
        return self.scode

    def get_absolute_url(self):
        return reverse('sall')


class Question(models.Model):
    question = models.CharField(max_length=64)
    option1  = models.CharField(max_length=64)
    option2  = models.CharField(max_length=64)
    option3  = models.CharField(max_length=64)
    option4  = models.CharField(max_length=64)
    answer   = models.CharField(max_length=64)
    examcode = models.CharField(max_length=64)
    subcode  = models.CharField(max_length=64)

    def __str__(self):
        return self.question

    def get_absolute_url(self):
        return reverse('displayallquestions')


class Score(models.Model):
    name = models.CharField(max_length=64)
    score = models.CharField(max_length=64)

    def __str__(self):
        return self.name

class Notification(models.Model):
    subject = models.CharField(max_length=500)
    date = models.CharField(max_length=500)
    body = models.CharField(max_length=1000)

    def __str__(self):
        return self.subject

class Image(models.Model):
    question = models.CharField(max_length=250)
    option1 = models.ImageField(upload_to='images1/')
    option2 = models.ImageField(upload_to='images1/')
    option3 = models.ImageField(upload_to='images1/')
    option4 = models.ImageField(upload_to='images1/')
    answer = models.ImageField(upload_to='images1/')
    examcode = models.CharField(max_length=64)
    subcode = models.CharField(max_length=64)

    def __str__(self):
        return self.question










