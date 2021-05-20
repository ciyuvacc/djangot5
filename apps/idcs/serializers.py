from rest_framework import  serializers
from .models import  Idc
from django.utils.translation import ugettext_lazy as _





class IdcSerializer(serializers.Serializer):
    """
    Idc 序列化类
    """
    error_messages = {'blank': _('字段不能为空'),
                      'required': _('字段必须存在')}




    id          = serializers.IntegerField(read_only=True)
    name        = serializers.CharField(required=True,
                                        max_length=32,
                                        label="机房名称",
                                        help_text="机房名称",
                                        error_messages={'blank': _('字段不能为空'),
                                                        'required': _('字段必须存在')})
    address     = serializers.CharField(required=True,
                                        max_length=200,
                                        label="机房地址",
                                        help_text="机房地址",
                                        error_messages={'blank': _('字段不能为空'),
                                                        'required': _('字段必须存在')})
    phone       = serializers.CharField(required=True,
                                        max_length=15,
                                        label="联系电话",
                                        help_text="联系电话",
                                        error_messages=error_messages)
    email       = serializers.EmailField(required=True,
                                         label="邮件地址",
                                         help_text="邮件地址",
                                         error_messages=error_messages)
    letter      = serializers.CharField(required=True,
                                        max_length=5,
                                        label="机房简称",
                                        help_text="机房简称",
                                        error_messages=error_messages)


    def create(self, validated_data):
        return   Idc.objects.create(**validated_data)

    def update(self, instance, validated_data):
        print(instance,validated_data)
        instance.name = validated_data.get("name",instance.name)
        instance.address = validated_data.get("address",instance.address)
        instance.phone = validated_data.get("phone",instance.phone)
        instance.letter = validated_data.get("letter",instance.letter)
        instance.email = validated_data.get("email",instance.email)
        instance.save()
        return  instance
