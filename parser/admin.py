from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import LegalCategory

class PostAdmin(MPTTModelAdmin):
    list_display = ('name', 'type_id', 'block', 'auto_update', 'parent')
    list_filter = ('block', 'auto_update')
    search_fields = ('name', 'type_id')

admin.site.register(LegalCategory, PostAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'type_id', 'block', 'auto_update')


