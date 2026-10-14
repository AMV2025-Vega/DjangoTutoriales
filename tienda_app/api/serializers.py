from rest_framework import serializers
from tienda_app.models import Libro


class LibroSerializer(serializers.ModelSerializer):
    """Serializer para exponer la información de los libros y su stock actual."""
    stock_actual = serializers.SerializerMethodField()

    class Meta:
        model = Libro
        fields = ['id', 'titulo', 'precio', 'stock_actual']

    def get_stock_actual(self, obj):
        inventario = getattr(obj, 'inventario', None)
        return inventario.cantidad if inventario else 0


class OrdenInputSerializer(serializers.Serializer):
    """DTO (Data Transfer Object) para validar los datos de entrada al comprar por API."""
    libro_id = serializers.IntegerField()
    direccion_envio = serializers.CharField(max_length=200)
    cantidad = serializers.IntegerField(min_value=1, default=1)