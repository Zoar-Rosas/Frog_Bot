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
        self.velas = deque(maxlen=Settings.MAX_VELAS)  # Ajustado a 100
        self.velas_5min = deque(maxlen=21)  # Almacena velas de 5 minutos construidas
        self.ema_8_1min = None
        self.ema_20_1min = None
        self.ema_8_5min = None
        self.ema_20_5min = None
        self.adx = None
        self.zigzag_points = []  # Para niveles clave
        self.last_zigzag_dir = None
        self.precio_actual = None
        self.senal_activa = 0  # 0: sin señal, 1: Call, 2: Put
        self.tiempo_senal = 0
        self.periodo = periodo
        self.SENAL_DURACION = 5
        self.ultimo_vela_timestamp = None
        self.nueva_vela_disponible = 0
        self.contador_5min = 0  # Para agrupar 5 velas de 1 min

    def actualizar_velas(self, nueva_vela: dict):
        """Actualiza velas y construye velas de 5 minutos"""
        vela_time = nueva_vela.get('time', time.time())

        if vela_time == self.ultimo_vela_timestamp:
            return

        self.ultimo_vela_timestamp = vela_time
        self.velas.append(nueva_vela)
        self.precio_actual = nueva_vela['close']
        self.contador_5min += 1

        # Construir vela de 5 minutos cada 5 velas
        if self.contador_5min == 5:
            self._construir_vela_5min()
            self.contador_5min = 0

        if len(self.velas) >= 20 and len(self.velas_5min) >= 8:  # Mínimo para EMAs y ADX
            try:
                self._calcular_indicadores()
                self._imprimir_indicadores()
                self.nueva_vela_disponible = 0
            except Exception as e:
                print(f"[ERROR] Error al calcular indicadores: {e}")
        else:
            self.nueva_vela_disponible = 0
            print(f"[DEBUG] Esperando datos: Velas 1min={len(self.velas)}, Velas 5min={len(self.velas_5min)}")

    def _construir_vela_5min(self):
        """Construye una vela de 5 minutos a partir de 5 velas de 1 minuto"""
        if len(self.velas) < 5:
            return
        velas_grupo = list(self.velas)[-5:]
        vela_5min = {
            'open': velas_grupo[0]['open'],
            'close': velas_grupo[-1]['close'],
            'high': max(v['high'] for v in velas_grupo),
            'low': min(v['low'] for v in velas_grupo),
            'time': velas_grupo[-1]['time']
        }
        self.velas_5min.append(vela_5min)

    def _calcular_indicadores(self):
        """Calcula EMAs, ADX y niveles clave"""
        # Datos de 1 minuto
        closes_1min = np.array([v['close'] for v in self.velas], dtype=float)
        highs_1min = np.array([v['high'] for v in self.velas], dtype=float)
        lows_1min = np.array([v['low'] for v in self.velas], dtype=float)
        self.ema_8_1min = talib.EMA(closes_1min, timeperiod=8)[-1]
        self.ema_20_1min = talib.EMA(closes_1min, timeperiod=20)[-1]
        self.adx = talib.ADX(highs_1min, lows_1min, closes_1min, timeperiod=14)[-1]

        # Datos de 5 minutos
        closes_5min = np.array([v['close'] for v in self.velas_5min], dtype=float)
        self.ema_8_5min = talib.EMA(closes_5min, timeperiod=8)[-1] if len(closes_5min) >= 8 else None
        self.ema_20_5min = talib.EMA(closes_5min, timeperiod=20)[-1] if len(closes_5min) >= 20 else None

        # Niveles clave con ZigZag
        self._calcular_zigzag(closes_1min)

    def _calcular_zigzag(self, closes):
        """Calcula niveles clave con ZigZag"""
        if len(closes) < 3:
            return
        last_price = closes[-1]
        if not self.zigzag_points:
            self.zigzag_points.append((len(self.velas) - 1, last_price))
            self.last_zigzag_dir = 0
            return
        last_zigzag = self.zigzag_points[-1]
        change_percent = abs(last_price - last_zigzag[1]) / last_zigzag[1]
        if change_percent >= 0.001:
            if len(self.zigzag_points) >= 2:
                anteultimo_zigzag = self.zigzag_points[-2]
                if last_zigzag[1] > anteultimo_zigzag[1] and last_price < last_zigzag[1]:
                    self.zigzag_points[-1] = (last_zigzag[0], last_zigzag[1])
                    self.last_zigzag_dir = 1
                elif last_zigzag[1] < anteultimo_zigzag[1] and last_price > last_zigzag[1]:
                    self.zigzag_points[-1] = (last_zigzag[0], last_zigzag[1])
                    self.last_zigzag_dir = -1
            if last_price > last_zigzag[1] and (self.last_zigzag_dir is None or self.last_zigzag_dir <= 0):
                self.zigzag_points.append((len(self.velas) - 1, last_price))
                self.last_zigzag_dir = 1
            elif last_price < last_zigzag[1] and (self.last_zigzag_dir is None or self.last_zigzag_dir >= 0):
                self.zigzag_points.append((len(self.velas) - 1, last_price))
                self.last_zigzag_dir = -1

    def _imprimir_indicadores(self):
        print(f"{Colors.PASTEL_CYAN}Indicadores actualizados:{Colors.RESET}")
        print(f"Precio actual: {self.precio_actual:.5f}")
        print(f"EMA 8 (1min): {self.ema_8_1min:.5f}")
        print(f"EMA 20 (1min): {self.ema_20_1min:.5f}")
        ema_8_5min_str = f"{self.ema_8_5min:.5f}" if self.ema_8_5min is not None else "N/A"
        ema_20_5min_str = f"{self.ema_20_5min:.5f}" if self.ema_20_5min is not None else "N/A"
        print(f"EMA 8 (5min): {ema_8_5min_str}")
        print(f"EMA 20 (5min): {ema_20_5min_str}")
        print(f"ADX: {self.adx:.2f}")
        print(f"Último ZigZag: {self.zigzag_points[-1] if self.zigzag_points else 'Ninguno'}, Dirección: {self.last_zigzag_dir}")
        print("-" * 40)

    def detectar_senal(self) -> int:
        """Detecta señales de trading basadas en EMAs, ADX y niveles clave"""
        current_time = time.time()
        if self.senal_activa != 0 and (current_time - self.tiempo_senal) > self.SENAL_DURACION:
            self.senal_activa = 0

        if self.senal_activa == 0 and len(self.velas) >= 20 and len(self.velas_5min) >= 8 and all(v is not None for v in [self.ema_8_1min, self.ema_20_1min, self.ema_8_5min, self.ema_20_5min, self.adx]):
            ultima_vela = list(self.velas)[-1]
            penultima_vela = list(self.velas)[-2]
            distancia_pips = abs(ultima_vela['close'] - self.ema_8_1min) * 10000  # Convertir a pips (4 decimales)

            # Condiciones para señal
            cruce_alcista = self.ema_8_1min > self.ema_20_1min and penultima_vela['close'] <= penultima_vela['open'] and ultima_vela['close'] > ultima_vela['open']
            cruce_bajista = self.ema_8_1min < self.ema_20_1min and penultima_vela['close'] >= penultima_vela['open'] and ultima_vela['close'] < ultima_vela['open']
            tendencia_alcista_5min = self.ema_8_5min > self.ema_20_5min
            tendencia_bajista_5min = self.ema_8_5min < self.ema_20_5min
            adx_suficiente = self.adx >= 15
            lejos_ema = distancia_pips >= 5  # Umbral de 5 pips
            cerca_nivel = any(abs(ultima_vela['close'] - zp[1]) * 10000 < 5 for zp in self.zigzag_points)  # Menos de 5 pips de nivel clave

            if (cruce_alcista and lejos_ema and adx_suficiente and tendencia_alcista_5min and not cerca_nivel):
                self.senal_activa = 1
                self.tiempo_senal = current_time
                print(f"{Colors.PASTEL_GREEN}Señal CALL detectada{Colors.RESET}")
            elif (cruce_bajista and lejos_ema and adx_suficiente and tendencia_bajista_5min and not cerca_nivel):
                self.senal_activa = 2
                self.tiempo_senal = current_time
                print(f"{Colors.PASTEL_RED}Señal PUT detectada{Colors.RESET}")

        return self.senal_activa