from rest_framework import  serializers
from  idcs.serializers  import IdcSerializer
from cabinet.models import Cabinet
from idcs.models import Idc


#############################################################一###############################################################
class CabinetSerializer(serializers.Serializer):
    idc     = serializers.SerializerMethodField()
    name    = serializers.CharField(required=True,label="机柜序号")

    def get_idc(self, obj):
        print(obj.idc)
        return {
            "id":obj.id,
            "name":obj.name
        }



    def to_representation(self, instance):
        idc_obj = instance.idc
        ret =   super(CabinetSerializer,self).to_representation(instance)
        ret['idc'] = {
            "id":idc_obj.id,
            "name":idc_obj.name
        }
        return  ret



    def to_internal_value(self, data):
        """
        反序列化的第一步,那到的是提交过来的原始数据:queryset=> request.GET,request.POST
        :param data:
        :return:
        """
        print(data)
        return  super(CabinetSerializer, self).to_internal_value(data)

    def create(self,validated_data):
        print(validated_data)
        raise  serializers.ValidationError("create error")
        return Cabinet.objects.create(**validated_data)