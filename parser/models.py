from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey
from django.db import models

class LegalCategory(MPTTModel):
    id = models.CharField(max_length=100, primary_key=True, verbose_name='ID')
    name = models.CharField(max_length=100, verbose_name='Название')
    type_id = models.IntegerField(null=True,blank=True, verbose_name='Тип')
    block = models.CharField(max_length=100, verbose_name='Блок')
    auto_update = models.BooleanField(default=False, verbose_name='Автообновление')

    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', verbose_name='Родитель')

    def __str__(self):
        """
        Returns a string representation of the object, in the form of
        "Category name (Parent: Parent name if exists else 'Root')"
        """
        return f"{self.name} (Родитель: {self.parent.name if self.parent else 'Корень'})"
    
    class MPTTMeta:
        order_insertion_by = ['name']


class Document(models.Model):
    eoNUMBER = models.CharField(max_length=100, verbose_name='Номер ЕО')
    category = models.ForeignKey(LegalCategory, on_delete=models.CASCADE, verbose_name='Категория')
    pdf_file = models.FileField(upload_to='documents/', verbose_name='PDF-файл')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    

    

