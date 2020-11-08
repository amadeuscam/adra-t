from django.contrib import admin
from .models import Persona, Alimentos, AlmacenAlimentos, Hijo,Profile

# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth']


class HijoInline(admin.TabularInline):
    model = Hijo

@admin.register(Hijo)
class HijoAdmin(admin.ModelAdmin):
    search_fields = ("nombre_apellido",)
    list_display = ("nombre_apellido", "persona", "modificado_por",)


class PersonaAdmin(admin.ModelAdmin):
    inlines = [HijoInline, ]
    list_filter = ("fecha_nacimiento",'covid',)
    search_fields = ("nombre_apellido", "numero_adra",)
    list_display = ("nombre_apellido", "numero_adra", "mensaje",'covid',)
    ordering = ('nombre_apellido', 'numero_adra')


admin.site.register(Persona, PersonaAdmin)

# admin.site.register(Hijo)
admin.site.register(Alimentos)

admin.site.register(AlmacenAlimentos)
