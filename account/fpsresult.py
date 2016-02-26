#coding=utf-8
#__author__ = 'libinhui'
from django import forms
from django.shortcuts import render_to_response
from models import AuthUser, Fpsresult
#from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from django.contrib.auth.hashers import make_password#, check_password
from django.http import HttpResponse,HttpResponseRedirect
import datetime, simplejson


class fpsForm(forms.Form):
    module = forms.CharField()
    testcase = forms.CharField()
    result = forms.CharField()
    count = forms.CharField()

def postfpsresult(request):
    form = fpsForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        modulename = data['module']
        testcase = data['testcase']
        result = data['result']
        count = data['count']
        fpsresult = Fpsresult()
        fpsresult.modulename = modulename
        fpsresult.testcase = testcase
        fpsresult.result = result
        fpsresult.count = count
        fpsresult.save()
    return HttpResponse("成功录入")

class fpsinfoForm(forms.Form):
    module = forms.CharField()
    testcase = forms.CharField()

def postmoduleinfo(request):
    form = fpsinfoForm(request.POST)
    return render_to_response('fpstest.html',{'form':form})

def fpsresultinfo(request):
    resultlist = []
    testresult = []
    form = fpsinfoForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        modulename = data['module']
        testcase = data['testcase']
        testresult = Fpsresult.objects.values("result","count").filter(modulename=modulename).filter(testcase=testcase)
        maxavg = testresult[0].get("count")
        resultlist = eval(testresult[0].get("result"))
    return render_to_response('newfpslist.html',{'listinfo':resultlist,"testcase":testcase,"modulename":modulename,"maxavg":maxavg})


