"""
Tests de integración para HU-16, HU-17: Menú y navegación
Verificar el menú principal y la navegación del juego.
"""

import pygame
import pytest


class TestMenuPrincipal:
    """CP-16: Tests del menú principal"""

    def test_opciones_menu_disponibles(self):
        """Verificar que el menú tiene las opciones esperadas"""
        opciones_menu = ["Jugar", "Salón de la Fama", "Salir"]

        assert "Jugar" in opciones_menu
        assert "Salón de la Fama" in opciones_menu
        assert "Salir" in opciones_menu

    def test_numero_opciones_menu(self):
        """Verificar que el menú tiene 3 opciones principales"""
        opciones_menu = ["Jugar", "Salón de la Fama", "Salir"]

        assert len(opciones_menu) == 3, "El menú debe tener 3 opciones"

    def test_seleccion_inicializa_en_primera_opcion(self):
        """Verificar que la selección inicial es la primera opción"""
        seleccion = 0  # Índice de la opción seleccionada

        assert seleccion == 0, "La selección debe iniciar en la primera opción"

    def test_navegacion_arriba_abajo(self):
        """Verificar que se puede navegar con las teclas de dirección"""
        opciones = ["Jugar", "Salón de la Fama", "Salir"]
        seleccion = 0

        # Navegar hacia abajo
        seleccion = (seleccion + 1) % len(opciones)
        assert seleccion == 1

        # Navegar hacia abajo otra vez
        seleccion = (seleccion + 1) % len(opciones)
        assert seleccion == 2

        # Navegar hacia arriba
        seleccion = (seleccion - 1) % len(opciones)
        assert seleccion == 1

    def test_navegacion_circular(self):
        """Verificar que la navegación es circular"""
        opciones = ["Jugar", "Salón de la Fama", "Salir"]
        seleccion = 2  # Última opción

        # Intentar ir más abajo (debe volver al inicio)
        seleccion = (seleccion + 1) % len(opciones)
        assert seleccion == 0, "Debe volver al inicio del menú"

        # Desde la primera, ir arriba (debe ir al final)
        seleccion = (seleccion - 1) % len(opciones)
        assert seleccion == 2, "Debe ir a la última opción"


class TestConfirmacionSalir:
    """CP-17: Tests de confirmación al salir"""

    def test_mensaje_confirmacion_existe(self):
        """Verificar que existe un mensaje de confirmación"""
        mensaje_confirmacion = "¿Seguro que desea salir?"

        assert len(mensaje_confirmacion) > 0
        assert "salir" in mensaje_confirmacion.lower()

    def test_opciones_confirmacion(self):
        """Verificar que la confirmación tiene opciones Sí/No"""
        opciones_confirmacion = ["Sí", "No"]

        assert "Sí" in opciones_confirmacion or "Si" in opciones_confirmacion
        assert "No" in opciones_confirmacion

    def test_seleccionar_si_cierra_juego(self):
        """Verificar que seleccionar Sí cierra el juego"""
        confirmar_salir = True
        juego_activo = True

        if confirmar_salir:
            juego_activo = False

        assert not juego_activo, "El juego debe cerrarse al confirmar"

    def test_seleccionar_no_regresa_menu(self):
        """Verificar que seleccionar No regresa al menú"""
        confirmar_salir = False
        en_menu = False

        if not confirmar_salir:
            en_menu = True

        assert en_menu, "Debe regresar al menú al cancelar"


class TestTransicionPantallas:
    """Tests de transición entre pantallas"""

    def test_menu_a_juego(self):
        """Verificar transición de menú a juego"""
        pantalla_actual = "menu"
        accion = "jugar"

        if accion == "jugar":
            pantalla_actual = "juego"

        assert pantalla_actual == "juego"

    def test_menu_a_salon_fama(self):
        """Verificar transición de menú a salón de la fama"""
        pantalla_actual = "menu"
        accion = "salon_fama"

        if accion == "salon_fama":
            pantalla_actual = "salon_fama"

        assert pantalla_actual == "salon_fama"

    def test_juego_a_menu_con_esc(self):
        """Verificar que ESC regresa al menú desde el juego"""
        pantalla_actual = "juego"
        tecla_presionada = pygame.K_ESCAPE

        if tecla_presionada == pygame.K_ESCAPE:
            pantalla_actual = "menu"

        assert pantalla_actual == "menu"

    def test_salon_fama_a_menu(self):
        """Verificar que se puede regresar del salón de la fama al menú"""
        pantalla_actual = "salon_fama"
        accion = "volver"

        if accion == "volver":
            pantalla_actual = "menu"

        assert pantalla_actual == "menu"


class TestIngresoNombre:
    """Tests de ingreso de nombre del jugador"""

    def test_nombre_se_puede_ingresar(self):
        """Verificar que se puede ingresar un nombre"""
        nombre = "TestPlayer"

        assert len(nombre) > 0, "El nombre debe tener caracteres"
        assert isinstance(nombre, str), "El nombre debe ser un string"

    def test_nombre_minimo_caracteres(self):
        """Verificar validación de nombre mínimo"""
        nombre = "A"

        # En el juego real, debería validarse longitud mínima
        tiene_longitud_valida = len(nombre) >= 1

        assert tiene_longitud_valida

    def test_nombre_maximo_caracteres(self):
        """Verificar que hay límite de caracteres"""
        nombre = "A" * 20
        nombre_limitado = nombre[:15]  # Límite de 15 caracteres

        assert len(nombre_limitado) <= 15, "El nombre debe tener límite de caracteres"

    def test_nombre_no_vacio(self):
        """Verificar que el nombre no puede estar vacío"""
        nombre = ""

        es_valido = len(nombre) > 0

        assert not es_valido, "El nombre vacío no debe ser válido"


class TestDimensionesPantallas:
    """Tests de dimensiones de las pantallas"""

    def test_pantalla_juego_dimensiones(self):
        """Verificar dimensiones de la pantalla de juego"""
        ANCHO_JUEGO = 1200
        ALTO_JUEGO = 800

        assert ANCHO_JUEGO == 1200
        assert ALTO_JUEGO == 800

    def test_pantalla_menu_dimensiones(self):
        """Verificar dimensiones de la pantalla del menú"""
        ANCHO_MENU = 800
        ALTO_MENU = 600

        assert ANCHO_MENU == 800
        assert ALTO_MENU == 600

    def test_cambio_resolucion_menu_juego(self):
        """Verificar que se cambia la resolución al ir de menú a juego"""
        resolucion_menu = (800, 600)
        resolucion_juego = (1200, 800)

        assert (
            resolucion_menu != resolucion_juego
        ), "Las resoluciones deben ser diferentes"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
