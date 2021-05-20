from rest_framework import viewsets
from django.contrib.auth.models import  User
from .serializer import  UserSrializer
from django_filters.rest_framework import  DjangoFilterBackend
from .filters import  UserFilter
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import  IsAuthenticated,AllowAny

# from rest_framework.pagination import  PageNumberPagination
# from .pagination import Pagination

from django.contrib.auth import  get_user_model
User = get_user_model()

class UserViewset(viewsets.ReadOnlyModelViewSet):
    """
    retrieve:
        返回指定用户信息
    list:
        返回用户列表
    """
    queryset = User.objects.all()

    ###################分页
    serializer_class = UserSrializer
    # 分页. setting 配置 page_size
    # pagination_class = PageNumberPagination
    # # pagination_class = Pagination


    # def get_queryset(self):
    #     queryset = super(UserViewset, self).get_queryset()
    #     username = self.request.query_params.get("username",None)
    #     if username:
    #         queryset = queryset.filter(username__icontains=username)
    #     return  queryset
    # filter_backends = (DjangoFilterBackend,)
    ############## 搜索
    filter_class = UserFilter
    filter_fields = ("username",)


    ############### 权限验证
    # authentication_classes = (SessionAuthentication,)
    # permission_classes = (AllowAny,)