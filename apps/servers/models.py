from django.db import models
from manufacturer.models import Manufacturer,ProductModel
from idcs.models import Idc
from cabinet.models import  Cabinet
# Create your models here.

class Server(models.Model):
    ip                  = models.CharField("管理IP",db_index=True,unique=True,max_length=15,help_text="管理IP")
    hostname            = models.CharField("主机名",max_length=30,db_index=True,unique=True,help_text="主机名")
    cpu                 = models.CharField("CPU",max_length=50,help_text="CPU")
    mem                 = models.CharField("内存",max_length=32,help_text="内存")
    disk                = models.CharField("磁盘",max_length=200,help_text="磁盘")
    os                  = models.CharField("操作系统",max_length=50,help_text="OS")
    sn                  = models.CharField("SN",max_length=50,db_index=True,help_text="SN")
    manufacturer        = models.ForeignKey(Manufacturer,verbose_name="制造商",on_delete=models.DO_NOTHING,help_text="制造商")
    model_name          = models.ForeignKey(ProductModel,verbose_name="服务型号",on_delete=models.DO_NOTHING,help_text="服务型号")
    rem_card_ip         = models.CharField("远程管理卡IP",max_length=15,unique=True,db_index=True,help_text="远程管理卡IP")
    idc                 = models.ForeignKey(Idc,verbose_name="所在机房",null=True,on_delete=models.DO_NOTHING,help_text="所在机房")
    cabinet             = models.ForeignKey(Cabinet,verbose_name="所在机柜",null=True,on_delete=models.DO_NOTHING,help_text="所在机柜")
    cabinet_position    = models.CharField("机柜内位置",null=True,max_length=20,help_text="机柜内位置")
    uuid                = models.CharField("UUID",db_index=True,unique=True,max_length=50,help_text="服务器的UUID")
    last_check          = models.DateTimeField("检测时间",db_index=True,help_text="检测时间",auto_now=True)


    def __str__(self):
        return self.ip

    class Meta:
        db_table = "resources_server"
        ordering = ["id"]


class NetworkDevice(models.Model):
    """
    网卡模型
    """
    name            = models.CharField("网卡设备名",max_length=20,db_index=True,help_text="网卡设备名")
    mac_address     = models.CharField("MAC地址",max_length=30,help_text="MAC地址")
    host            = models.ForeignKey(Server,verbose_name="所在服务器",on_delete=models.CASCADE,help_text="所在服务器")
    remark          = models.CharField("备注",max_length=300,help_text="备注")

    def __str__(self):
        return self.name
    class Meta:
        db_table = "resources_network_device"

class IP(models.Model):
    """
    IP模型
    """
    ip_addr         = models.CharField("IP地址",max_length=15,db_index=True,unique=True)
    netmask         = models.CharField("子网掩码",max_length=15,help_text="子网掩码")
    device          = models.ForeignKey(NetworkDevice,verbose_name="所在网卡",on_delete=models.CASCADE,help_text="所在网卡")
    remark          = models.CharField("备注", max_length=300, help_text="备注")


    def __str__(self):
        return self.ip_addr
    class Meta:
        db_table = "resources_ip"