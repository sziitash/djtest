from django.conf.urls import patterns, url
import views
import fpsresult

urlpatterns = patterns('',
    # url(r'^/$', views.mylogin, name='login'),
    url(r'^login/$',views.mylogin,name = 'login'),
    url(r'^register/$',views.register,name = 'register'),
    # url(r'^$', views.login, name='login'),
    url(r'^logout/$',views.mylogout,name = 'logout'),
    url(r'^profile/$',views.myprofile,name = 'profile'),
    url(r'^changepassword/(?P<username>\w+)/$',views.changepassword,name = 'changepassword'),
    url(r'^delplayer/(?P<name>\w+)/$',views.delplayer,name = 'delplayer'),
    url(r'^postfpsresult/$',fpsresult.postfpsresult,name = 'postfpsresult'),
    #url(r'^fpsinfo/$',views.fpsresultinfo,name = 'fpsinfo'),
    url(r'^fpsinfo/$',fpsresult.fpsresultinfo,name = 'fpsinfo'),
    url(r'^fpstest/$',fpsresult.postmoduleinfo,name = 'fpstest'),
    url(r'^runuiapage/$',views.runuiapage,name = 'runuiapage'),
    url(r'^runuia/$',views.runuiatest,name = 'runuia'),
)
