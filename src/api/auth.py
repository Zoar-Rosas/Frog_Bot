import asyncio
import os
from dotenv import load_dotenv
from quotexapi.stable_api import Quotex

import sys
sys.path.append(r"C:\Users\zoarn\Desktop\Trading Bot")
from config import Colors

load_dotenv()

class InicioSesionQuotexOTC:
    def __init__(self):
        self.email = os.getenv("QUOTEX_EMAIL", "").strip()
        self.password = os.getenv("QUOTEX_PASSWORD", "").strip()
        if not all([self.email, self.password]):
            raise ValueError(f"{Colors.ERROR}(#>.<) Credenciales faltantes en .env\033[0m")
        self.cliente = None

    async def iniciar_sesion(self, timeout=60):
        """Intenta conectar y retorna el cliente autenticado o None."""
        try:
            self.cliente = Quotex(email=self.email, password=self.password, lang = "es")
            check_connect, mensaje = await asyncio.wait_for(
                self.cliente.connect(),
                timeout=timeout
            )
            if check_connect:
                print("\033[38;5;129m[SESSION] :: (/^o^)/ Sesión iniciada!\033[0m\n")
                return self.cliente
            print(f"\033[38;5;196m[ERROR] :: (ﾉಥ益ಥ)ﾉ 彡┻━┻ {mensaje}\033[0m")
            return None
        except asyncio.TimeoutError:
            print("\033[38;5;196m[TIMEOUT]:: (╯°□°)╯ ┻━┻ Conexión agotada\033[0m")
            return None

async def main():
    """Punto de entrada para auth.py. Retorna el cliente o None."""
    try:
        inicio = InicioSesionQuotexOTC()
        return await inicio.iniciar_sesion()
    except Exception as e:
        print(f"\033[38;5;196m[ERROR] (ﾉಥ益ಥ)ﾉ 彡┻━┻ :: {str(e)}\033[0m")
        return None

if __name__ == "__main__":
    asyncio.run(main())