from  .models import Idc
from  .serializers import IdcSerializer
from rest_framework import viewsets

class IdcListViewset(viewsets.ModelViewSet):
    """
    retrieve:
        返回指定IDC信息
    list:
        返回idc列表
    update:
        更新IDC信息
    destroy:
        删除IDC记录
    create:
        创建IDC记录
    partial_update:
        更新部分字段
    """
    queryset = Idc.objects.all()
    serializer_class = IdcSerializer