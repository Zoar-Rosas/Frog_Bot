import asyncio
from collections import deque
from colorama import init
import logging

init()

class RealTimeCandlesOTC:
    def __init__(self, cliente):
        self.cliente = cliente
        self.activo = None
        self.periodo = None
        self.velas = deque()
        self.ultimo_timestamp = None

    async def iniciar_stream_velas(self):
        try:
            self.activo = input("\033[38;5;221m[INPUT] :: (°v°) Ingresa el activo (por ejemplo, EURUSD_otc): ") or "EURUSD_otc"
            self.periodo = int(input("\033[38;5;221m[INPUT] :: (°v°) Ingresa el período de la vela en segundos: ") or "60")

            asset_name, asset_data = await self.cliente.get_available_asset(self.activo, force_open=True)
            print(f"\033[38;5;184m[INFO] :: Activo: \033[32m{asset_name}, \033[38;5;184mDatos: \033[0m{asset_data}")
            if asset_data[2]:
                print("\n\033[38;5;121m[STREAM] :: (/´ V `)/ Activo abierto con éxito.\033[0m\n")
                await self._obtener_velas(asset_name, self.periodo)
            else:
                print("\033[38;5;196m[ERROR] :: (>_<) El activo está cerrado.\033[0m")
        except Exception as e:
            logging.error(f"\033[38;5;196m[ERROR] :: Error al iniciar el stream: {e}\033[0m", exc_info=True)
            raise  # Re-lanzar la excepción para que se maneje en main.py

    async def _obtener_velas(self, asset_name, period):
        try:
            while True:
                candles = await self.cliente.get_candle_v2(asset_name, period)
                if candles:
                    current_candle = candles[-1]
                    current_timestamp = current_candle['time']

                    if current_timestamp != self.ultimo_timestamp:
                        self.ultimo_timestamp = current_timestamp
                        end_time = current_timestamp + period
                        print("\033[38;5;82m[STREAM] :: + Vela:\033[0m")
                        print(f"\033[38;5;137mInicio: \033[0m{current_timestamp}, \033[38;5;137mFin: \033[0m{end_time}")
                        print(f"\033[38;5;141mApertura: \033[0m{current_candle['open']}, \033[38;5;141mCierre: \033[0m{current_candle['close']}"
                              f"\033[38;5;141m Máximo: \033[0m{current_candle['high']}, \033[38;5;141mMínimo: \033[0m{current_candle['low']}\n")
                else:
                    logging.warning("\033[38;5;117m[ ] :: (×_×;) No se encontraron velas\033[0m")  # Usar logging.warning
                await asyncio.sleep(0.1)  # Reducir el sleep
        except asyncio.CancelledError:
            logging.info("\033[38;5;220m[INFO] :: (;×_×) Obtener_velas cancelado.\033[0m")
            raise  # Re-lanzar para que gather lo maneje
        except Exception as e:
            logging.error(f"\033[38;5;196m[ERROR] :: (╬ Ò~Ó) Error en _obtener_velas: {e}\033[0m", exc_info=True)
            raise  # Re-lanzar para que gather lo maneje


    async def detener_stream_velas(self):
        try:
            if self.activo:
                self.cliente.stop_candles_stream(self.activo)
                print(f"\033[38;5;178m[STREAM] :: (҂`_´) Stream detenido\033[0m")
        except Exception as e:
            logging.error(f"\033[38;5;196m[ERROR] :: Error al detener el stream: {e}\033[0m", exc_info=True)