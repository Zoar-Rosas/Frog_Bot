# src/api/streams.py
import asyncio
from collections import deque
import sys
sys.path.append(r"C:\Users\zoarn\Desktop\Trading Bot")
from config import Colors, Settings, Horas

class RealTimeCandlesOTC:
    def __init__(self, cliente, analizador, ejecutor, periodo: int):
        self.cliente = cliente
        self.analizador = analizador
        self.ejecutor = ejecutor
        self.activo = None
        self.periodo = periodo
        self.ultimo_timestamp = None

    async def iniciar_stream_velas(self):
        try:
            self.activo = input(f"{Colors.INPUT}Activo (ej. EURUSD_otc): \033[0m") or "EURUSD_otc"

            from datetime import datetime, timedelta
            inicio = datetime.now()
            fin_estimado = inicio + timedelta(seconds=(Settings.MAX_VELAS * self.periodo))

            asset_name, asset_data = await self.cliente.get_available_asset(self.activo, force_open=True)
            print(f"\n{Colors.CIERRE}Activo: \033[32m{asset_name}, {Colors.CYAN}Datos: \033[0m{asset_data}")
            print(f"{Colors.PASTEL_YELLOW}[STREAM] :: Inicio [{Horas.cyan()}{Colors.PASTEL_YELLOW}] {Colors.RESET}|{Colors.PASTEL_YELLOW} Fin estimado: [{Colors.PASTEL_CYAN}{fin_estimado.strftime('%H:%M:%S')}{Colors.PASTEL_YELLOW}]\033[0m")

            mensaje_mostrado = False

            while True:
                velas = await self.cliente.get_candle_v2(self.activo, self.periodo)
                #print(f"[DEBUG] Streams: Velas recibidas: {len(velas) if velas else 'Ninguna'}")
                if velas:
                    ultima_vela = velas[-1]
                    vela_timestamp = ultima_vela.get('time')

                    # Validate candle data
                    required_fields = ['open', 'high', 'low', 'close']
                    valid_candle = True
                    for field in required_fields:
                        if ultima_vela.get(field) is None or not isinstance(ultima_vela.get(field), (int, float)):
                            valid_candle = False
                            print(f"{Colors.ERROR}[DEBUG] Vela inválida: {field} es {ultima_vela.get(field)} en vela {ultima_vela}{Colors.RESET}")
                            break

                    if not valid_candle:
                        print(f"{Colors.ERROR}Omitiendo vela inválida con timestamp={vela_timestamp}{Colors.RESET}")
                        await asyncio.sleep(0.5)
                        continue

                    # Verificar si la vela es nueva
                    if vela_timestamp != self.ultimo_timestamp:
                        self.ultimo_timestamp = vela_timestamp
                        self.analizador.nueva_vela_disponible = 1  # Señalizar nueva vela
                        self.analizador.actualizar_velas(ultima_vela)
                        print(f"{Colors.CYAN}[{Horas.cyan()}] Nueva vela: timestamp={vela_timestamp}, open={ultima_vela['open']:.5f}, high={ultima_vela['high']:.5f}, low={ultima_vela['low']:.5f}, close={ultima_vela['close']:.5f}, volume={ultima_vela.get('volume', 'N/A')}{Colors.RESET}")

                        if not mensaje_mostrado and len(self.analizador.velas) == Settings.MAX_VELAS-10:
                            print(f"{Colors.CYAN}[{Horas.cyan()}{Colors.CYAN}]Velas obtenidas, esperando señal....{Colors.RESET}")
                            mensaje_mostrado = True

                        # Detectar señal después de procesar la vela
                        senal = self.analizador.detectar_senal()
                        if senal in [1, 2]:
                            await self.ejecutor.ejecutar_orden(self.activo, senal)

                # Esperar para sincronizar con las velas
                await asyncio.sleep(0.5)

        except Exception as e:
            print(f"{Colors.ERROR}Error en stream: {str(e)}\033[0m")
            raise

    async def detener_stream_velas(self):
        if self.activo:
            await self.cliente.stop_candles_stream(self.activo)
        print(f"{Colors.INFO}Stream detenido\033[0m")