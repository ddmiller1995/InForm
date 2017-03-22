from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from forms import views

urlpatterns = [
    url(r'^forms/$', views.FormList.as_view()),
    url(r'^forms/(?P<pk>[0-9]+)/$', views.FormDetail.as_view()),
    url(r'^$', views.index)
]

urlpatterns = format_suffix_patterns(urlpatterns)