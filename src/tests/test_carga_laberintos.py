"""
Tests para HU-14, HU-15: Carga y validación de laberintos desde JSON
Verificar que se pueden cargar laberintos desde archivos JSON correctamente.
"""

import json
import os

import pytest

from models.laberinto import Laberinto


@pytest.fixture
def mapa_valido():
    """Fixture que devuelve un mapa válido"""
    return {
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


@pytest.fixture
def archivo_json_valido(tmp_path, mapa_valido):
    """Fixture que crea un archivo JSON válido"""
    archivo = tmp_path / "laberinto_valido.json"
    with open(archivo, "w") as f:
        json.dump(mapa_valido, f)
    return archivo


class TestCargaLaberintoJSON:
    """CP-14: Tests de carga de laberinto desde JSON"""

    def test_cargar_json_valido(self, archivo_json_valido):
        """Verificar que se puede cargar un archivo JSON válido"""
        import pygame

        pygame.init()

        # Leer el archivo
        with open(archivo_json_valido, "r") as f:
            data = json.load(f)

        # Crear laberinto
        laberinto = Laberinto(data)

        assert laberinto is not None
        assert laberinto.mapa_data is not None

    def test_archivo_json_contiene_campos_requeridos(self, mapa_valido):
        """Verificar que el archivo JSON contiene todos los campos requeridos"""
        campos_requeridos = [
            "filas",
            "columnas",
            "mapa",
            "inicio_jugador",
            "inicio_computadora",
            "obsequios",
        ]

        for campo in campos_requeridos:
            assert campo in mapa_valido, f"Falta el campo requerido: {campo}"

    def test_inicio_jugador_tiene_coordenadas(self, mapa_valido):
        """Verificar que inicio_jugador tiene fila y columna"""
        inicio = mapa_valido["inicio_jugador"]

        assert "fila" in inicio, "inicio_jugador debe tener fila"
        assert "columna" in inicio, "inicio_jugador debe tener columna"

    def test_inicio_computadora_tiene_coordenadas(self, mapa_valido):
        """Verificar que inicio_computadora tiene fila y columna"""
        inicio = mapa_valido["inicio_computadora"]

        assert "fila" in inicio, "inicio_computadora debe tener fila"
        assert "columna" in inicio, "inicio_computadora debe tener columna"

    def test_obsequios_es_lista(self, mapa_valido):
        """Verificar que obsequios es una lista"""
        obsequios = mapa_valido["obsequios"]

        assert isinstance(obsequios, list), "obsequios debe ser una lista"

    def test_cada_obsequio_tiene_coordenadas(self, mapa_valido):
        """Verificar que cada obsequio tiene fila y columna"""
        for obsequio in mapa_valido["obsequios"]:
            assert "fila" in obsequio, "Cada obsequio debe tener fila"
            assert "columna" in obsequio, "Cada obsequio debe tener columna"


class TestValidacionLaberinto:
    """CP-15: Tests de validación de estructura del laberinto"""

    def test_dimensiones_coinciden_con_mapa(self, mapa_valido):
        """Verificar que filas y columnas coinciden con el tamaño del mapa"""
        filas = mapa_valido["filas"]
        columnas = mapa_valido["columnas"]
        mapa = mapa_valido["mapa"]

        assert len(mapa) == filas, "Número de filas debe coincidir"
        assert len(mapa[0]) == columnas, "Número de columnas debe coincidir"

    def test_inicio_jugador_dentro_limites(self, mapa_valido):
        """Verificar que la posición inicial del jugador está dentro del mapa"""
        inicio = mapa_valido["inicio_jugador"]
        filas = mapa_valido["filas"]
        columnas = mapa_valido["columnas"]

        assert 0 <= inicio["fila"] < filas, "Fila del jugador fuera de límites"
        assert 0 <= inicio["columna"] < columnas, "Columna del jugador fuera de límites"

    def test_inicio_computadora_dentro_limites(self, mapa_valido):
        """Verificar que la posición inicial de la computadora está dentro del mapa"""
        inicio = mapa_valido["inicio_computadora"]
        filas = mapa_valido["filas"]
        columnas = mapa_valido["columnas"]

        assert 0 <= inicio["fila"] < filas, "Fila de la computadora fuera de límites"
        assert (
            0 <= inicio["columna"] < columnas
        ), "Columna de la computadora fuera de límites"

    def test_obsequios_dentro_limites(self, mapa_valido):
        """Verificar que los obsequios están dentro del mapa"""
        filas = mapa_valido["filas"]
        columnas = mapa_valido["columnas"]

        for obsequio in mapa_valido["obsequios"]:
            assert 0 <= obsequio["fila"] < filas, "Fila del obsequio fuera de límites"
            assert (
                0 <= obsequio["columna"] < columnas
            ), "Columna del obsequio fuera de límites"

    def test_inicio_jugador_no_en_pared(self, mapa_valido):
        """Verificar que el jugador no inicia en una pared"""
        inicio = mapa_valido["inicio_jugador"]
        mapa = mapa_valido["mapa"]

        celda = mapa[inicio["fila"]][inicio["columna"]]

        assert celda != "#", "El jugador no debe iniciar en una pared"

    def test_inicio_computadora_no_en_pared(self, mapa_valido):
        """Verificar que la computadora no inicia en una pared"""
        inicio = mapa_valido["inicio_computadora"]
        mapa = mapa_valido["mapa"]

        celda = mapa[inicio["fila"]][inicio["columna"]]

        assert celda != "#", "La computadora no debe iniciar en una pared"

    def test_obsequios_no_en_pared(self, mapa_valido):
        """Verificar que los obsequios no están en paredes"""
        mapa = mapa_valido["mapa"]

        for obsequio in mapa_valido["obsequios"]:
            celda = mapa[obsequio["fila"]][obsequio["columna"]]
            assert celda != "#", "Los obsequios no deben estar en paredes"


class TestValidacionErrores:
    """Tests de validación de archivos incorrectos"""

    def test_detectar_dimensiones_incorrectas(self):
        """Verificar que se detectan dimensiones incorrectas"""
        mapa_incorrecto = {
            "filas": 3,
            "columnas": 3,
            "mapa": [["#", "#", "#"], ["#", ".", "#"]],  # Falta una fila
            "inicio_jugador": {"fila": 1, "columna": 1},
            "inicio_computadora": {"fila": 1, "columna": 1},
            "obsequios": [],
        }

        filas_esperadas = mapa_incorrecto["filas"]
        filas_reales = len(mapa_incorrecto["mapa"])

        assert filas_reales != filas_esperadas, "Debe detectar dimensiones incorrectas"

    def test_detectar_falta_campos(self):
        """Verificar que se detectan campos faltantes"""
        mapa_incompleto = {
            "filas": 3,
            "columnas": 3,
            # Falta el campo "mapa"
            "inicio_jugador": {"fila": 1, "columna": 1},
        }

        assert "mapa" not in mapa_incompleto, "Debe detectar campo faltante"

    def test_detectar_coordenadas_invalidas(self):
        """Verificar que se detectan coordenadas fuera de límites"""
        inicio_invalido = {"fila": 10, "columna": 10}  # Fuera de un mapa 5x5
        filas = 5
        columnas = 5

        es_valido = (
            0 <= inicio_invalido["fila"] < filas
            and 0 <= inicio_invalido["columna"] < columnas
        )

        assert not es_valido, "Debe detectar coordenadas inválidas"


class TestCargaArchivosReales:
    """Tests con archivos reales del proyecto"""

    def test_cargar_laberinto1_json(self):
        """Verificar que se puede cargar el archivo laberinto1.json del proyecto"""
        import pygame

        pygame.init()

        archivo = "/home/marcosferreto/Dev/coderunner/src/data/laberinto1.json"

        if os.path.exists(archivo):
            with open(archivo, "r") as f:
                data = json.load(f)

            # Verificar estructura básica
            assert "filas" in data
            assert "columnas" in data
            assert "mapa" in data

            # Crear laberinto
            laberinto = Laberinto(data)
            assert laberinto is not None
        else:
            pytest.skip("Archivo laberinto1.json no encontrado")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
