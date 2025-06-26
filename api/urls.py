# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PagamentoViewSet, CategoriaViewSet

router = DefaultRouter()
router.register(r'pagamentos', PagamentoViewSet, basename='pagamento')
router.register(r'categorias', CategoriaViewSet, basename='categoria')

urlpatterns = [
    path('', include(router.urls)),
]