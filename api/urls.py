# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PagamentoViewSet, 
    CategoriaViewSet, 
    ClienteAdminViewSet, 
    get_user_profile,
    GerarRelatorioPDF
)

router = DefaultRouter()
router.register(r'pagamentos', PagamentoViewSet, basename='pagamento')
router.register(r'categorias', CategoriaViewSet, basename='categoria')
router.register(r'admin/clientes', ClienteAdminViewSet, basename='admin-cliente')

urlpatterns = [
    path('', include(router.urls)),
    path('profile/', get_user_profile, name='user_profile'),
    #path('relatorio-pdf/', GerarRelatorioPDF.as_view(), name='gerar_relatorio_pdf'),
    
]