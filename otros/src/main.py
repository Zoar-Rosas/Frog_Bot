# src/main.py
import asyncio
from api import auth
from analisis.indicadores import AnalizadorTecnico
from ordenes.ejecutor import EjecutorOrdenes
from api.streams import RealTimeCandlesOTC
import arte_ascii
import signal
import sys
sys.path.append(r"C:\Users\zoarn\Desktop\Trading Bot")
from config import Colors

async def main_app():
    arte_ascii.mostrar_presentacion()

    try:
        # 1. Autenticación
        cliente = await auth.main()
        if not cliente:
            print(f"{Colors.ERROR}No se pudo autenticar\033[0m")
            return

        # 2. Inicializar componentes
        analizador = AnalizadorTecnico()
        ejecutor = EjecutorOrdenes(cliente)
        stream = RealTimeCandlesOTC(cliente, analizador, ejecutor)

        # Manejar Ctrl+C
        def handle_interrupt(sig, frame):
            print(f"\n{Colors.INFO}Deteniendo bot...\033[0m")
            raise KeyboardInterrupt

        signal.signal(signal.SIGINT, handle_interrupt)

        # 3. Iniciar flujo principal
        await stream.iniciar_stream_velas()

    except KeyboardInterrupt:
        print(f"{Colors.INFO}Bot detenido manualmente\033[0m")
    except Exception as e:
        print(f"{Colors.ERROR}Error fatal: {str(e)}\033[0m")
    finally:
        if 'stream' in locals():
            await stream.detener_stream_velas()
        if 'cliente' in locals():
            await cliente.close()
        print(f"{Colors.CIERRE}Programa finalizado\033[0m")

if __name__ == "__main__":
    asyncio.run(main_app())