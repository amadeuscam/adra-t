from django.urls import path, include
from .views import (
    PersonaDetailView,
    PersonaCreateView,
    PersonaUpdateView, PersonaDeleteView,
    PersonaAlimentosDeleteView,
    AlmacenListView,
    HijoUpdateView,
    HijoDeleteView,
    PersonaListView,
    PersonaAlimentosUpdateView,
    statistics_persona,
    export_users_csv

)
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as vs

app_name = 'adra'
# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'personas', views.PersonaViewSet)
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('api/', include((router.urls, 'api'), namespace='api')),
    path('api-token-auth/', vs.obtain_auth_token, name="api-token-auth"),
    # API
    # path('api/', views.api_root),
    # path('api/persona/', persona_list, name="persona-list"),
    # path('api/persona/<int:pk>/', persona_detail, name='persona-api-detail'),
    # path('api/users/', user_list, name='user-list'),
    # path('api/users/<int:pk>/', user_detail),

    # personas url
    path('', PersonaListView.as_view(), name="persona-home"),
    path('persona/<int:pk>/', PersonaDetailView.as_view(), name="personas_detail"),
    path('persona/new/', PersonaCreateView.as_view(), name="persona-create"),
    path('persona/<int:pk>/update/', PersonaUpdateView.as_view(),
         name="persona-update"),
    path('persona/<int:pk>/delete/', PersonaDeleteView.as_view(),
         name="persona-delete"),
    # end persona url

    # almacen url
    path('almacen/', AlmacenListView.as_view(), name="almacen-home"),
    # end almacen url

    # statistics
    path('statistics/', views.statistics_persona, name="statistics-personas"),
    path('export/csv/', views.export_users_csv, name='exportar-users-csv'),
    path('export/pdf/<int:pk>', views.generar_hoja_entrega, name='pdf_form'),
    # end statistics

    # buscar url
    path('buscar/', views.buscar, name="buscar"),
    path('buscar_por_fecha/', views.buscar_fecha, name='buscar-por-fecha'),
    # end bucar url

    # alimentos url
    path('persona/<int:pk>/alimentos', views.adauga_alimentos_persona,
         name="alimentos-create"),
    path('persona/alimentos/<int:pk>/update',
         PersonaAlimentosUpdateView.as_view(), name='persona-update-alimentos'),

    path('persona/alimentos/<int:pk>/delete',
         PersonaAlimentosDeleteView.as_view(), name='persona-alimentos-delete'),
    # end alimentos url

    # hijos url
    path('persona/<int:pk>/hijos', views.adauga_hijo_persona,
         name="hijo-create"),
    path('persona/hijos/<int:pk>/update', HijoUpdateView.as_view(),
         name="hijo-update"),
    path('persona/hijos/<int:pk>/delete', HijoDeleteView.as_view(),
         name="hijo-delete"),
    # end hijos url
    path('edit/', views.edit, name='edit-profile'),
    path('get-data/', views.get_data, name='get_data'),
    path('adra-anuncios/', views.anuncios, name='anuncio'),

]
urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]
