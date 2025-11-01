"""
Archivo de configuración de pytest para el proyecto.
Define fixtures globales y configuraciones de los tests.
"""

import os
import sys

import pygame
import pytest

# Agregar el directorio src al path para imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


@pytest.fixture(scope="session", autouse=True)
def inicializar_pygame():
    """Inicializa pygame una vez para toda la sesión de tests"""
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def pantalla_test():
    """Crea una pantalla de pygame para tests"""
    pantalla = pygame.display.set_mode((800, 600))
    yield pantalla


def pytest_configure(config):
    """Configuración personalizada de pytest"""
    config.addinivalue_line("markers", "slow: marca tests que son lentos de ejecutar")
    config.addinivalue_line("markers", "integration: marca tests de integración")
    config.addinivalue_line("markers", "unit: marca tests unitarios")


def pytest_collection_modifyitems(config, items):
    """Modifica la colección de tests para agregar markers automáticos"""
    for item in items:
        # Agregar marker 'unit' a todos los tests por defecto
        if "integration" not in item.keywords:
            item.add_marker(pytest.mark.unit)
