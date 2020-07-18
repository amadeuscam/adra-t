from django.contrib import admin
from .models import Persona, Alimentos, AlmacenAlimentos, Hijo,Profile

# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'photo']


class HijoInline(admin.TabularInline):
    model = Hijo


class PersonaAdmin(admin.ModelAdmin):
    inlines = [HijoInline, ]
    list_filter = ('numero_adra', "fecha_nacimiento",)
    search_fields = ("fecha_nacimiento", "numero_adra",)
    list_display = ("nombre_apellido", "numero_adra", "mensaje",)
    date_hierarchy = "fecha_nacimiento"


admin.site.register(Persona, PersonaAdmin)

admin.site.register(Hijo)
admin.site.register(Alimentos)

admin.site.register(AlmacenAlimentos)
