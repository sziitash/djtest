#-*- coding: utf-8 -*-
from django import forms
from django.shortcuts import render_to_response
from models import AuthUser, GoalNum
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from django.contrib.auth.hashers import make_password#, check_password
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import Permission, User
# from django.contrib.auth.decorators import permission_required
import datetime
import simplejson
import paramiko

class LoginForm(forms.Form):
    username = forms.CharField(label="用户名/账号")
    password = forms.CharField(label="密码",widget=forms.PasswordInput)

def mylogin(request):
    error = []
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            username = data['username']
            password = data['password']
            if login_validate(request,username,password):
                response = HttpResponseRedirect('/account/profile/')
                response.set_cookie('username',username,3600)
                return response
            else:
                error.append('请输入正确的密码！')
        else:
            error.append('请输入账号/密码！')
    else:
        form = LoginForm()
    return render_to_response('login.html',{'error':error,'form':form})


def login_validate(request, username, password):
    rtvalue = False
    user = authenticate(username=username,password=password)
    if user is not None:
        if user.is_active:
          auth_login(request, user)
          return True
    return rtvalue

class RegisterForm(forms.Form):
    username = forms.CharField(label="用户名/账号")
    email = forms.EmailField(label="邮件地址")
    password = forms.CharField(label="密码",widget=forms.PasswordInput)
    password2= forms.CharField(label='确认密码',widget=forms.PasswordInput)
    def pwd_validate(self,p1,p2):
        return p1==p2

def register(request):
    error=[]
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            username = data['username']
            email = data['email']
            password = data['password']
            password2= data['password2']
            # user = AuthUser()
            try:
                AuthUser.objects.get(username=username)
            except:
                if form.pwd_validate(password, password2):
                    User = AuthUser()
                    User.username = username
                    User.password = make_password(password, None, 'pbkdf2_sha256')
                    User.email = email
                    User.is_superuser = 0
                    User.is_staff = 0
                    User.is_active = 1
                    User.date_joined = datetime.datetime.now()
                    User.save()
                    login_validate(request,username,password)
                    response = HttpResponseRedirect('/account/profile/')
                    response.set_cookie('username',username,3600)
                    return response
                    # return HttpResponseRedirect('/account/profile/')
                else:
                    error.append('请确认二次密码与新密码是否一致！')
            else:
                error.append('该账号已存在！')
    else:
        form = RegisterForm()
    return render_to_response('register.html',{'form':form,'error':error})

def mylogout(request):
    response = HttpResponseRedirect('/account/login/')
    #清理cookie里保存username
    response.delete_cookie('username')
    return response
    # return HttpResponseRedirect('/account/login/')

class ChangepwdForm(forms.Form):
    old_pwd = forms.CharField(label="旧密码",widget=forms.PasswordInput)
    new_pwd = forms.CharField(label="新密码",widget=forms.PasswordInput)
    new_pwd2 = forms.CharField(label="确认新密码",widget=forms.PasswordInput)

def changepassword(request,username):
    error = []
    if request.method == 'POST':
        form = ChangepwdForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(username=username,password=data['old_pwd'])
            if user is not None:
                if data['new_pwd']==data['new_pwd2']:
                    newuser = AuthUser.objects.get(username=username)
                    newuser.password = make_password(data['new_pwd'], None, 'pbkdf2_sha256')
                    newuser.save()
                    # return HttpResponseRedirect('/account/login/')
                    response = HttpResponseRedirect('/account/login/')
                    #清理cookie里保存username
                    response.delete_cookie('username')
                    return response
                else:
                    error.append('请确认二次密码与新密码是否一致！')
            else:
                error.append('请输入正确的旧密码！')
        else:
            error.append('Please input the required domain')
    else:
        form = ChangepwdForm()
    return render_to_response('changepassword.html',{'form':form,'error':error})

def myprofile(request):
    try:
        user = request.COOKIES['username']
    except:
        return HttpResponseRedirect('/account/login/')
    else:
        testlist = GoalNum.objects.order_by('-id')[0]
        return render_to_response('welcome.html' ,{'user':user,'namelist':testlist})

class delplayerForm(forms.Form):
    name = forms.CharField()

def delplayer(request,name):
    try:
        user = request.COOKIES['username']
    except:
        return HttpResponseRedirect('/account/login/')
    else:
        # if not 'goal_num.delete_goalnum' in get_all_permissions():
        if request.user.has_perm( 'football.delete_goalnum'):
            delplayer = GoalNum.objects.get(name=name)
            delplayer.delete()
            return HttpResponseRedirect('/account/profile/')
        else:
            return HttpResponseRedirect('/account/profile/')

def fpsresultinfo(request):
    try:
        user = request.COOKIES['username']
    except:
        return HttpResponseRedirect('/account/login/')
    else:
        if request.user.has_perm( 'football.change_goalnum'):
            testfile = open("c:/test.txt","r")
            infolist = testfile.readlines()
            newlist = []
            for i in range(len(infolist)):
                a = infolist[i].replace("\n","").split(",")
                testdict = {"count":i+1,"Max":a[0],"Min":a[1],"AVG":a[2]}
                newlist.append(testdict)
            #return HttpResponse(simplejson.dumps(newlist,ensure_ascii = False))
            return render_to_response('line.html',{'listinfo':newlist})
            # return newlist
        else:
            return HttpResponseRedirect('/account/profile/')

class runuiaForm(forms.Form):
    testcasename = forms.CharField(required=False)

def runuiapage(request):
    error=[]
    # pagetext = "web端运行uiautomator"
    form = runuiaForm(request.POST,auto_id=False)
    return render_to_response('runuia.html' ,{"form":form,"error":error})

def runuiatest(request):
    if request.method == 'POST':
        form = runuiaForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            testcase = data["testcasename"]
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect("172.29.0.17",22,"root","admin",timeout=5)
            cmd = "am broadcast -a com.example.broadcastservicetest.RunUiaService --es tcname "+testcase
            stdin,stdout,stderr = ssh.exec_command(cmd)
            ssh.close()
            return HttpResponseRedirect('/account/login/')
        else:
            return HttpResponseRedirect('/account/login/')
    


