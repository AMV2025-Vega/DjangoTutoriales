import datetime
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import View
from .models import Libro, Inventario, Orden

# Importamos la fábrica y los servicios
from .infra.factories import PaymentFactory
from .services import CompraService, CompraRapidaService


# ==========================================
# Paso 1: FBV (Function-Based View Spaghetti)
# ==========================================
def compra_rapida_fbv(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)
    
    if request.method == 'POST':
        inventario = Inventario.objects.get(libro=libro)
        if inventario.cantidad > 0:
            total = float(libro.precio) * 1.19
            with open("pagos_manuales.log", "a") as f:
                f.write(f"[{datetime.datetime.now()}] Pago FBV: ${total}\n")
                
            inventario.cantidad -= 1
            inventario.save()
            Orden.objects.create(libro=libro, total=total)
            return HttpResponse(f"Compra exitosa: {libro.titulo}")
        else:
            return HttpResponse("Sin stock", status=400)
            
    total_estimado = float(libro.precio) * 1.19
    return render(request, 'tienda_app/compra_rapida.html', {
        'libro': libro,
        'total': total_estimado
    })


# ==========================================
# Paso 2 / Sección 4: CBV Refactorizada con Factory + Builder
# ==========================================
class CompraRapidaView(View):
    template_name = 'tienda_app/compra_rapida.html'

    def get(self, request, libro_id):
        # Usamos la fábrica para obtener el procesador configurado por ambiente
        processor = PaymentFactory.get_processor()
        servicio = CompraService(processor)
        
        detalle = servicio.obtener_detalle_producto(libro_id)
        return render(request, self.template_name, {
            'libro': detalle['libro'],
            'total': detalle['total']
        })

    def post(self, request, libro_id):
        # Delegación total de la infraestructura a la Fábrica (Factory Method)
        processor = PaymentFactory.get_processor()
        servicio = CompraService(processor)
        
        try:
            # Ejecución utilizando el servicio (que usa el OrdenBuilder internamente)
            orden_total = servicio.ejecutar_compra(libro_id=libro_id)
            return HttpResponse(f"¡Compra realizada con éxito! Total: ${orden_total}")
        except Exception as e:
            return HttpResponse(f"Error en la transacción: {str(e)}", status=400)