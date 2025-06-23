# src/api/streams.py
import asyncio
from collections import deque
import sys
sys.path.append(r"C:\Users\zoarn\Desktop\Trading Bot")
from config import Colors, Settings, Horas

class RealTimeCandlesOTC:
    def __init__(self, cliente, analizador, ejecutor):
        self.cliente = cliente
        self.analizador = analizador
        self.ejecutor = ejecutor
        self.activo = None
        self.periodo = None
        self.ultimo_timestamp = None

    async def iniciar_stream_velas(self):
        try:
            self.activo = input(f"{Colors.INPUT}Activo (ej. EURUSD_otc): \033[0m") or "EURUSD_otc"
            self.periodo = int(input(f"{Colors.INPUT}Período (segundos): \033[0m") or 60)

            from datetime import datetime, timedelta
            inicio = datetime.now()
            fin_estimado = inicio + timedelta(seconds=(Settings.MAX_VELAS * self.periodo))

            asset_name, asset_data = await self.cliente.get_available_asset(self.activo, force_open=True)
            print(f"\n{Colors.CIERRE}Activo: \033[32m{asset_name}, {Colors.CYAN}Datos: \033[0m{asset_data}")
            print(f"{Colors.PASTEL_YELLOW}[STREAM] :: Inicio [{Horas.cyan()}{Colors.PASTEL_YELLOW}] {Colors.RESET}|{Colors.PASTEL_YELLOW} Fin estimado: [{Colors.PASTEL_CYAN}{fin_estimado.strftime('%H:%M:%S')}{Colors.PASTEL_YELLOW}]\033[0m")

            mensaje_mostrado = False

            while True:
                velas = await self.cliente.get_candle_v2(self.activo, self.periodo)
                if velas:
                    ultima_vela = velas[-1]

                    if ultima_vela['time'] != self.ultimo_timestamp:
                        self.ultimo_timestamp = ultima_vela['time']
                        self.analizador.actualizar_velas(ultima_vela)

                        if not mensaje_mostrado and len(self.analizador.velas) >= 20:
                            print(f"{Colors.CYAN}[{Horas.cyan()}{Colors.CYAN}]Velas obtenidas, esperando señal....{Colors.RESET}")
                            mensaje_mostrado = True

                        senal = self.analizador.detectar_senal()
                        if senal in [1, 2]:
                            # Ejecutar orden sin esperar su finalización
                            await self.ejecutor.ejecutar_orden(self.activo, senal)

                await asyncio.sleep(0.5)

        except Exception as e:
            print(f"{Colors.ERROR}Error en stream: {str(e)}\033[0m")
            raise

    async def detener_stream_velas(self):
        """Limpieza al finalizar"""
        if self.activo:
            await self.cliente.stop_candles_stream(self.activo)
        print(f"{Colors.INFO}Stream detenido\033[0m")