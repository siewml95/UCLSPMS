from django.contrib import admin
from .models import Invitation
# Register your models here.

class InvitationAdmin(admin.ModelAdmin):
    fields = ('email',)



admin.site.register(Invitation,InvitationAdmin)
