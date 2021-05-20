from rest_framework import serializers

class UserSrializer(serializers.Serializer):
    """
    用户序列表
    """
    id              = serializers.IntegerField()
    username        = serializers.CharField(required=True)
    email           = serializers.EmailField(required=True)




    def __str__(self):
        return  self.username

    class Meta():
        db_table = "resoure_user"
