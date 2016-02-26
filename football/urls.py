from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    url(r'^$', views.play_sql, name='player'),
    url(r'^player/$',views.play_sql,name = 'player'),
    url(r'^$', views.soccerList, name='goallist'),
    url(r'^goallist/$',views.soccerList,name = 'goallist'),
)

