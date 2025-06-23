from typing import Final
import datetime
from datetime import datetime
from colorama import init

init()

class Colors:
    """Códigos ANSI para colores pastel."""
    ERROR: Final[str] = "\033[38;5;196m[ERROR] :: "
    BALANCE: Final [str] = "\033[38;5;226m[BALANCE] :: "
    SUCCESS: Final[str] = "\033[38;5;46m[STREAM] :: "
    INFO: Final[str] = "\033[38;5;220m[INFO] :: "
    CIERRE: Final [str] = "\033[38;5;117m[INFO] :: "
    STREAM: Final [str] = "\033[38;5;178m[STREAM] :: "
    ABIERTO: Final [str] = "\033[38;5;121m[STREAM] :: "
    INPUT: Final [str] = "\033[38;5;221m[INPUT] :: "
    CYAN :Final [str] = "\033[38;5;117m"
    OPERACION: Final[str] = "\033[38;5;159m"  # Cyan claro
    GANANCIA: Final[str] = "\033[38;5;46m"    # Verde brillante
    PERDIDA: Final[str] = "\033[38;5;196m"    # Rojo
    INFOS: Final[str] = "\033[38;5;220m"       # Amarillo
    RESET: Final [str] = "\033[0m"
    VERDE: Final [str] = "\033[38;5;76m"
    AMARILLO: Final [str] = "\033[38;5;226m"
    PASTEL_CYAN = "\033[38;5;159m"
    PASTEL_PINK = "\033[38;5;218m"
    PASTEL_GREEN = "\033[38;5;157m"
    PASTEL_ORANGE = "\033[38;5;223m"
    PASTEL_WHITE = "\033[38;5;255m"
    PASTEL_YELLOW = "\033[38;5;191m"
    PASTEL_RED= "\033[38;5;210m"

    pass

class Settings:
    """Configuraciones globales."""
    COOLDOWN: Final[int] = 80  # Segundos
    DURACION_ORDEN: Final[int] = 61          # Segundos
    MAX_VELAS: Final[int] = 110               # Tamaño del deque en streams.py

class Horas:
    """Clase para manejo de horas con colores (actualizada en tiempo real)."""
    
    @staticmethod
    def amarilla() -> str:
        """Hora actual en formato amarillo (se actualiza al llamarla)."""
        return datetime.now().strftime("\033[38;5;226m%H:%M:%S")
    
    @staticmethod
    def roja() -> str:
        """Hora actual en formato amarillo (se actualiza al llamarla)."""
        return datetime.now().strftime("\033[38;5;203m%H:%M:%S")
    
    @classmethod
    def cyan(cls) -> str:
        """Hora actual en formato cyan (alternativa con classmethod)."""
        return datetime.now().strftime("\033[38;5;159m%H:%M:%S")
    pass

# Uso CORRECTO:
#print(Horas.amarilla())  # Output: \x1b[38;5;226m17:20:45\x1b[0m (pero se ve amarillo en terminal)
#print(Horas.cyan())
#print(f"{Colors.PASTEL_PINK}(╬ Ò - Ó) No se pudo autenticar. Saliendo...{Colors.RESET}")
#print(f"{Colors.STREAM}(╯-_-)╰ No se pudo conectar al cliente\033[0m")
#print("\033[38;5;46m[STREAM] :: (╯-_-)╰ No se pudo conectar al cliente\033[0m")