from django.urls import path,re_path,include
from  .views import idc_list,idc_detail

#############################版本一##########################################
urlpatterns = [
    re_path('^$', idc_list),
    re_path('^(?P<pk>[0-9]+)/$', idc_detail),
]

#############################版本二##########################################
from .views import idc_list_v2,idc_detail_v2,api_root
from   rest_framework.urlpatterns import  format_suffix_patterns

urlpatterns = [
    re_path('^$', api_root),
    re_path('^idcs/$', idc_list_v2,name="idc-list"),
    re_path('^idcs/(?P<pk>[0-9]+)/$', idc_detail_v2,name="idc-detail"),
]
urlpatterns = format_suffix_patterns(urlpatterns)


#############################版本三##########################################
from . import  views
from   rest_framework.urlpatterns import  format_suffix_patterns
urlpatterns = [
    re_path('^$', views.api_root),
    re_path('^idcs/$', views.IdcList.as_view(),name="idc-list"),
    re_path('^idcs/(?P<pk>[0-9]+)/$', views.IdcDetail.as_view(),name="idc-detail"),
]
urlpatterns = format_suffix_patterns(urlpatterns)


#############################版本四##########################################

from . import  views
from   rest_framework.urlpatterns import  format_suffix_patterns
urlpatterns = [
    re_path('^$', views.api_root),
    re_path('^idcs/$', views.IdcList_v4.as_view(),name="idc-list"),
    re_path('^idcs/(?P<pk>[0-9]+)/$', views.IdcDetail_v4.as_view(),name="idc-detail"),
]
urlpatterns = format_suffix_patterns(urlpatterns)


#############################版本五##########################################
from . import  views
from   rest_framework.urlpatterns import  format_suffix_patterns
urlpatterns = [
    re_path('^$', views.api_root),
    re_path('^idcs/$', views.IdcList_v5.as_view(),name="idc-list"),
    re_path('^idcs/(?P<pk>[0-9]+)/$', views.IdcDetail_v5.as_view(),name="idc-detail"),
]
urlpatterns = format_suffix_patterns(urlpatterns)


#############################版本六##########################################
idc_list = views.IdcListViewset.as_view({
    "get":"list",
    "post":"create"
})

idc_detail = views.IdcListViewset.as_view({
    "get":"retrieve",
    "put":"update",
    "delete":"destroy"
})

urlpatterns = [
    re_path('^$', views.api_root),
    re_path('^idcs/$', idc_list,name="idc-list"),
    re_path('^idcs/(?P<pk>[0-9]+)/$', idc_detail,name="idc-detail"),
]

#########################版本七############################
from rest_framework.routers import DefaultRouter

route = DefaultRouter()
route.register("idcs",views.IdcListViewset_v7)

urlpatterns = [
    re_path('^', include(route.urls))
]