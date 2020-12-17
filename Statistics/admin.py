from django.contrib import admin
from .models import YearlyTable
# Register your models here.
class YearlyAdmin(admin.ModelAdmin):
    #'Action_taken_at',
    list_display = ('index','productdate','timestamp', 'open','low','low','high','volume')
    ordering = ('timestamp','volume')

admin.site.register(YearlyTable,YearlyAdmin)
