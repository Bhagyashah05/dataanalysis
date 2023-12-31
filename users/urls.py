"""
URL configuration for users project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
# from myapp.views import rel_value
from myapp.views import rel_form
from userloginactivitycount.views import login_activity
from userloginactivitycount.views import userlogin
from myapp.views import mainpage
from timespentbyuser.views import session_activity
from client_logins.views import usage_graph
from client_session_time.views import userids
from clientselect.views import setvariables
# from clientselect.views import dataanalysis
from myapp.views import phases


urlpatterns = [
    path('admin/', admin.site.urls),
    path('activeuser/', rel_form, name='activeuser'),
    # path('', rel_form, name='rel_value'),
    path('login-activity/', login_activity, name='login_activity'),
    path('login-activity/user', userlogin, name='userlogin'),

    path('', setvariables, name='setvariables'),
    path('sessiontime/',session_activity, name='session_time'),
    path('client_logins/', usage_graph, name='client_usage_graph'),
    path('client_session/', userids, name='client_session'),
    path('mainpage/', mainpage, name='mainpage'),
    path('phase/', phases, name='phase'),


    # path('data_analysis/', dataanalysis, name='dataanalysis'),




]

