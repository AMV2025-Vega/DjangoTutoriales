from django.urls import path
from .api.views import CompraAPIView
from .views import CompraRapidaView

urlpatterns = [
    # Endpoint de la API REST (DRF) - Quitamos el prefijo repetido
    path('comprar/', CompraAPIView.as_view(), name='api_comprar'),
    
    # Vista clásica basada en clases (HTML)
    path('compra-rapida/<int:libro_id>/', CompraRapidaView.as_view(), name='compra_rapida'),
    path('api/v1/productos/', listar_productos),
]