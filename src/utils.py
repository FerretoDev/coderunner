"""
Utilidades compartidas para el juego.

Funciones helper que evitan duplicación de código:
- Manejo de rutas y archivos
- Validaciones comunes
- Helpers de configuración
"""
import json
import os


def resolver_ruta_laberinto(ruta: str) -> str:
    """
    Resuelve una ruta de laberinto, buscando en src/data/ si es relativa.

    Args:
        ruta: Ruta del archivo (absoluta o relativa)

    Returns:
        Ruta absoluta del archivo, o la ruta original si no se encuentra
    """
    if not os.path.isabs(ruta):
        # Si no existe tal cual, buscar en src/data/
        if not os.path.exists(ruta):
            ruta_data = os.path.join("src", "data", ruta)
            if os.path.exists(ruta_data):
                return ruta_data
    return ruta


def cargar_json(ruta: str) -> dict | None:
    """
    Carga un archivo JSON y retorna su contenido.

    Args:
        ruta: Ruta del archivo JSON

    Returns:
        Diccionario con el contenido o None si hay error
    """
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error al cargar JSON {ruta}: {e}")
        return None


def guardar_json(ruta: str, datos: dict, indent: int = 2) -> bool:
    """
    Guarda datos en un archivo JSON.

    Args:
        ruta: Ruta donde guardar
        datos: Datos a guardar
        indent: Indentación del JSON

    Returns:
        True si se guardó correctamente, False si hubo error
    """
    try:
        # Crear directorio si no existe
        directorio = os.path.dirname(ruta)
        if directorio:
            os.makedirs(directorio, exist_ok=True)

        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=indent, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error al guardar JSON {ruta}: {e}")
        return False


def validar_extension(ruta: str, extension: str) -> bool:
    """
    Valida que un archivo tenga la extensión correcta.

    Args:
        ruta: Ruta del archivo
        extension: Extensión esperada (con o sin punto)

    Returns:
        True si la extensión es correcta
    """
    if not extension.startswith("."):
        extension = f".{extension}"
    return os.path.splitext(ruta)[1].lower() == extension.lower()


def truncar_texto(texto: str, max_len: int) -> str:
    """
    Trunca un texto si excede el máximo de caracteres.

    Args:
        texto: Texto a truncar
        max_len: Longitud máxima

    Returns:
        Texto truncado con "..." si es necesario
    """
    if len(texto) <= max_len:
        return texto
    return texto[: max_len - 3] + "..."


def obtener_nombre_archivo(ruta: str) -> str:
    """
    Obtiene el nombre de archivo sin la ruta.

    Args:
        ruta: Ruta completa del archivo

    Returns:
        Nombre del archivo con extensión
    """
    return os.path.basename(ruta)


def obtener_nombre_sin_extension(ruta: str) -> str:
    """
    Obtiene el nombre de archivo sin extensión.

    Args:
        ruta: Ruta completa del archivo

    Returns:
        Nombre del archivo sin extensión
    """
    return os.path.splitext(os.path.basename(ruta))[0]
