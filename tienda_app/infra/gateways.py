import datetime
from ..domain.interfaces import ProcesadorPago

class BancoNacionalProcesador(ProcesadorPago):
    """
    Implementación concreta de la infraestructura.
    Simula un banco local escribiendo en un log.
    """
    def pagar(self, monto: float) -> bool:
        # Nombre de archivo personalizado para evidencia de auditoría
        archivo_log = "pagos_locales_ALEJANDRO_MARTINEZ.log"
        with open(archivo_log, "a") as f:
            f.write(f"[{datetime.datetime.now()}] BANCO NACIONAL - Cobro procesado: ${monto}\n")
        return True