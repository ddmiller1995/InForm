from django.conf.urls import url
from forms import views

urlpatterns = [
    url(r'^forms/$', views.form_list),
    url(r'^forms/(?P<pk>[0-9]+)/$', views.form_detail),
]