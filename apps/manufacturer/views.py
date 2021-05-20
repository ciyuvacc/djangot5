from django.shortcuts import render
from  manufacturer.serializer import  ManufacturerSerializer,ProductModelSerializer
from manufacturer.models import  Manufacturer,ProductModel
from    rest_framework import viewsets

# Create your views here.
class ManufacturerListViewset(viewsets.ModelViewSet):
    """
    retrieve:
        返回指定Manufacturer信息
    list:
        返回Manufacturer列表
    update:
        更新Manufacturer信息
    destroy:
        删除Manufacturer记录
    create:
        创建Manufacturer记录
    partial_update:
        更新部分字段
    """
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer



class ProductModelListViewset(viewsets.ModelViewSet):
    """
    retrieve:
        返回指定型号信息
    list:
        返回型号列表
    update:
        更新型号信息
    destroy:
        删除型号记录
    create:
        创建型号记录
    partial_update:
        更新部分字段
    """
    queryset = ProductModel.objects.all()
    serializer_class = ProductModelSerializer