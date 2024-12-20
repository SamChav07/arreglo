from django.contrib import admin
from .models import *

# Register your models here.
class EG_admin(admin.ModelAdmin):
    list_display = ('id',)  # Asegúrate de que sea una tupla, incluso con un solo elemento

class OpV_admin(admin.ModelAdmin):
    list_display = ('id',)

class FxV_admin(admin.ModelAdmin):
    list_display = ('id',)

class pMxV_admin(admin.ModelAdmin):
    list_display = ('id',)

class sMrx_admin(admin.ModelAdmin):
    list_display = ('id',)

admin.site.register(Elim_Gauss, EG_admin)
admin.site.register(Ope_combinadas, OpV_admin)
admin.site.register(MultiFxC, FxV_admin)
admin.site.register(PropMxV, pMxV_admin)
admin.site.register(SmMrx, sMrx_admin)