"""
Tests para HU-03, HU-04, HU-05: Sistema de vidas
Verificar el sistema de vidas del jugador.
"""

import pygame
import pytest

from personajes.computadora import Computadora
from personajes.jugador import Jugador


@pytest.fixture
def jugador_con_vidas():
    """Fixture que crea un jugador con vidas"""
    pygame.init()
    return Jugador(x=100, y=100, radio=10)


@pytest.fixture
def computadora_test():
    """Fixture que crea una computadora"""
    pygame.init()
    return Computadora(x=100, y=100, radio=10, velocidad=1.5)


class TestVidasJugador:
    """CP-03: Tests de visualización de vidas"""

    def test_jugador_inicia_con_tres_vidas(self, jugador_con_vidas):
        """Verificar que el jugador inicia con 3 vidas"""
        assert jugador_con_vidas.vidas == 3, "El jugador debe iniciar con 3 vidas"

    def test_vidas_es_entero_positivo(self, jugador_con_vidas):
        """Verificar que las vidas es un número entero positivo"""
        assert isinstance(jugador_con_vidas.vidas, int), "Vidas debe ser un entero"
        assert jugador_con_vidas.vidas > 0, "Vidas debe ser positivo"

    def test_vidas_se_puede_consultar(self, jugador_con_vidas):
        """Verificar que se puede consultar el número de vidas"""
        vidas = jugador_con_vidas.vidas
        assert vidas is not None, "Debe poder consultar las vidas"
        assert 0 <= vidas <= 3, "Vidas debe estar entre 0 y 3"


class TestPerdidaVida:
    """CP-04: Tests de pérdida de vida al ser atrapado"""

    def test_jugador_pierde_vida_al_colisionar(self, jugador_con_vidas):
        """Verificar que el jugador pierde una vida al colisionar"""
        vidas_iniciales = jugador_con_vidas.vidas

        # Simular pérdida de vida usando el método correcto
        jugador_con_vidas.perder_vida()

        assert jugador_con_vidas.vidas == vidas_iniciales - 1, "Debe perder una vida"

    def test_deteccion_colision_por_distancia(
        self, jugador_con_vidas, computadora_test
    ):
        """Verificar que se detecta colisión cuando la distancia es menor al radio"""
        # Colocar computadora muy cerca del jugador
        jugador_con_vidas.jugador_principal.x = 100
        jugador_con_vidas.jugador_principal.y = 100
        computadora_test._rect.x = 105
        computadora_test._rect.y = 105

        # Calcular distancia
        dx = jugador_con_vidas.jugador_principal.x - computadora_test._rect.x
        dy = jugador_con_vidas.jugador_principal.y - computadora_test._rect.y
        distancia = (dx**2 + dy**2) ** 0.5

        # Radio de colisión (radio jugador + radio computadora)
        radio_colision = jugador_con_vidas.radio + computadora_test.radio

        # Si la distancia es menor que la suma de radios, hay colisión
        hay_colision = distancia < radio_colision

        assert hay_colision, "Debe detectar colisión cuando están muy cerca"

    def test_no_colision_cuando_lejos(self, jugador_con_vidas, computadora_test):
        """Verificar que no hay colisión cuando están lejos"""
        jugador_con_vidas.jugador_principal.x = 100
        jugador_con_vidas.jugador_principal.y = 100
        computadora_test._rect.x = 200
        computadora_test._rect.y = 200

        dx = jugador_con_vidas.jugador_principal.x - computadora_test._rect.x
        dy = jugador_con_vidas.jugador_principal.y - computadora_test._rect.y
        distancia = (dx**2 + dy**2) ** 0.5

        radio_colision = jugador_con_vidas.radio + computadora_test.radio

        hay_colision = distancia < radio_colision

        assert not hay_colision, "No debe haber colisión cuando están lejos"

    def test_vidas_no_negativos(self, jugador_con_vidas):
        """Verificar que las vidas no pueden ser negativas"""
        # Perder vidas hasta llegar a 1
        jugador_con_vidas.perder_vida()  # 2
        jugador_con_vidas.perder_vida()  # 1

        # Perder una vida más
        jugador_con_vidas.perder_vida()  # 0

        assert jugador_con_vidas.vidas == 0, "Vidas debe llegar a 0"

        # Intentar perder otra vida (debe mantenerse en 0)
        jugador_con_vidas.perder_vida()

        assert jugador_con_vidas.vidas >= 0, "Vidas no debe ser negativo"


class TestFinPartida:
    """CP-05: Tests de fin de partida"""

    def test_juego_termina_con_cero_vidas(self, jugador_con_vidas):
        """Verificar que el juego termina cuando las vidas llegan a 0"""
        # Perder todas las vidas
        jugador_con_vidas.perder_vida()
        jugador_con_vidas.perder_vida()
        jugador_con_vidas.perder_vida()

        juego_terminado = not jugador_con_vidas.esta_vivo()

        assert juego_terminado, "El juego debe terminar con 0 vidas"

    def test_juego_continua_con_vidas_restantes(self, jugador_con_vidas):
        """Verificar que el juego continúa mientras haya vidas"""
        jugador_con_vidas.perder_vida()  # 2 vidas restantes

        juego_continua = jugador_con_vidas.esta_vivo()

        assert juego_continua, "El juego debe continuar con vidas restantes"

    def test_secuencia_perdida_todas_vidas(self, jugador_con_vidas):
        """Verificar la secuencia completa de perder todas las vidas"""
        assert jugador_con_vidas.vidas == 3

        # Primera colisión
        jugador_con_vidas.perder_vida()
        assert jugador_con_vidas.vidas == 2
        assert jugador_con_vidas.esta_vivo()  # Juego continúa

        # Segunda colisión
        jugador_con_vidas.perder_vida()
        assert jugador_con_vidas.vidas == 1
        assert jugador_con_vidas.esta_vivo()  # Juego continúa

        # Tercera colisión
        jugador_con_vidas.perder_vida()
        assert jugador_con_vidas.vidas == 0
        assert not jugador_con_vidas.esta_vivo()  # Juego termina


class TestRespawn:
    """Tests adicionales relacionados con el respawn del jugador"""

    def test_jugador_puede_reposicionarse(self, jugador_con_vidas):
        """Verificar que el jugador puede ser reposicionado después de perder vida"""
        # Mover jugador lejos de su posición spawn
        jugador_con_vidas.jugador_principal.x = 300
        jugador_con_vidas.jugador_principal.y = 300

        # Verificar que se movió
        assert jugador_con_vidas.jugador_principal.x == 300
        assert jugador_con_vidas.jugador_principal.y == 300

        # Usar método respawn para volver a la posición inicial
        jugador_con_vidas.respawn()

        # Verificar que volvió al spawn (usando spawn_x y spawn_y)
        assert jugador_con_vidas.jugador_principal.x == jugador_con_vidas.spawn_x
        assert jugador_con_vidas.jugador_principal.y == jugador_con_vidas.spawn_y


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
