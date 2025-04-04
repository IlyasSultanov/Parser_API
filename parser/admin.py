from django.contrib import admin

from .models import LegalCategory, BaseParsingResult


@admin.register(LegalCategory)
class BaseTaskAdmin(admin.ModelAdmin):
    list_display = ['name', 'type_id', 'block', 'auto_update', 'parent']
    readonly_fields = ['block', 'auto_update']
    list_filter = ['name', 'type_id']

@admin.register(BaseParsingResult)
class BaseResultAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'type_id', 'block', 'auto_update']