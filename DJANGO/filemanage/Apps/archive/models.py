from django.db.models.enums import IntegerChoices
from django.utils import timezone
from django.db import models
from django.db.models.deletion import DO_NOTHING,SET_NULL,PROTECT
from filemanage.settings import stage_type
import os
import uuid
# Create your models here.


def upload_to(instance, filename):
    # 将文件名加上随机字符，避免被直接访问
    name, ext = os.path.splitext(filename)
    filename = '{}_{}{}'.format(name, uuid.uuid4().hex[:10], ext)
    return "PDgroup/{0}/{1}/{2}".format(instance.product.product_name, instance.get_stage_display(), filename)

# 发放类型
class StageType(models.Model):
    id=models.AutoField(primary_key=True)
    
    stage_name=models.CharField(max_length=16,unique=True,verbose_name='发放类型')
    stage_mark=models.CharField(max_length=16,verbose_name='发放标记')
    remark=models.CharField(max_length=30,blank=True,null=True,verbose_name='备注')

    class Meta:
        verbose_name = '发放类型'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.stage_name


# 产品信息库
class Product(models.Model):
    id=models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=64, verbose_name='产品名称', unique=True)
    product_code = models.CharField(
        max_length=32, verbose_name='产品代码', unique=True, blank=True)
    description = models.CharField(
        max_length=256, verbose_name='产品说明', blank=True)

    class Meta:
        verbose_name = '产品信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.product_name


# 发放单
class Archive(models.Model): 
    # get_stage_display()   取出选项对应的字段    

    archive_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    archive_no = models.CharField(max_length=18, verbose_name='文件发放单号')
    
    product= models.ForeignKey('Product',on_delete=PROTECT,verbose_name='产品名称')

    stage = models.IntegerField(
        default=10, choices=stage_type, verbose_name='发放类型')

    description = models.CharField(max_length=256, verbose_name='发放说明')

    username = models.CharField(max_length=30, verbose_name='发放人')

    file = models.FileField(upload_to=upload_to,
                            max_length=255, blank=True, verbose_name='发放文件')
    bom = models.FileField(
        upload_to=upload_to, max_length=255, blank=True, verbose_name='发放清单')
    add_time = models.DateTimeField(default=timezone.now, verbose_name='发放时间')

    class Meta:
        verbose_name = '文档发放信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.archive_no+" "+self.product.product_name
    
    def to_dict(self):
        item={}
        item['archive_id'] = str(self.archive_id)
        item['archive_no']=self.archive_no
        item['product']=self.product.product_name
        item['product_code'] = self.product.product_code
        item['stage'] = self.get_stage_display()
        item['description']=self.description
        item['username'] = self.username
        item['add_time'] = self.add_time.strftime("%Y-%m-%d %H:%M")

        return item

