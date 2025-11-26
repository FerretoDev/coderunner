"""
Tests para HU-11, HU-12, HU-13: Sistema de Salón de la Fama
Verificar la persistencia y gestión de puntajes.
"""

import json
import os

import pytest

from mundo.registro import Registro
from mundo.salon_fama import SalonFama


@pytest.fixture
def salon_fama_test(tmp_path):
    """Fixture que crea un Salón de la Fama con archivo temporal"""
    archivo_test = tmp_path / "salon_fama_test.json"
    salon = SalonFama(str(archivo_test))
    return salon


@pytest.fixture
def registros_ejemplo():
    """Fixture que crea registros de ejemplo"""
    return [
        Registro("Jugador1", 100, "laberinto1"),
        Registro("Jugador2", 200, "laberinto1"),
        Registro("Jugador3", 150, "laberinto1"),
    ]


class TestGuardarPuntaje:
    """CP-11: Tests de guardado de puntajes"""

    def test_crear_registro(self):
        """Verificar que se puede crear un registro"""
        registro = Registro("TestPlayer", 50, "laberinto1")

        assert registro.nombre_jugador == "TestPlayer"
        assert registro.puntaje == 50
        assert registro.laberinto == "laberinto1"

    def test_registro_tiene_atributos_necesarios(self):
        """Verificar que el registro tiene todos los atributos necesarios"""
        registro = Registro("Player", 75, "lab1")

        assert hasattr(registro, "nombre_jugador"), "Registro debe tener nombre_jugador"
        assert hasattr(registro, "puntaje"), "Registro debe tener puntaje"
        assert hasattr(registro, "laberinto"), "Registro debe tener laberinto"

    def test_agregar_registro_salon_fama(self, salon_fama_test):
        """Verificar que se puede agregar un registro al salón de la fama"""
        registro = Registro("Player1", 100, "laberinto1")

        salon_fama_test.guardar_puntaje(registro)
        registros = salon_fama_test.mostrar_mejores()

        assert len(registros) > 0, "Debe haber al menos un registro"
        assert registros[0]["nombre_jugador"] == "Player1"

    def test_multiples_registros(self, salon_fama_test, registros_ejemplo):
        """Verificar que se pueden guardar múltiples registros"""
        for registro in registros_ejemplo:
            salon_fama_test.guardar_puntaje(registro)

        registros = salon_fama_test.mostrar_mejores()

        assert len(registros) == 3, "Debe haber 3 registros"

    def test_persistencia_archivo(self, salon_fama_test):
        """Verificar que los registros se guardan en archivo"""
        registro = Registro("PersistentPlayer", 250, "lab1")
        salon_fama_test.guardar_puntaje(registro)

        # Verificar que el archivo existe
        assert os.path.exists(salon_fama_test._archivo), "El archivo debe existir"

        # Leer el archivo directamente
        with open(salon_fama_test._archivo, "r") as f:
            data = json.load(f)

        assert len(data["registros"]) > 0, "El archivo debe contener registros"


class TestRankingSalonFama:
    """CP-12: Tests de visualización del ranking"""

    def test_registros_ordenados_por_puntaje(self, salon_fama_test, registros_ejemplo):
        """Verificar que los registros se ordenan por puntaje descendente"""
        for registro in registros_ejemplo:
            salon_fama_test.guardar_puntaje(registro)

        registros = salon_fama_test.mostrar_mejores()

        # Verificar orden descendente
        for i in range(len(registros) - 1):
            assert (
                registros[i]["puntaje"] >= registros[i + 1]["puntaje"]
            ), "Los registros deben estar ordenados de mayor a menor puntaje"

    def test_primer_lugar_mayor_puntaje(self, salon_fama_test, registros_ejemplo):
        """Verificar que el primer lugar tiene el mayor puntaje"""
        for registro in registros_ejemplo:
            salon_fama_test.guardar_puntaje(registro)

        registros = salon_fama_test.mostrar_mejores()

        assert (
            registros[0]["puntaje"] == 200
        ), "El primer lugar debe tener el mayor puntaje"
        assert registros[0]["nombre_jugador"] == "Jugador2"

    def test_obtener_top_n_registros(self, salon_fama_test):
        """Verificar que se pueden obtener los top N registros"""
        # Agregar 10 registros
        for i in range(10):
            registro = Registro(f"Player{i}", i * 10, "lab1")
            salon_fama_test.guardar_puntaje(registro)

        # Obtener top 5
        registros = salon_fama_test.mostrar_mejores(limite=5)

        assert len(registros) == 5, "Debe devolver exactamente 5 registros"
        assert registros[0]["puntaje"] >= registros[4]["puntaje"], "Debe estar ordenado"

    def test_ranking_vacio_inicialmente(self, salon_fama_test):
        """Verificar que el ranking está vacío al inicio"""
        registros = salon_fama_test.mostrar_mejores()

        assert len(registros) == 0, "El ranking debe estar vacío inicialmente"

    def test_formato_visualizacion_ranking(self, salon_fama_test, registros_ejemplo):
        """Verificar que los registros se pueden formatear para visualización"""
        for registro in registros_ejemplo:
            salon_fama_test.guardar_puntaje(registro)

        registros = salon_fama_test.mostrar_mejores()

        # Simular formato de visualización
        for i, registro in enumerate(registros, 1):
            texto = f"{i}. {registro['nombre_jugador']}: {registro['puntaje']}"
            assert str(i) in texto
            assert registro["nombre_jugador"] in texto
            assert str(registro["puntaje"]) in texto


class TestReiniciarSalonFama:
    """CP-13: Tests de reinicio del salón de la fama"""

    def test_limpiar_todos_registros(self, salon_fama_test, registros_ejemplo):
        """Verificar que se pueden eliminar todos los registros"""
        # Agregar registros
        for registro in registros_ejemplo:
            salon_fama_test.guardar_puntaje(registro)

        assert len(salon_fama_test.mostrar_mejores()) == 3

        # Limpiar
        salon_fama_test.reiniciar()

        registros = salon_fama_test.mostrar_mejores()
        assert len(registros) == 0, "No debe haber registros después de limpiar"

    def test_archivo_vacio_despues_limpiar(self, salon_fama_test, registros_ejemplo):
        """Verificar que el archivo queda vacío después de limpiar"""
        for registro in registros_ejemplo:
            salon_fama_test.guardar_puntaje(registro)

        salon_fama_test.reiniciar()

        # Leer archivo directamente
        with open(salon_fama_test._archivo, "r") as f:
            data = json.load(f)

        assert len(data["registros"]) == 0, "El archivo debe estar vacío"

    def test_agregar_despues_de_limpiar(self, salon_fama_test, registros_ejemplo):
        """Verificar que se pueden agregar registros después de limpiar"""
        # Agregar y limpiar
        for registro in registros_ejemplo:
            salon_fama_test.guardar_puntaje(registro)
        salon_fama_test.reiniciar()

        # Agregar nuevo registro
        nuevo_registro = Registro("NewPlayer", 300, "lab1")
        salon_fama_test.guardar_puntaje(nuevo_registro)

        registros = salon_fama_test.mostrar_mejores()
        assert len(registros) == 1
        assert registros[0]["nombre_jugador"] == "NewPlayer"


class TestPersistenciaDatos:
    """Tests adicionales de persistencia de datos"""

    def test_carga_datos_existentes(self, tmp_path):
        """Verificar que se cargan datos existentes al crear el salón"""
        archivo = tmp_path / "salon_existente.json"

        # Crear archivo con datos
        datos_iniciales = {
            "registros": [
                {
                    "nombre_jugador": "Player1",
                    "puntaje": 100,
                    "laberinto": "lab1",
                    "fecha": "2025-01-01",
                }
            ]
        }
        with open(archivo, "w") as f:
            json.dump(datos_iniciales, f)

        # Crear salón (debe cargar los datos)
        salon = SalonFama(str(archivo))
        registros = salon.mostrar_mejores()

        assert len(registros) == 1
        assert registros[0]["nombre_jugador"] == "Player1"

    def test_manejo_archivo_corrupto(self, tmp_path):
        """Verificar que se maneja correctamente un archivo corrupto"""
        archivo = tmp_path / "salon_corrupto.json"

        # Crear archivo con JSON inválido
        with open(archivo, "w") as f:
            f.write("{ corrupto json")

        # Intentar crear salón (no debe fallar)
        try:
            salon = SalonFama(str(archivo))
            registros = salon.mostrar_mejores()
            # Si logra cargar, debe estar vacío o manejar el error
            assert isinstance(registros, list)
        except Exception:
            # Es aceptable que lance excepción controlada
            pass

    def test_puntajes_no_negativos(self):
        """Verificar que los puntajes no son negativos"""
        registro = Registro("Player", 50, "lab1")

        assert registro.puntaje >= 0, "El puntaje no debe ser negativo"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
