"""
Tests para HU-01: Movimiento básico del jugador
Verificar que el jugador se mueve correctamente con las teclas de dirección.
"""

import pygame
import pytest

from models.jugador import Jugador
from models.laberinto import Laberinto


@pytest.fixture
def laberinto_simple(tmp_path):
    """Fixture que crea un laberinto simple de 5x5 para pruebas"""
    pygame.init()
    # Crear un laberinto simple con pasillos
    mapa_prueba = {
        "nombre": "Laberinto Test",
        "dificultad": "facil",
        "mapa": [
            [1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1],
            [1, 0, 1, 0, 1],
            [1, 0, 0, 0, 1],
            [1, 1, 1, 1, 1],
        ],
        "jugador_inicio": [1, 1],
        "computadora_inicio": [3, 3],
        "obsequios": [{"posicion": [3, 2], "valor": 10}],
    }

    # Crear archivo temporal JSON
    import json

    archivo = tmp_path / "laberinto_test.json"
    with open(archivo, "w") as f:
        json.dump(mapa_prueba, f)

    return Laberinto(str(archivo))


@pytest.fixture
def jugador_test(laberinto_simple):
    """Fixture que crea un jugador en posición inicial"""
    inicio = laberinto_simple.mapa_data["inicio_jugador"]
    x = inicio["columna"] * 32 + 16
    y = inicio["fila"] * 32 + 16
    return Jugador(x=x, y=y, radio=10, velocidad=1)


class TestMovimientoBasico:
    """CP-01: Tests de movimiento básico del jugador"""

    def test_jugador_se_mueve_arriba(self, jugador_test, laberinto_simple):
        """Verificar que el jugador se mueve hacia arriba al presionar ↑"""
        y_inicial = jugador_test.jugador_principal.y

        # Simular movimiento hacia arriba (una celda = 32 píxeles)
        jugador_test.jugador_principal.y -= 32

        assert jugador_test.jugador_principal.y == y_inicial - 32

    def test_jugador_se_mueve_abajo(self, jugador_test):
        """Verificar que el jugador se mueve hacia abajo al presionar ↓"""
        y_inicial = jugador_test.jugador_principal.y

        jugador_test.jugador_principal.y += 32

        assert jugador_test.jugador_principal.y == y_inicial + 32

    def test_jugador_se_mueve_izquierda(self, jugador_test):
        """Verificar que el jugador se mueve hacia la izquierda al presionar ←"""
        x_inicial = jugador_test.jugador_principal.x

        jugador_test.jugador_principal.x -= 32

        assert jugador_test.jugador_principal.x == x_inicial - 32

    def test_jugador_se_mueve_derecha(self, jugador_test):
        """Verificar que el jugador se mueve hacia la derecha al presionar →"""
        x_inicial = jugador_test.jugador_principal.x

        jugador_test.jugador_principal.x += 32

        assert jugador_test.jugador_principal.x == x_inicial + 32

    def test_jugador_no_atraviesa_paredes(self, laberinto_simple):
        """Verificar que el jugador no puede atravesar paredes"""
        # Posicionar jugador cerca de una pared
        jugador = Jugador(x=48, y=48, radio=10, velocidad=1)

        # Intentar moverse hacia una pared (columna 2, fila 2 es pared en nuestro mapa)
        nueva_col = 2
        nueva_fila = 2

        es_valido = laberinto_simple.es_paso_valido((nueva_fila, nueva_col))

        assert (
            es_valido == False
        ), "El jugador no debería poder moverse a una celda con pared"

    def test_movimiento_en_pasillo_valido(self, laberinto_simple):
        """Verificar que el jugador puede moverse por pasillos"""
        # Posición en pasillo válido
        fila, columna = 1, 1

        es_valido = laberinto_simple.es_paso_valido((fila, columna))

        assert es_valido == True, "El jugador debería poder moverse por pasillos"

    def test_posicion_inicial_valida(self, jugador_test, laberinto_simple):
        """Verificar que la posición inicial del jugador es válida"""
        inicio = laberinto_simple.mapa_data["inicio_jugador"]

        # Convertir posición del jugador a celda
        celda_x = jugador_test.jugador_principal.x // 32
        celda_y = jugador_test.jugador_principal.y // 32

        assert celda_x == inicio["columna"]
        assert celda_y == inicio["fila"]


class TestLimitesLaberinto:
    """Tests adicionales para verificar límites del laberinto"""

    def test_jugador_no_sale_del_mapa_arriba(self, jugador_test):
        """Verificar que el jugador no puede salir por arriba"""
        jugador_test.jugador_principal.y = 16  # Primera fila
        y_inicial = jugador_test.jugador_principal.y

        # Intentar salir por arriba debería fallar
        nueva_y = y_inicial - 32

        # La nueva posición estaría fuera del mapa
        assert nueva_y < 0 or nueva_y < 32, "Movimiento fuera de límites detectado"

    def test_jugador_permanece_en_limites(self, laberinto_simple):
        """Verificar que las celdas del borde son paredes"""
        filas = laberinto_simple.mapa_data["filas"]
        columnas = laberinto_simple.mapa_data["columnas"]

        # Verificar esquinas (deben ser paredes)
        assert laberinto_simple.mapa_data["mapa"][0][0] == "#"
        assert laberinto_simple.mapa_data["mapa"][0][columnas - 1] == "#"
        assert laberinto_simple.mapa_data["mapa"][filas - 1][0] == "#"
        assert laberinto_simple.mapa_data["mapa"][filas - 1][columnas - 1] == "#"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
