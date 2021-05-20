from rest_framework import serializers
from servers.models import Server,IP,NetworkDevice
from manufacturer.models import Manufacturer,ProductModel

class IPSerializer(serializers.ModelSerializer):
    """
    IP序列化
    """

    class Meta:
        model = IP
        fields = "__all__"



class NetworkDeviceSerializer(serializers.ModelSerializer):
    """
    网卡序列化
    """

    class Meta:
        model = NetworkDevice
        fields = "__all__"



class ServerSerializer(serializers.ModelSerializer):
    """
    服务器序列化
    """

    class Meta:
        model = Server
        fields = "__all__"
        # fields = ("ip", "hostname", "cpu", "mem", "disk", "os", "sn", "manufacturer", "model_name", "uuid")


class ServerAutoReportSerializer(serializers.Serializer):

    """
    服务器序列化
    """
    ip          = serializers.IPAddressField(required=True)
    hostname    = serializers.CharField(required=True,max_length=20)
    cpu         = serializers.CharField(required=True,max_length=50)
    mem         = serializers.CharField(required=True,max_length=200)
    os          = serializers.CharField(required=True,max_length=50)
    sn          = serializers.CharField(required=True,max_length=50)
    # disk          = serializers.CharField(required=True,max_length=50)
    # manufacturer= serializers.PrimaryKeyRelatedField(many=True,queryset=Manufacturer.objects.all())
    manufacturer= serializers.CharField(required=True)
    model_name  = serializers.CharField(required=True)
    uuid        = serializers.CharField(required=True,max_length=50)
    network     = serializers.JSONField(required=True)



    def validate_manufacturer(self,value):
        print("自定义字段验证二")
        print(value)
        try:
            return  Manufacturer.objects.get(vendor_name__exact=value)
        except Manufacturer.DoesNotExist:
            return self.create_manufacturer(value)

    def validate(self, attrs):
        print("对象验证三")

        # network = attrs["network"]
        # del attrs["network"]
        print(attrs)
        manufacturer_obj = attrs["manufacturer"]
        try:
            attrs["model_name"] = manufacturer_obj.productmodel_set.get(model_name__exact=attrs["model_name"])
        except ProductModel.DoesNotExist:
            attrs["model_name"] = self.create_product_model(manufacturer_obj,attrs["model_name"])
        return  attrs



    def create_server(self,validated_data):
        print("create")
        network = validated_data.pop("network")
        server_obj = Server.objects.create(**validated_data)
        self.check_server_network_device(server_obj, network)
        return server_obj



    def create(self,validated_data):
        print(validated_data)

        uuid = validated_data["uuid"].lower()
        sn = validated_data["sn"].lower()

        try:
            if sn == uuid or sn == "" or sn.startswith("vmware"):
                #虚机
                server_obj = Server.objects.get(uuid__icontains=uuid)
            else:
                #物理机
                server_obj = Server.objects.get(sn__icontains=sn)
        except Server.DoesNotExist:
            return  self.create_server(validated_data)
        else:
            return  self.update_server(server_obj,validated_data)

    def update_server(self, instance, validated_data):
        print("update")
        instance.hostname = validated_data.get("hostname",instance.hostname)
        instance.cpu = validated_data.get("cpu",instance.cpu)
        instance.mem = validated_data.get("mem",instance.mem)
        instance.disk  = validated_data.get("disk",instance.disk)
        instance.os  = validated_data.get("os",instance.os)
        self.check_server_network_device(instance,validated_data['network'])
        instance.save()
        return  instance


    def check_server_network_device(self,server_obj,network):
        """
        检查指定服务器有没有这些网卡设备,并做关联.
        :return:
        """
        print("检查网卡")
        network_device_queryset = server_obj.networkdevice_set.all()
        current_network_device_queryset = []
        for device in  network:
            try:
                network_device_obj = network_device_queryset.get(name__exact=device["name"])
            except NetworkDevice.DoesNotExist:
                """
                网卡不存在
                """
                network_device_obj = self.create_network_device(server_obj,device)
            print(device["ips"])
            self.check_ip(network_device_obj,device["ips"])
            current_network_device_queryset.append(network_device_obj)

        for network_device_obj in list(set(network_device_queryset)-set(current_network_device_queryset)):
            network_device_obj.delete()

    def check_ip(self,network_device_obj,ifnets):
        print("检查ip")
        ip_qeuryset = network_device_obj.ip_set.all()
        current_ip_queryset = []
        for ifnet in ifnets:
            try:
                ip_obj = ip_qeuryset.get(ip_addr__exact=ifnet["ip_addr"])
            except IP.DoesNotExist:
                ip_obj = self.create_ip(network_device_obj,ifnet)
            current_ip_queryset.append(ip_obj)
        for ip_obj in set(ip_qeuryset) - set(current_ip_queryset):
            ip_obj.delete()


    def create_ip(self,network_device_obj,ifnet):
        ifnet["device"] = network_device_obj
        return  IP.objects.create(**ifnet)



    def create_network_device(self,server_obj,device):
        ips = device.pop("ips")
        device["host"] = server_obj
        network_device_obj = NetworkDevice.objects.create(**device)
        return  network_device_obj



    def create_manufacturer(self,vendor_name):
        # print("创建数据manuacturer")
        return  Manufacturer.objects.create(vendor_name=vendor_name)

    def create_product_model(self,manufacturer_obj,model_name):
        print("创建数据product_model")
        return  ProductModel.objects.create(model_name=model_name,vendor=manufacturer_obj)

    def to_representation(self, instance):
        print("序列化后的数据")
        # print(instance)
        ret = {
            "hostname": instance.hostname,
            "ip": instance.ip
        }
        return  ret


    # def to_internal_value(self, data):
    #     print("数据接收的元数据一")
    #     print(data)
    #     return data