from django.contrib import admin
from .models import Keyword,Project
# Register your models here.

class KeywordAdmin(admin.ModelAdmin):
    pass
class ProjectAdmin(admin.ModelAdmin):
    pass

admin.site.register(Project,admin.ModelAdmin)
admin.site.register(Keyword,KeywordAdmin)
