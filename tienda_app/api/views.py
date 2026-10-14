from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
###
from django.http import JsonResponse

def listar_productos(request):
    return JsonResponse({
        "productos": [
            {"id": 1, "nombre": "Producto Base Monolito", "precio": 100.0}
        ]
    }, safe=False)
###

from tienda_app.infra.factories import PaymentFactory
from tienda_app.services import CompraService

from .serializers import OrdenInputSerializer


class CompraAPIView(APIView):
    """Endpoint REST para procesar compras utilizando la capa de servicio existente."""

    def post(self, request):
        # 1. Validación de los datos de entrada (Patrón Adapter / DTO)
        serializer = OrdenInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        datos = serializer.validated_data

        try:
            # 2. Inyección de dependencias mediante la Fábrica (Factory Method)
            gateway = PaymentFactory.get_processor()

            # 3. Ejecución de la lógica de negocio reutilizando la Capa de Servicio
            servicio = CompraService(procesador_pago=gateway)
            resultado = servicio.ejecutar_compra(
                libro_id=datos['libro_id'],
                cantidad=datos['cantidad'],
                direccion=datos['direccion_envio'],
                usuario=request.user if request.user.is_authenticated else None,
            )

            return Response(
                {
                    "estado": "éxito",
                    "mensaje": f"Orden creada correctamente. Total pagado: ${resultado}",
                },
                status=status.HTTP_201_CREATED,
            )

        except ValueError as e:
            # Errores de lógica de negocio (ej. falta de stock)
            return Response({"error": str(e)}, status=status.HTTP_409_CONFLICT)
        except Exception as e:
            # Errores inesperados de infraestructura o servidor
            return Response({"error": "Error interno del servidor"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)