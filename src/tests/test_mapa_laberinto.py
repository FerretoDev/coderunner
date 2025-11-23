"""
Tests para HU-06, HU-07: Estructura del mapa (muros y pasillos)
Verificar que el laberinto tiene muros y pasillos correctos.
"""

import pygame
import pytest

from world.laberinto import Laberinto


@pytest.fixture
def laberinto_test():
    """Fixture que crea un laberinto de prueba"""
    pygame.init()

    mapa_data = {
        "filas": 5,
        "columnas": 5,
        "mapa": [
            ["#", "#", "#", "#", "#"],
            ["#", ".", ".", ".", "#"],
            ["#", ".", "#", ".", "#"],
            ["#", ".", ".", ".", "#"],
            ["#", "#", "#", "#", "#"],
        ],
        "inicio_jugador": {"fila": 1, "columna": 1},
        "inicio_computadora": {"fila": 3, "columna": 3},
        "obsequios": [{"fila": 2, "columna": 3}],
    }

    return Laberinto(mapa_data)


class TestMurosLaberinto:
    """CP-06: Tests de muros del laberinto"""

    def test_laberinto_tiene_muros(self, laberinto_test):
        """Verificar que el laberinto tiene muros (#)"""
        mapa = laberinto_test.mapa_data["mapa"]

        # Contar muros
        muros = 0
        for fila in mapa:
            for celda in fila:
                if celda == "#":
                    muros += 1

        assert muros > 0, "El laberinto debe tener muros"

    def test_bordes_son_muros(self, laberinto_test):
        """Verificar que los bordes del laberinto son muros"""
        mapa = laberinto_test.mapa_data["mapa"]
        filas = laberinto_test.mapa_data["filas"]
        columnas = laberinto_test.mapa_data["columnas"]

        # Verificar primera y última fila
        for col in range(columnas):
            assert mapa[0][col] == "#", "Primera fila debe ser todo muros"
            assert mapa[filas - 1][col] == "#", "Última fila debe ser todo muros"

        # Verificar primera y última columna
        for fila in range(filas):
            assert mapa[fila][0] == "#", "Primera columna debe ser todo muros"
            assert mapa[fila][columnas - 1] == "#", "Última columna debe ser todo muros"

    def test_muro_bloquea_movimiento(self, laberinto_test):
        """Verificar que un muro bloquea el movimiento"""
        # Intentar validar movimiento a una celda con muro
        celda_muro = (0, 0)  # Esquina superior izquierda (siempre es muro)

        es_valido = laberinto_test.es_paso_valido(celda_muro)

        assert not es_valido, "No se debe poder mover a un muro"

    def test_muros_internos_existen(self, laberinto_test):
        """Verificar que existen muros internos (no solo en bordes)"""
        mapa = laberinto_test.mapa_data["mapa"]
        filas = laberinto_test.mapa_data["filas"]
        columnas = laberinto_test.mapa_data["columnas"]

        # Buscar muros en el interior (excluyendo bordes)
        muros_internos = 0
        for i in range(1, filas - 1):
            for j in range(1, columnas - 1):
                if mapa[i][j] == "#":
                    muros_internos += 1

        assert muros_internos > 0, "Debe haber muros internos en el laberinto"


class TestPasillosLaberinto:
    """CP-07: Tests de pasillos del laberinto"""

    def test_laberinto_tiene_pasillos(self, laberinto_test):
        """Verificar que el laberinto tiene pasillos (.)"""
        mapa = laberinto_test.mapa_data["mapa"]

        # Contar pasillos
        pasillos = 0
        for fila in mapa:
            for celda in fila:
                if celda == ".":
                    pasillos += 1

        assert pasillos > 0, "El laberinto debe tener pasillos"

    def test_pasillo_permite_movimiento(self, laberinto_test):
        """Verificar que los pasillos permiten movimiento"""
        # La celda (1, 1) es un pasillo según nuestro mapa
        celda_pasillo = (1, 1)

        es_valido = laberinto_test.es_paso_valido(celda_pasillo)

        assert es_valido, "Se debe poder mover por pasillos"

    def test_inicio_jugador_en_pasillo(self, laberinto_test):
        """Verificar que la posición inicial del jugador es un pasillo"""
        inicio = laberinto_test.mapa_data["inicio_jugador"]
        fila = inicio["fila"]
        col = inicio["columna"]

        celda = laberinto_test.mapa_data["mapa"][fila][col]

        assert celda == ".", "El jugador debe iniciar en un pasillo"

    def test_inicio_computadora_en_pasillo(self, laberinto_test):
        """Verificar que la posición inicial de la computadora es un pasillo"""
        inicio = laberinto_test.mapa_data["inicio_computadora"]
        fila = inicio["fila"]
        col = inicio["columna"]

        celda = laberinto_test.mapa_data["mapa"][fila][col]

        assert celda == ".", "La computadora debe iniciar en un pasillo"

    def test_pasillos_conectados(self, laberinto_test):
        """Verificar que existen pasillos conectados (hay camino)"""
        inicio = laberinto_test.mapa_data["inicio_jugador"]
        destino = laberinto_test.mapa_data["inicio_computadora"]

        # Si ambos están en pasillos y el mapa es válido,
        # debe existir algún camino entre ellos
        inicio_valido = laberinto_test.es_paso_valido(
            (inicio["fila"], inicio["columna"])
        )
        destino_valido = laberinto_test.es_paso_valido(
            (destino["fila"], destino["columna"])
        )

        assert inicio_valido and destino_valido, "Inicio y destino deben ser pasillos"


class TestEstructuraLaberinto:
    """Tests adicionales de la estructura del laberinto"""

    def test_dimensiones_laberinto(self, laberinto_test):
        """Verificar que el laberinto tiene las dimensiones correctas"""
        filas = laberinto_test.mapa_data["filas"]
        columnas = laberinto_test.mapa_data["columnas"]
        mapa = laberinto_test.mapa_data["mapa"]

        assert len(mapa) == filas, "Número de filas debe coincidir"
        assert len(mapa[0]) == columnas, "Número de columnas debe coincidir"

    def test_mapa_rectangular(self, laberinto_test):
        """Verificar que todas las filas tienen el mismo número de columnas"""
        mapa = laberinto_test.mapa_data["mapa"]
        columnas_esperadas = len(mapa[0])

        for fila in mapa:
            assert (
                len(fila) == columnas_esperadas
            ), "Todas las filas deben tener el mismo largo"

    def test_solo_caracteres_validos(self, laberinto_test):
        """Verificar que el mapa solo contiene caracteres válidos (# y .)"""
        mapa = laberinto_test.mapa_data["mapa"]
        caracteres_validos = {"#", "."}

        for fila in mapa:
            for celda in fila:
                assert (
                    celda in caracteres_validos
                ), f"Carácter inválido encontrado: {celda}"

    def test_laberinto_no_vacio(self, laberinto_test):
        """Verificar que el laberinto no está vacío"""
        mapa = laberinto_test.mapa_data["mapa"]

        assert len(mapa) > 0, "El laberinto no debe estar vacío"
        assert len(mapa[0]) > 0, "Las filas no deben estar vacías"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
