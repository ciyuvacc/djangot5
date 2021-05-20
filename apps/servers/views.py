from rest_framework import viewsets
from servers.models import Server,IP,NetworkDevice
from servers.serializer import ServerSerializer,IPSerializer,NetworkDeviceSerializer,ServerAutoReportSerializer
from rest_framework import mixins
from django_filters.rest_framework import  DjangoFilterBackend
from .filters import  ServerFilter

# class ServerAutoReportViewset(viewsets.ModelViewSet):
class ServerAutoReportViewset(mixins.CreateModelMixin,viewsets.GenericViewSet):
    """
    create:
        创建Server记录
    """
    queryset = Server.objects.all()
    serializer_class = ServerAutoReportSerializer






class ServerListViewset(viewsets.ModelViewSet):
    """
    create:
        创建Server记录
    """
    queryset = Server.objects.all()
    serializer_class = ServerSerializer
    # filter_backends = (DjangoFilterBackend,)

    filter_class = ServerFilter
    # filter_fields = ("hostname")

class IPListViewset(viewsets.ModelViewSet):
    """
    retrieve:
        返回指定IP信息
    list:
        返回IP列表
    """
    queryset = IP.objects.all()
    serializer_class = IPSerializer




class NetworkDeviceListViewset(viewsets.ModelViewSet):
    """
    retrieve:
        返回指定NetworkDevice信息
    list:
        返回NetworkDevice列表
    """
    queryset = NetworkDevice.objects.all()
    serializer_class = NetworkDeviceSerializer