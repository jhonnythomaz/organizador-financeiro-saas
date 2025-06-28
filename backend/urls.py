# backend/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from api.views import GerarRelatorioPDF

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/relatorios/gerar/', GerarRelatorioPDF.as_view(), name='gerar_relatorio'),
    path('api/', include('api.urls')), # Inclui as URLs do nosso app
    # Rotas de Autenticação JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]