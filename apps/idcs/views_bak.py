from django.shortcuts import render
from django.http import  HttpResponse,JsonResponse
from  .models import Idc
from  .serializers import IdcSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import  JSONParser


#############################################版本一#################################################
class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        kwargs.setdefault('content_type', 'application/json')
        result = JSONRenderer().render(data)
        super().__init__(content=result, **kwargs)


def idc_list(request,*args,**kwargs):
    if request.method =="GET":
        queryset = Idc.objects.all()
        serializer = IdcSerializer(queryset,many=True)
        return  JSONResponse(serializer.data)
        # result = JSONRenderer().render(serializer.data)
        # return  HttpResponse(result,content_type="application/json")
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = IdcSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
            # result = JSONRenderer().render(serializer.data)
            # return HttpResponse(result,content_type="application/json")
    # return  HttpResponse("")

def idc_detail(request,pk,*args,**kwargs):
    try:
        idc = Idc.objects.get(pk=pk)
    except Idc.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == "GET":
        serializar = IdcSerializer(idc)
        return  JSONResponse(serializar.data)

    elif request.method == "PUT":
        content = JSONParser().parse(request)
        serializer = IdcSerializer(idc,data=content)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return  HttpResponse(serializer.errors,status=400)


    elif request.method == "DELETE":
        idc.delete()
        return HttpResponse(status=204)

#############################################版本二 装饰器#################################################

from rest_framework.decorators import api_view
from rest_framework import  status
from  rest_framework.response import Response

@api_view(['GET',"POST"])
def idc_list_v2(request, *args, **kwargs):
    if request.method == "GET":
        queryset = Idc.objects.all()
        serializer = IdcSerializer(queryset, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = IdcSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return  Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET',"PUT","DELETE"])
def idc_detail_v2(request,pk,*args,**kwargs):
    try:
        idc = Idc.objects.get(pk=pk)
    except Idc.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializar = IdcSerializer(idc)
        return  Response(serializar.data,status=status.HTTP_200_OK)

    elif request.method == "PUT":
        serializer = IdcSerializer(idc, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return  Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


    elif request.method == "DELETE":
        idc.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

from rest_framework.reverse import reverse
@api_view(['GET'])
def api_root(request, *args,**kwargs):
    return Response({
        "idcs": reverse("idc-list",request=request)
    })

#############################################版本三 类视图#重要看################################################
from rest_framework.views import  APIView
from   django.http import Http404

class IdcList(APIView):
    def get(self,request,*args,**kwargs):
        queryset = Idc.objects.all()
        serializer = IdcSerializer(queryset,many=True)
        return  Response(serializer.data)

    def post(self,request, *args, **kwargs):
        serializer = IdcSerializer(request.data)
        if serializer.is_valid():
            serializer.save()
            return  Response(serializer.data,status=status.HTTP_201_CREATED)
        return  Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)

class IdcDetail(APIView):
    def get_obj(self,pk):
        try:
            return  Idc.objects.get(pk=pk)
        except Idc.DoesNotExist:
            raise  Http404

    def get(self,request,pk,format=None):
        idc = self.get_obj(pk)
        serializer = IdcSerializer(idc)
        return Response(serializer.data)

    def put(self, request, pk,format=None):
        idc = self.get_obj(pk)
        serializer = IdcSerializer(idc,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return  Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk,format=None):
        idc = self.get_obj(pk)
        idc.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

from rest_framework.reverse import reverse
@api_view(['GET'])
def api_root(request, *args,**kwargs):
    return Response({
        "idcs": reverse("idc-list",request=request)
    })


#############################################版本四 mixins#重要看################################################
from rest_framework import  mixins,generics

class IdcList_v4(generics.GenericAPIView,
                 mixins.ListModelMixin,
                 mixins.CreateModelMixin):
    queryset = Idc.objects.all()
    serializer_class = IdcSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class IdcDetail_v4(generics.GenericAPIView,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin):

    queryset = Idc.objects.all()
    serializer_class = IdcSerializer
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

#############################################版本五 mixins_GenericAPIView#重要看################################################
from rest_framework import  mixins,generics


class IdcList_v5(generics.ListCreateAPIView):
    queryset = Idc.objects.all()
    serializer_class = IdcSerializer

class IdcDetail_v5(generics.RetrieveUpdateDestroyAPIView):
    queryset = Idc.objects.all()
    serializer_class = IdcSerializer

#############################################版本六 视图集##重要看# 作用合并请求的多种类型####################################
from rest_framework import  viewsets,mixins

class IdcListViewset(viewsets.GenericViewSet,
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin):
    queryset = Idc.objects.all()
    serializer_class = IdcSerializer

#############################################版本七 视图集##重要看# 作用合并请求的多种类型####################################
from rest_framework import  viewsets
class IdcListViewset_v7(viewsets.ModelViewSet):
    queryset = Idc.objects.all()
    serializer_class = IdcSerializer