# src/ordenes/ejecutor.py
import asyncio
from datetime import datetime
import sys
sys.path.append(r"C:\Users\zoarn\Desktop\Trading Bot")
from config import Colors, Settings, Horas

class EjecutorOrdenes:
    def __init__(self, cliente):
        self.cliente = cliente
        self.duration = Settings.DURACION_ORDEN
        self.ultima_orden = None
        self.balance_anterior = 0
        self.balance_actual = 0
        self.en_operacion = False
        self.amount = 1  # Monto fijo para demo
        
    async def calcular_monto(self, porcentaje=0.1):
        """Calcula monto como porcentaje del balance"""
        balance = await self.obtener_balance()
        return round(balance * porcentaje)  # Redondea a 2 decimales

    async def obtener_balance(self):
        """Obtiene el balance actual sin imprimir"""
        return await self.cliente.get_balance()
    
    async def _verificar_resultado(self, asset: str, direction: str):
        """Tarea separada para esperar y verificar el resultado de la orden"""
        try:
            # Espera silenciosa
            await asyncio.sleep(91)
            
            # Mostrar resultado compacto
            nuevo_balance = await self.obtener_balance()
            diferencia = nuevo_balance - self.balance_anterior
            
            color = Horas.amarilla() if diferencia > 0 else Horas.roja()
            resultado = f"{Colors.PASTEL_GREEN}Ganadora" if diferencia > 0 else f"{Colors.PASTEL_PINK}Perdedora"
            valor = f"{Colors.PASTEL_GREEN}+${diferencia:.2f}" if diferencia > 0 else f"{Colors.PASTEL_PINK}-${abs(diferencia):.2f}"
            
            print(f"{Colors.RESET}[{color}{Colors.RESET}] {resultado}: {valor}{Colors.RESET} | {Colors.PASTEL_GREEN}Balance: ${nuevo_balance:.2f}{Colors.RESET} | {Colors.VERDE}Listo...\033[0m")
            
        finally:
            self.en_operacion = False
            self.ultima_orden = datetime.now()

    async def ejecutar_orden(self, asset: str, senal: int):
        """Ejecuta la orden y delega la espera a una tarea separada"""
        if self.en_operacion:
            print(f"{Colors.INFO}Operación en curso, omitiendo nueva orden\033[0m")
            return False

        try:
            self.en_operacion = True
            
            # 1. Obtener balance inicial silenciosamente
            self.balance_anterior = await self.obtener_balance()
            self.amount = await self.calcular_monto(0.1)  # 10% del balance
            
            # 2. Determinar dirección y ejecutar
            direction = "call" if senal == 1 else "put"
            print(f"\n{Colors.PASTEL_GREEN}[{Horas.amarilla()}{Colors.PASTEL_GREEN}] Ejecutando {direction.upper()}{Colors.PASTEL_GREEN} en {Colors.PASTEL_YELLOW}{asset} {Colors.PASTEL_GREEN}(${self.amount:.2f}){Colors.RESET}")
            
            status, _ = await self.cliente.buy(self.amount, asset, direction, self.duration)
            if not status:
                self.en_operacion = False
                return False
                
            # 3. Crear tarea separada para esperar y verificar resultado
            asyncio.create_task(self._verificar_resultado(asset, direction))
            return True
            
        except Exception:
            self.en_operacion = False
            return False