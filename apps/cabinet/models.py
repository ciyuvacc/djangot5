from django.db import models
from  idcs.models import Idc

# Create your models here.
class Cabinet(models.Model):
    idc         = models.ForeignKey(Idc,verbose_name="所在机房",on_delete="DO_NOTHING")
    name        = models.CharField(max_length=255)

    def __str__(self):
        return  self.name

    class Meta:
        db_table = "resources_cabinet"
        ordering = ["id"]