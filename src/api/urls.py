from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

'''
API endpoints:

GET /api/youth
    Param: activeOnly=True (if activeOnly param not specified, default value is False)
    Param: search=john (optional search param filters search results)
    Returns: Array of youth objects

GET /api/youth/ (pk is an int which represents a youth's primary key)
    Returns: Youth object for the youth with that PK

PUT /api/youth/PK/progress-chart (create or update operation for the progress chart.
    Once a user presses "save changes", the front end will persist changes with this PUT request)
    Returns: response code 201
'''

urlpatterns = [
    url(r'^youth/$', views.YouthList.as_view(), name='youth-list'),
    url(r'^youth/(?P<youth_id>[0-9]+)/$', views.YouthDetail.as_view(), name='youth-detail'),
    url(r'^youth/(?P<youth_id>[0-9]+)/forms/$', views.YouthForms.as_view(), name='youth-forms'),
    url(r'^placement-type/$', views.PlacementTypeList.as_view(), \
        name='youth-list-placement-type'),
    url(r'^form-type/$', views.FormTypeList.as_view(), \
        name='youth-list-form-type'),
    url(r'^visit/(?P<youth_visit_id>[0-9]+)/change-placement/$',
        views.YouthChangePlacement.as_view(),
        name='youth-change-placement'),
    url(r'^visit/(?P<youth_visit_id>[0-9]+)/mark-exited/$', views.YouthMarkExited.as_view(), \
        name='youth-mark-exited'),
    url(r'^visit/(?P<youth_visit_id>[0-9]+)/add-extension/$', views.YouthAddExtension.as_view(), \
        name='youth-add-extension'),
    url(r'^visit/(?P<youth_visit_id>[0-9]+)/edit-note/$', views.YouthEditNote.as_view(), \
        name='youth-edit-note'),

    url(r'^export/youth-visits/', views.ExportYouthVisits.as_view(), \
        name='export-youth-vists'),

    url(r'docs/$', views.api_docs, name='docs')
]
urlpatterns = format_suffix_patterns(urlpatterns)
