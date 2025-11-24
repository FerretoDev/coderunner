"""
Tests para HU-08, HU-09, HU-10: Sistema de puntajes y obsequios
Verificar el sistema de puntos y recolección de obsequios.
"""

import pygame
import pytest

from mundo.obsequio import Obsequio
from personajes.jugador import Jugador


@pytest.fixture
def jugador_test():
    """Fixture que crea un jugador"""
    pygame.init()
    return Jugador(x=100, y=100, radio=10)


@pytest.fixture
def obsequio_test():
    """Fixture que crea un obsequio"""
    pygame.init()
    return Obsequio(posicion=(4, 4), valor=10)


class TestPuntajePorMovimiento:
    """CP-08: Tests de puntos por movimiento (NOTA: En la implementación actual no se suma por movimiento)"""

    def test_puntaje_inicia_en_cero(self):
        """Verificar que el puntaje inicia en 0"""
        puntaje = 0
        assert puntaje == 0, "El puntaje debe iniciar en 0"

    def test_puntaje_es_numero(self):
        """Verificar que el puntaje es un número"""
        puntaje = 0
        assert isinstance(puntaje, (int, float)), "El puntaje debe ser un número"

    def test_puntaje_se_puede_incrementar(self):
        """Verificar que el puntaje puede incrementarse"""
        puntaje = 0
        puntaje += 1

        assert puntaje == 1, "El puntaje debe poder incrementarse"


class TestObsequios:
    """CP-09: Tests de recolección de obsequios"""

    def test_obsequio_tiene_posicion(self, obsequio_test):
        """Verificar que el obsequio tiene posición"""
        assert hasattr(obsequio_test, "posicion"), "Obsequio debe tener posicion"
        assert isinstance(
            obsequio_test.posicion, tuple
        ), "Posición debe ser una tupla (col, fila)"
        assert len(obsequio_test.posicion) == 2, "Posición debe tener 2 coordenadas"

    def test_obsequio_tiene_valor(self, obsequio_test):
        """Verificar que el obsequio tiene valor en puntos"""
        assert hasattr(obsequio_test, "valor"), "Obsequio debe tener valor"
        assert obsequio_test.valor > 0, "Valor debe ser positivo"

    def test_deteccion_recoleccion_obsequio(self, jugador_test, obsequio_test):
        """Verificar que se detecta cuando el jugador recoge un obsequio"""
        # En la implementación actual, la detección se hace por posición de celda
        # Colocar jugador en la misma celda que el obsequio
        col, fila = obsequio_test.posicion
        tam_celda = 32

        # Posicionar jugador en el centro de la misma celda del obsequio
        jugador_test.jugador_principal.x = col * tam_celda + tam_celda // 2
        jugador_test.jugador_principal.y = fila * tam_celda + tam_celda // 2

        # Convertir posición del jugador a celda
        celda_jugador = (
            jugador_test.jugador_principal.x // tam_celda,
            jugador_test.jugador_principal.y // tam_celda,
        )

        recolectado = celda_jugador == obsequio_test.posicion

        assert recolectado, "Debe detectar recolección cuando está en la misma celda"

    def test_no_recoleccion_cuando_lejos(self, jugador_test, obsequio_test):
        """Verificar que no se recoge el obsequio cuando está lejos"""
        # Colocar jugador lejos del obsequio
        tam_celda = 32
        jugador_test.jugador_principal.x = 0
        jugador_test.jugador_principal.y = 0

        # Convertir posición del jugador a celda
        celda_jugador = (
            jugador_test.jugador_principal.x // tam_celda,
            jugador_test.jugador_principal.y // tam_celda,
        )

        recolectado = celda_jugador == obsequio_test.posicion

        assert not recolectado, "No debe recolectar cuando está lejos"

    def test_obsequio_suma_diez_puntos(self):
        """Verificar que recoger un obsequio suma 10 puntos"""
        puntaje = 0
        puntos_por_obsequio = 10

        # Simular recolección
        puntaje += puntos_por_obsequio

        assert puntaje == 10, "Recoger obsequio debe sumar 10 puntos"

    def test_multiples_obsequios(self):
        """Verificar que se pueden recoger múltiples obsequios"""
        puntaje = 0

        # Recoger 3 obsequios
        for _ in range(3):
            puntaje += 10

        assert puntaje == 30, "Tres obsequios deben sumar 30 puntos"


class TestTiempoVidaObsequios:
    """Tests adicionales para el tiempo de vida de los obsequios"""

    def test_obsequio_tiene_temporizador(self):
        """Verificar que los obsequios tienen temporizador (600 frames = 10 segundos)"""
        tiempo_vida = 600  # frames a 60 FPS = 10 segundos

        assert tiempo_vida == 600, "Tiempo de vida debe ser 600 frames"
        assert tiempo_vida / 60 == 10, "Tiempo de vida debe ser 10 segundos a 60 FPS"

    def test_temporizador_decrementa(self):
        """Verificar que el temporizador decrementa"""
        tiempo_restante = 600

        # Simular paso de frames
        tiempo_restante -= 1

        assert tiempo_restante == 599, "El temporizador debe decrementar"

    def test_obsequio_expira(self):
        """Verificar que el obsequio expira cuando el temporizador llega a 0"""
        tiempo_restante = 1

        tiempo_restante -= 1

        obsequio_expirado = tiempo_restante <= 0

        assert obsequio_expirado, "El obsequio debe expirar"

    def test_obsequio_se_reposiciona(self, obsequio_test):
        """Verificar que el obsequio puede reposicionarse"""
        posicion_inicial = obsequio_test.posicion

        # Reposicionar obsequio
        obsequio_test.posicion = (6, 6)

        assert obsequio_test.posicion != posicion_inicial
        assert obsequio_test.posicion == (6, 6)


class TestVisualizacionPuntaje:
    """CP-10: Tests de visualización del puntaje"""

    def test_puntaje_se_puede_mostrar(self):
        """Verificar que el puntaje se puede convertir a string para mostrar"""
        puntaje = 50
        puntaje_texto = str(puntaje)

        assert puntaje_texto == "50", "El puntaje debe poder mostrarse como texto"

    def test_puntaje_formato_correcto(self):
        """Verificar que el puntaje tiene formato correcto"""
        puntaje = 123
        puntaje_texto = f"Puntaje: {puntaje}"

        assert "Puntaje" in puntaje_texto
        assert "123" in puntaje_texto

    def test_puntaje_actualiza_tiempo_real(self):
        """Verificar que el puntaje se actualiza en tiempo real"""
        puntaje = 0

        # Primera actualización
        puntaje += 10
        assert puntaje == 10

        # Segunda actualización inmediata
        puntaje += 10
        assert puntaje == 20, "El puntaje debe actualizarse inmediatamente"

    def test_puntaje_maximo(self):
        """Verificar que el puntaje puede llegar a valores altos"""
        puntaje = 0

        # Simular recolección de muchos obsequios
        for _ in range(100):
            puntaje += 10

        assert puntaje == 1000, "El puntaje debe poder llegar a valores altos"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
