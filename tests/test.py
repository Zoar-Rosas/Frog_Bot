import asyncio
from quotexapi.stable_api import Quotex

async def ejecutar_orden():
    email = "zoar.nava09@gmail.com"
    password = "pandalococo"

    cliente = None  # Inicializamos cliente fuera del bloque try

    try:
        cliente = Quotex(email=email, password=password, lang="es")
        conectado, mensaje = await cliente.connect()
        if not conectado:
            print(f"Error al conectar: {mensaje}")
            return

        cliente.change_account("PRACTICE")
        print("Cambiado a cuenta real.")

        # Obtener y mostrar la lista de todos los activos disponibles
        assets = cliente.get_all_asset_name()
        print("\nActivos disponibles:")
        for asset in assets:
            print(f"- {asset}")

        # Solicitar al usuario los parámetros de la operación
        asset = input("\nIngresa el asset que deseas usar (ej: EURUSD_otc): ")
        try:
            amount = float(input("Ingresa el monto a invertir: "))
        except ValueError:
            print("El monto ingresado no es válido. Debe ser un número.")
            return
        try:
            duration = int(input("Ingresa la duración de la operación en segundos: "))
        except ValueError:
            print("La duración ingresada no es válida. Debe ser un número entero.")
            return
        direction = input("Ingresa la dirección de la operación (call/put): ").lower()
        if direction not in ["call", "put"]:
            print("La dirección ingresada no es válida. Debe ser 'call' o 'put'.")
            return

        asset_nombre, asset_info = await cliente.get_available_asset(asset, force_open=True)
        if not (asset_info and asset_info[2]):
            print(f"El activo {asset} no está disponible o el mercado está cerrado.")
            return

        status, orden_info = await cliente.buy(amount, asset_nombre, direction, duration)
        if status:
            print(f"Orden de {direction.upper()} ejecutada. ID: {orden_info['id']}")
        else:
            print(f"Error al ejecutar orden de {direction.upper()}.")

    except Exception as e:
        print(f"Ocurrió un error: {e}")
    finally:
        if cliente:
            await cliente.close()
            print("Conexión cerrada.")

if __name__ == "__main__":
    asyncio.run(ejecutar_orden())