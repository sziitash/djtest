# -*- coding: utf8 -*-
##from django.template.loader import get_template
##from django.template import Context
from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404
import datetime,requests#, MySQLdb
from models import GoalNum
#from models import Team
#import django.utils
import simplejson

def play_sql(request):
    json_list = {}
    for i in range(2,12):
        player_goal_list = GoalNum.objects.get(id=i)
        player_name = player_goal_list.name
        player_goal = player_goal_list.goalnum
        player_group = player_goal_list.groupname
##	player_team_id = player_goal_list.team_id
##	player_team_list = Team.objects.get(id=player_team_id)
##	player_team = player_team_list.name
        #json_list={'name':player_name,'goal':player_goal,'team':player_group}
        json_list[i-1] = {'name':player_name,'goal':player_goal,'team':player_group}
#	return render_to_response('b.html',locals())
    return HttpResponse(simplejson.dumps(json_list,ensure_ascii = False))

def soccerList(request):
    a = requests.get("http://m.zhibo8.cc/json/paihang/zhongchao_player_goal.htm")
    ##print a.json().get("playerlist")[:10]
    resultList = a.json().get("playerlist")[:20]
    htmlList = []
    for i in resultList:
        toList = i.items()
        num = toList[5][1]
        group = toList[4][1]
        name = toList[3][1]
        goal = toList[2][1]
        resulthtml = {'num':num,'name':name,'group':group,'goal':goal}
        htmlList.append(resulthtml)
    return render_to_response('soccerlist.html',{'listinfo':htmlList})
    
    
    



