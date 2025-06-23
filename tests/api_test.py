import asyncio
import os
from dotenv import load_dotenv
from quotexapi.stable_api import Quotex

# Carga las variables del archivo .env
load_dotenv()

class InicioSesionQuotexOTC:
    def __init__(self):
        """
        Inicializa la clase para iniciar sesión en Quotex OTC.
        Las credenciales se leen del archivo .env con validación de que existen
        """

        self.email = os.getenv("QUOTEX_EMAIL", "").strip()
        self.password = os.getenv("QUOTEX_PASSWORD", "").strip()
        if not all([self.email, self.password]):
            print("\033[38;5;203m[ERROR] :: (☉_☉) Credenciales no configuradas en .env\033[0m")
            raise ValueError("\033[38;5;203m[ERROR] :: (╯°□°）╯︵ ┻━┻ Credenciales faltantes en .env\033[0m")

        self.cliente = None

    async def iniciar_sesion(self, timeout=10):
        """Conexión al servidor de Quotex"""
        print("\033[38;5;121m[INFO] :: =^.^=\033[0m Iniciando sesión...")

        
        try:
            self.cliente = Quotex(email=self.email, password=self.password, lang="es")
            check_connect, mensaje = await asyncio.wait_for(
                self.cliente.connect(),
                timeout=timeout
            )

            if check_connect:
                print("\033[38;5;129m[SESSION] :: (/´ v `)/*\033[0m Sesión iniciada correctamente!")
                return True, self.cliente
            else:
                print(f"\033[38;5;196m[ERROR] :: (×_×;) Error: {mensaje}\033[0m\n")
                return False, None
                
        except:
            print("\033[38;5;196m[TIMEOUT] :: (҂`_´) Tiempo de conexión agotado.\033[0m\n")
            return False, None

    async def cerrar_sesion(self):
        """Cierra la conexión"""
        if self.cliente:
            await self.cliente.close()
            print("\033[38;5;183m[INFO] :: (-w-) zzZ\033[0m Conexión cerrada!")


async def operaciones_principales(cliente):
    """Aquí iría va la lógica de trading"""
    print("\033[38;5;57m[EXEC] :: (° v °)\033[0m Ejecutando operaciones...\n")

    # await cliente.operar()  # Tu lógica aquí

async def main():
    try:
       
        inicio_sesion = InicioSesionQuotexOTC()
        sesion_exitosa, cliente = await inicio_sesion.iniciar_sesion()

        if sesion_exitosa:
            await operaciones_principales(cliente)
            
    except Exception as e:
        print(f"\033[38;5;196m(╬ Ò - Ó) Error crítico: {str(e)}\033[0m\n")
    finally:
        await inicio_sesion.cerrar_sesion()
        print("\033[38;5;40m[INFO] :: (ᵔᴥᵔ)\033[0m Cerrando sesión...")


if __name__ == "__main__":
    asyncio.run(main())