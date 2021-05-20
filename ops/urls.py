"""ops URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path,include,re_path
from    rest_framework.documentation import  include_docs_urls
from   rest_framework.routers import  DefaultRouter
from idcs.views import  IdcListViewset
from users.views import UserViewset
from cabinet.views import CabinetListViewset
from manufacturer.views import ManufacturerListViewset,ProductModelListViewset
from servers.views import ServerAutoReportViewset,IPListViewset,NetworkDeviceListViewset,ServerListViewset




route = DefaultRouter()
route.register("idcs",IdcListViewset,base_name='idcs')
route.register("users",UserViewset,base_name='users')
route.register("cabinet",CabinetListViewset,base_name='cabinet')
route.register("manufacturer",ManufacturerListViewset,base_name='manufacturer')
route.register("ProductModel",ProductModelListViewset,base_name='ProductModel')
route.register("Server",ServerAutoReportViewset,base_name='Server')
route.register("ServerList",ServerListViewset,base_name='ServerList')
route.register("IP",IPListViewset,base_name='IP')
route.register("NetworkDevice",NetworkDeviceListViewset,base_name='NetworkDevice')


urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('', include('idcs.urls')),
    # re_path( '^/', include('idcs.urls')),
    path("",include(route.urls)),
    # path("api-auth",include("rest_framework.urls",namespace="rest_framework")),
    path("api-auth",include("rest_framework.urls",)),
    path("docs/",include_docs_urls("运维平台接口文档"))
]
