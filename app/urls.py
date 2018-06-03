from django.conf.urls import url
from django.contrib import admin
from . import views
from django.views.generic.base import TemplateView
from django.views import generic
from django.urls import reverse_lazy, path, re_path

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='app/home.html'), name='home'),
    url(r'^inscription/$', views.inscription, name='inscription'),
    url(r'^activation/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activation, name='activation'),
    
    url(r'^liste_requete/$', views.ListeRequete.as_view(), name='liste_requete'),
    url(r'^detail_requete/(?P<pk>\d+)', views.DetailRequete.as_view(), name='detail_requete'),
    url(r'^creer_requete/$', views.creer_requete, name='creer_requete'),
    url(r'^editer_requete/(?P<pk>[0-9]+)', views.RequeteUpdate.as_view(), name='editer_requete'),
    url(r'^supprimer_requete/(?P<pk>[0-9]+)', views.RequeteDelete.as_view(), name='supprimer_requete'),
    url(r'^mes_requetes/$', views.mes_requetes, name ='mes_requetes'),
    
    url(r'^profil/(?P<username>[\w.@+-]+)', views.profil, name='profil'),
    url(r'^mon_profil/$', views.mon_profil, name ='mon_profil'),

    url(r'^editer_suivi/(?P<idRequete>[0-9]+)', views.SuiviRequeteUpdate.as_view(), name ='editer_suivi'),
    url(r'^suivi/(?P<idRequete>[0-9]+)', views.suivi, name='suivi'),

]