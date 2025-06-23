import sys
sys.path.append(r"C:\Users\zoarn\Desktop\Trading Bot")
from config import Colors
from colorama import init
import datetime

ahora = datetime.datetime.now()
hora_formateada = ahora.strftime("\033[38;5;226m%H:%M:%S\033[0m")

init()  # Habilita colores en Windows

def colorizar(texto, codigo_color=46, fondo=None):
    """
    Aplica color ANSI a un texto. Devuelve el texto coloreado (sin imprimir).
    
    Args:
        texto (str): Texto a colorear.
        codigo_color (int): Código ANSI para el color del texto (default: 46 = verde dólar).
        fondo (int, optional): Código ANSI para el color de fondo (ej: 28 = verde oscuro).
    
    Returns:
        str: Texto con códigos ANSI para color.
    """
    if fondo:
        return f"\033[48;5;{fondo}m\033[38;5;{codigo_color}m{texto}\033[0m"
    return f"\033[38;5;{codigo_color}m{texto}\033[0m"

# --- Dibujo ASCII (borde superior) ---
print(f"{Colors.SUCCESS}✅ Ganancia: +${Colors.RESET}")
dibujo_ascii = r"""/==============================================================================\
    """
dibujo_verde = colorizar(dibujo_ascii, 46)  # Verde dólar brillante

# --- Mensajes ---
mensaje_conexion = colorizar("(/^o^)/ ¡Conectado al servidor!", 117)  # Verde agua
mensaje_error = colorizar("✖ Error: No se pudo conectar.", 196)  # Rojo

# --- Imprimir resultados ---
print(dibujo_verde)
print(mensaje_conexion)
print(colorizar("=== BOT DE TRADING ===", 42))  # Verde esmeralda
print(mensaje_error)

# --- Ejemplo con fondo verde (estilo billete) ---
texto_billete = colorizar(" $ 100 USD ", 15, 28)  # Texto blanco, fondo verde oscuro

print("\033[38;5;121m[STREAM] :: (╯-_-)╰ No se pudo conectar al cliente\033[0m")
print("\033[38;5;183m[INFO] :: (-w-) zzZ\033[0m Conexión cerrada!")
print("\033[38;5;203mKaren te amo mucho <3\033[0m")
print("\033[38;5;121m=^.^= Navegador iniciado. Probando login...\033[0m")
print("\033[38;5;209m(×_×;) Error en BotSession: \033[0m")
print("\033[38;5;203m(╬ Ò - Ó) Error: \033[0m")
print("\033[38;5;183m(-w-) zzZ Cerrando navegador...\033[0m")
print("\033[38;5;84m(° v °) Sesión activa confirmada\033[0m")
print("\033[38;5;221m(#>.<) Página desconocida: \033[0m")
print("\033[38;5;229m(¬_¬) Detectada página de login. Iniciando sesión...\033[0m")
print("\033[38;5;141m(/´ v `)/* ¡Sesión iniciada con éxito!\033[0m")
print("\033[38;5;117m(/^o^)/ Bot listo para operar!\033[0m")
print("\033[38;5;40m(•̀_•́ )Proceso completado\033[0m")
print("\n" + texto_billete)
print("\033[38;5;203m[ERROR] :: (╯°□°)╯ ┻━┻ Credenciales faltantes en .env\033[0m")

# ========== ÉXITOS (Verde/Azul pastel) ========== #
print("\033[38;5;121m(˘ω˘ς) \033[0m Navegador iniciado. Probando login...")
print("\033[38;5;117m(ᵔᴥᵔ) \033[0m Bot listo para operar!")

# ========== ERRORES (Rojos/Naranjas pastel) ========== #
import sys

e = Exception("Mensaje de error simulado")  # Solo para ejemplo
print(f"\033[38;5;203m(╬ Ò~Ó) \033[0m Error: {e}", file=sys.stderr)
print("\033[38;5;221m(#> <) \033[0m Página desconocida:", file=sys.stderr)
print(f"\033[38;5;208m [STREAM] :: (:b) Esperando velas...\033[0m [{hora_formateada}]")

