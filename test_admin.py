"""
Script de prueba para validar la funcionalidad administrativa.
"""

from src.models.administrador import Administrador
from src.models.salon_fama import SalonFama
from src.models.registro import Registro
import os


def test_autenticacion():
    """Prueba la autenticación del administrador."""
    print("\n=== TEST: Autenticación ===")
    admin = Administrador("admin123")

    # Probar autenticación correcta
    assert admin.autenticar("admin123") == True, "❌ Autenticación correcta falló"
    print("✓ Autenticación correcta funciona")

    # Probar autenticación incorrecta
    assert (
        admin.autenticar("clave_incorrecta") == False
    ), "❌ Autenticación incorrecta falló"
    print("✓ Autenticación incorrecta funciona")


def test_carga_laberinto():
    """Prueba la carga de un laberinto."""
    print("\n=== TEST: Carga de Laberinto ===")
    admin = Administrador("admin123")

    # Ruta al archivo de ejemplo
    ruta = os.path.join(
        os.path.dirname(__file__), "src", "data", "laberintos", "laberinto_ejemplo.json"
    )

    # Cargar laberinto
    laberinto, mensaje = admin.cargar_laberinto(ruta)

    if laberinto:
        print(f"✓ {mensaje}")
        print(f"  - Nombre: {laberinto.nombre}")
        print(f"  - Dificultad: {laberinto.dificultad}")
        print(
            f"  - Dimensiones: {len(laberinto.laberinto[0])}x{len(laberinto.laberinto)}"
        )
        print(f"  - Inicio jugador: {laberinto.jugador_inicio}")
        print(f"  - Inicio computadora: {laberinto.computadora_inicio}")
    else:
        print(f"❌ Error: {mensaje}")


def test_validacion_estructura():
    """Prueba la validación de estructura del laberinto."""
    print("\n=== TEST: Validación de Estructura ===")
    admin = Administrador("admin123")

    # Crear un archivo temporal con estructura inválida (sin posición del jugador)
    import tempfile
    import json

    datos_invalidos = {
        "nombre": "Laberinto Inválido",
        "mapa": [[1, 0, 1], [0, 0, 0], [1, 0, 1]],
        "inicio_computadora": {"col": 1, "fila": 1},
        # Falta inicio_jugador
    }

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(datos_invalidos, f)
        temp_path = f.name

    try:
        laberinto, mensaje = admin.cargar_laberinto(temp_path)
        if not laberinto:
            print(f"✓ Validación detectó error: {mensaje}")
        else:
            print("❌ No se detectó la estructura inválida")
    finally:
        os.unlink(temp_path)


def test_reiniciar_salon_fama():
    """Prueba el reinicio del salón de la fama."""
    print("\n=== TEST: Reiniciar Salón de Fama ===")
    admin = Administrador("admin123")

    # Crear un salón temporal con datos de prueba
    import tempfile

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        temp_path = f.name

    try:
        salon = SalonFama(temp_path)

        # Agregar algunos registros
        salon.guardar_puntaje(Registro("Jugador1", 100, "Laberinto1"))
        salon.guardar_puntaje(Registro("Jugador2", 200, "Laberinto2"))

        print(f"  - Registros antes de reiniciar: {len(salon.mostrar_mejores())}")

        # Reiniciar
        mensaje = admin.reiniciar_salon_fama(salon)
        print(f"✓ {mensaje}")

        # Verificar que esté vacío
        registros_despues = salon.mostrar_mejores()
        assert len(registros_despues) == 0, "❌ El salón no se vació correctamente"
        print(f"  - Registros después de reiniciar: {len(registros_despues)}")

    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)


if __name__ == "__main__":
    print("=" * 50)
    print("PRUEBAS DE FUNCIONALIDAD ADMINISTRATIVA")
    print("=" * 50)

    try:
        test_autenticacion()
        test_carga_laberinto()
        test_validacion_estructura()
        test_reiniciar_salon_fama()

        print("\n" + "=" * 50)
        print("✅ TODAS LAS PRUEBAS PASARON EXITOSAMENTE")
        print("=" * 50)
    except Exception as e:
        print(f"\n❌ ERROR EN PRUEBAS: {e}")
        import traceback

        traceback.print_exc()
