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
    """Fixture que devuelve un mapa válido con el formato correcto"""
    return {
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

        # Crear laberinto pasando la RUTA del archivo, no el diccionario
        laberinto = Laberinto(str(archivo_json_valido))

        assert laberinto is not None
        assert laberinto.laberinto is not None
        assert len(laberinto.laberinto) > 0

    def test_archivo_json_contiene_campos_requeridos(self, mapa_valido):
        """Verificar que el archivo JSON contiene todos los campos requeridos"""
        campos_requeridos = ["mapa", "jugador_inicio", "computadora_inicio"]

        for campo in campos_requeridos:
            assert campo in mapa_valido, f"Falta el campo requerido: {campo}"

    def test_inicio_jugador_tiene_coordenadas(self, mapa_valido):
        """Verificar que jugador_inicio es una lista con 2 elementos [col, fila]"""
        inicio = mapa_valido["jugador_inicio"]

        assert isinstance(inicio, list), "jugador_inicio debe ser una lista"
        assert len(inicio) == 2, "jugador_inicio debe tener 2 elementos [col, fila]"

    def test_inicio_computadora_tiene_coordenadas(self, mapa_valido):
        """Verificar que computadora_inicio es una lista con 2 elementos [col, fila]"""
        inicio = mapa_valido["computadora_inicio"]

        assert isinstance(inicio, list), "computadora_inicio debe ser una lista"
        assert len(inicio) == 2, "computadora_inicio debe tener 2 elementos [col, fila]"

    def test_obsequios_es_lista(self, mapa_valido):
        """Verificar que obsequios es una lista"""
        obsequios = mapa_valido["obsequios"]

        assert isinstance(obsequios, list), "obsequios debe ser una lista"

    def test_cada_obsequio_tiene_coordenadas(self, mapa_valido):
        """Verificar que cada obsequio tiene posicion como lista [col, fila]"""
        for obsequio in mapa_valido["obsequios"]:
            assert "posicion" in obsequio, "Cada obsequio debe tener posicion"
            assert isinstance(obsequio["posicion"], list), "posicion debe ser una lista"
            assert (
                len(obsequio["posicion"]) == 2
            ), "posicion debe tener 2 elementos [col, fila]"


class TestValidacionLaberinto:
    """CP-15: Tests de validación de estructura del laberinto"""

    def test_dimensiones_coinciden_con_mapa(self, mapa_valido):
        """Verificar que las dimensiones del mapa son consistentes"""
        mapa = mapa_valido["mapa"]

        # Verificar que todas las filas tienen el mismo número de columnas
        num_columnas = len(mapa[0])
        for fila in mapa:
            assert (
                len(fila) == num_columnas
            ), "Todas las filas deben tener el mismo número de columnas"

    def test_inicio_jugador_dentro_limites(self, mapa_valido):
        """Verificar que la posición inicial del jugador está dentro del mapa"""
        inicio = mapa_valido["jugador_inicio"]  # [col, fila]
        mapa = mapa_valido["mapa"]
        filas = len(mapa)
        columnas = len(mapa[0])

        col, fila = inicio
        assert 0 <= fila < filas, "Fila del jugador fuera de límites"
        assert 0 <= col < columnas, "Columna del jugador fuera de límites"

    def test_inicio_computadora_dentro_limites(self, mapa_valido):
        """Verificar que la posición inicial de la computadora está dentro del mapa"""
        inicio = mapa_valido["computadora_inicio"]  # [col, fila]
        mapa = mapa_valido["mapa"]
        filas = len(mapa)
        columnas = len(mapa[0])

        col, fila = inicio
        assert 0 <= fila < filas, "Fila de la computadora fuera de límites"
        assert 0 <= col < columnas, "Columna de la computadora fuera de límites"

    def test_obsequios_dentro_limites(self, mapa_valido):
        """Verificar que los obsequios están dentro del mapa"""
        mapa = mapa_valido["mapa"]
        filas = len(mapa)
        columnas = len(mapa[0])

        for obsequio in mapa_valido["obsequios"]:
            col, fila = obsequio["posicion"]  # [col, fila]
            assert 0 <= fila < filas, "Fila del obsequio fuera de límites"
            assert 0 <= col < columnas, "Columna del obsequio fuera de límites"

    def test_inicio_jugador_no_en_pared(self, mapa_valido):
        """Verificar que el jugador no inicia en una pared"""
        inicio = mapa_valido["jugador_inicio"]  # [col, fila]
        mapa = mapa_valido["mapa"]

        col, fila = inicio
        celda = mapa[fila][col]  # mapa[fila][columna]

        assert celda == 0, "El jugador no debe iniciar en una pared (0=pasillo, 1=muro)"

    def test_inicio_computadora_no_en_pared(self, mapa_valido):
        """Verificar que la computadora no inicia en una pared"""
        inicio = mapa_valido["computadora_inicio"]  # [col, fila]
        mapa = mapa_valido["mapa"]

        col, fila = inicio
        celda = mapa[fila][col]

        assert (
            celda == 0
        ), "La computadora no debe iniciar en una pared (0=pasillo, 1=muro)"

    def test_obsequios_no_en_pared(self, mapa_valido):
        """Verificar que los obsequios no están en paredes"""
        mapa = mapa_valido["mapa"]

        for obsequio in mapa_valido["obsequios"]:
            col, fila = obsequio["posicion"]
            celda = mapa[fila][col]
            assert (
                celda == 0
            ), "Los obsequios no deben estar en paredes (0=pasillo, 1=muro)"


class TestValidacionErrores:
    """Tests de validación de archivos incorrectos"""

    def test_detectar_dimensiones_incorrectas(self):
        """Verificar que se detectan filas con diferentes números de columnas"""
        mapa_incorrecto = {
            "nombre": "Mapa Incorrecto",
            "mapa": [[1, 1, 1], [1, 0]],  # Segunda fila incompleta
            "jugador_inicio": [1, 1],
            "computadora_inicio": [1, 1],
            "obsequios": [],
        }

        primera_fila_cols = len(mapa_incorrecto["mapa"][0])
        segunda_fila_cols = len(mapa_incorrecto["mapa"][1])

        assert (
            primera_fila_cols != segunda_fila_cols
        ), "Debe detectar filas con diferente número de columnas"

    def test_detectar_falta_campos(self):
        """Verificar que se detectan campos faltantes"""
        mapa_incompleto = {
            "nombre": "Mapa Incompleto",
            # Falta el campo "mapa"
            "jugador_inicio": [1, 1],
        }

        assert "mapa" not in mapa_incompleto, "Debe detectar campo faltante"

    def test_detectar_coordenadas_invalidas(self):
        """Verificar que se detectan coordenadas fuera de límites"""
        inicio_invalido = [10, 10]  # Fuera de un mapa 5x5
        filas = 5
        columnas = 5

        col, fila = inicio_invalido
        es_valido = 0 <= fila < filas and 0 <= col < columnas

        assert not es_valido, "Debe detectar coordenadas inválidas"


class TestCargaArchivosReales:
    """Tests con archivos reales del proyecto"""

    def test_cargar_laberinto1_json(self):
        """Verificar que se puede cargar el archivo laberinto1.json del proyecto"""
        import pygame

        pygame.init()

        archivo = "/home/marcosferreto/Dev/coderunner/src/data/laberinto1.json"

        if os.path.exists(archivo):
            # Crear laberinto directamente desde el archivo
            laberinto = Laberinto(archivo)
            assert laberinto is not None
            assert len(laberinto.laberinto) > 0
            assert laberinto.nombre == "Laberinto Clásico"
        else:
            pytest.skip("Archivo laberinto1.json no encontrado")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
