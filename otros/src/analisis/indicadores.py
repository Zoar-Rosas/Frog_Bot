# src/analisis/indicadores.py
from collections import deque
import numpy as np
import talib
import sys
import time
sys.path.append(r"C:\Users\zoarn\Desktop\Trading Bot")
from config import Colors, Settings

class AnalizadorTecnico:
    def __init__(self, periodo: int):
        self.velas = deque(maxlen=Settings.MAX_VELAS)
        self.ema_fast = None
        self.ema_slow = None
        self.rsi = None
        self.precio_actual = None
        self.senal_activa = 0  # 0: sin señal, 1: Call, 2: Put
        self.tiempo_senal = 0
        self.periodo = periodo
        self.EMA_FAST_PERIOD = 8
        self.EMA_SLOW_PERIOD = 20
        self.RSI_PERIOD = 14
        self.RSI_OVERBOUGHT = 70
        self.RSI_OVERSOLD = 30
        self.SENAL_DURACION = 5
        self.ultimo_vela_timestamp = None
        self.nueva_vela_disponible = 0  # Variable de estado compartida

    def actualizar_velas(self, nueva_vela: dict):
        """Actualiza velas y calcula indicadores solo si hay suficientes velas"""
        vela_time = nueva_vela.get('time', time.time())

        # Ignorar vela si tiene el mismo timestamp que la última procesada
        if vela_time == self.ultimo_vela_timestamp:
            #print(f"[DEBUG] Vela ignorada: timestamp {vela_time} ya procesado")
            return

        # Actualizar el timestamp y añadir la vela
        self.ultimo_vela_timestamp = vela_time
        self.velas.append(nueva_vela)
        self.precio_actual = nueva_vela['close']
        #print(f"[DEBUG] Indicadores: Vela añadida, deque_size={len(self.velas)}, nueva_vela_disponible={self.nueva_vela_disponible}")

        # Procesar indicadores solo si tenemos Settings.MAX_VELAS y nueva vela disponible
        if self.nueva_vela_disponible == 1 and len(self.velas) >= Settings.MAX_VELAS:
            self._calcular_indicadores()
            #self._imprimir_indicadores()
            self.nueva_vela_disponible = 0  # Resetear después de procesar
            #print(f"[DEBUG] Indicadores: Indicadores calculados, nueva_vela_disponible={self.nueva_vela_disponible}")
        else:
            self.nueva_vela_disponible = 0  # Resetear para permitir más velas
            #print(f"[DEBUG] Indicadores: No hay suficientes velas ({len(self.velas)}/{Settings.MAX_VELAS}), nueva_vela_disponible={self.nueva_vela_disponible}")

    def _calcular_indicadores(self):
        closes = np.array([v['close'] for v in self.velas], dtype=float)
        self.ema_fast = talib.EMA(closes, timeperiod=self.EMA_FAST_PERIOD)[-1]
        self.ema_slow = talib.EMA(closes, timeperiod=self.EMA_SLOW_PERIOD)[-1]
        self.rsi = talib.RSI(closes, timeperiod=self.RSI_PERIOD)[-1]

    #fdef _imprimir_indicadores(self):
        #print(f"{Colors.PASTEL_CYAN}Indicadores actualizados:{Colors.RESET}")
        #print(f"Precio actual: {self.precio_actual:.5f}")
        #print(f"EMA {self.EMA_FAST_PERIOD}: {self.ema_fast:.5f}")
        #print(f"EMA {self.EMA_SLOW_PERIOD}: {self.ema_slow:.5f}")
        #print(f"RSI: {self.rsi:.2f}")
        #print("-" * 40)

    def _analizar_velas(self):
        if len(self.velas) < self.EMA_SLOW_PERIOD + 1 or any(v is None for v in [self.ema_fast, self.ema_slow, self.rsi]):
            return None, None

        closes = np.array([v['close'] for v in self.velas], dtype=float)
        ema_fast_series = talib.EMA(closes, timeperiod=self.EMA_FAST_PERIOD)
        ema_slow_series = talib.EMA(closes, timeperiod=self.EMA_SLOW_PERIOD)

        cond_call = (
            ema_fast_series[-1] > ema_slow_series[-1] and
            ema_fast_series[-2] <= ema_slow_series[-2] and
            self.rsi > self.RSI_OVERSOLD
        )

        cond_put = (
            ema_fast_series[-1] < ema_slow_series[-1] and
            ema_fast_series[-2] >= ema_slow_series[-2] and
            self.rsi < self.RSI_OVERBOUGHT
        )

        return cond_call, cond_put

    def detectar_senal(self) -> int:
        current_time = time.time()
        if self.senal_activa != 0 and (current_time - self.tiempo_senal) > self.SENAL_DURACION:
            self.senal_activa = 0

        if self.senal_activa == 0 and len(self.velas) >= Settings.MAX_VELAS:
            call, put = self._analizar_velas()
            if call:
                self.senal_activa = 1
                self.tiempo_senal = current_time
                print(f"{Colors.PASTEL_GREEN}Señal CALL detectada{Colors.RESET}")
            elif put:
                self.senal_activa = 2
                self.tiempo_senal = current_time
                print(f"{Colors.PASTEL_RED}Señal PUT detectada{Colors.RESET}")

        return self.senal_activa