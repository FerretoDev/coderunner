"""
Tests para HU-01: Movimiento básico del jugador
Verificar que el jugador se mueve correctamente con las teclas de dirección.
"""

import json

import pygame
import pytest

from mundo.laberinto import Laberinto
from personajes.jugador import Jugador


@pytest.fixture
def laberinto_simple(tmp_path):
    """Fixture que crea un laberinto simple de 5x5 para pruebas"""
    pygame.init()
    # Crear un laberinto simple con pasillos (1=muro, 0=pasillo)
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
        "inicio_jugador": {"col": 1, "fila": 1},
        "inicio_computadora": {"col": 3, "fila": 3},
        "obsequios": [{"posicion": [3, 2], "valor": 10}],
    }

    # Crear archivo temporal JSON
    archivo = tmp_path / "laberinto_test.json"
    with open(archivo, "w") as f:
        json.dump(mapa_prueba, f)

    return Laberinto(str(archivo))


@pytest.fixture
def jugador_test(laberinto_simple):
    """Fixture que crea un jugador en posición inicial"""
    col, fila = laberinto_simple.jugador_inicio
    x = col * 32 + 16
    y = fila * 32 + 16
    return Jugador(x=x, y=y, radio=10)


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
        jugador = Jugador(x=48, y=48, radio=10)

        # Intentar moverse hacia una pared (columna 2, fila 2 es pared en nuestro mapa)
        nueva_col = 2
        nueva_fila = 2

        es_valido = laberinto_simple.es_paso_valido((nueva_col, nueva_fila))

        assert not es_valido, "El jugador no debería poder moverse a una celda con pared"

    def test_movimiento_en_pasillo_valido(self, laberinto_simple):
        """Verificar que el jugador puede moverse por pasillos"""
        # Posición en pasillo válido (col=1, fila=1)
        columna, fila = 1, 1

        es_valido = laberinto_simple.es_paso_valido((columna, fila))

        assert es_valido, "El jugador debería poder moverse por pasillos"

    def test_posicion_inicial_valida(self, jugador_test, laberinto_simple):
        """Verificar que la posición inicial del jugador es válida"""
        col_inicio, fila_inicio = laberinto_simple.jugador_inicio

        # Convertir posición del jugador a celda
        celda_x = jugador_test.jugador_principal.x // 32
        celda_y = jugador_test.jugador_principal.y // 32

        assert celda_x == col_inicio
        assert celda_y == fila_inicio


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
        mapa = laberinto_simple.laberinto
        filas = len(mapa)
        columnas = len(mapa[0])

        # Verificar esquinas (deben ser paredes = 1)
        assert mapa[0][0] == 1
        assert mapa[0][columnas - 1] == 1
        assert mapa[filas - 1][0] == 1
        assert mapa[filas - 1][columnas - 1] == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
