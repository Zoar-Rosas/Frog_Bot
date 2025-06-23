import asyncio
from quotexapi.stable_api import Quotex

print("Iniciando cliente Quotex...")

client = Quotex(
    email="zoar.nava09@gmail.com",
    password="pandalococo"
)

async def get_closed_candles():
    check_connect, message = await client.connect()
    if check_connect:
        asset = input("Ingresa el activo (por ejemplo, EURUSD_otc): ") or "EURUSD_otc"
        period = 5 # Duración de la vela en segundos
        asset_name, asset_data = await client.get_available_asset(asset, force_open=True)
        print(asset_name, asset_data)
        if asset_data[2]:
            print("OK: Activo abierto.")
            last_timestamp = None
            while True:
                # Obtener las velas
                candles = await client.get_candle_v2(asset_name, period)
                if candles:
                    current_candle = candles[-1]  # Última vela (más reciente)
                    current_timestamp = current_candle['time']
                    
                    # Solo imprime si el timestamp ha cambiado (vela cerrada)
                    if current_timestamp != last_timestamp:
                        last_timestamp = current_timestamp
                        end_time = current_timestamp + period
                        print(f"Vela cerrada:")
                        print(f"Inicio: {current_timestamp}, Fin: {end_time}")
                        print(f"Apertura: {current_candle['open']}, Cierre: {current_candle['close']}")
                        print(f"Máximo: {current_candle['high']}, Mínimo: {current_candle['low']}\n")
                else:
                    print("No se encontraron velas.")
                
                await asyncio.sleep(1)  # Esperar un segundo antes de verificar nuevamente
        else:
            print("ERROR: El activo está cerrando.")
    else:
        print("ERROR: No se pudo conectar al cliente.")

    print("Saliendo...")
    await client.close()

# Ejecutar el script
if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(get_closed_candles())
    except KeyboardInterrupt:
        print("Cerrando el programa.")
    finally:
        loop.close()