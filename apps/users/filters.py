import django_filters
from django.contrib.auth import  get_user_model
User = get_user_model()


class UserFilter(django_filters.FilterSet):
    # username = django_filters.CharFilter(lookup_expr='icontains')   不区分大小写
    username = django_filters.CharFilter(lookup_expr='contains')

    class Meta:
        model = User
        fields = ['username']