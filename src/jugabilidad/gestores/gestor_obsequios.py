"""
Gestor de obsequios para el juego.

Maneja el ciclo de vida completo de los obsequios:
- Inicialización de timers
- Actualización de timers (vencimiento)
- Recolección de obsequios
- Creación de nuevos obsequios en posiciones válidas
"""

import random

from mundo.obsequio import Obsequio


class GestorObsequios:
    """
    Gestiona el ciclo de vida de los obsequios en el laberinto.

    Responsabilidades:
    - Mantener timers de vida de cada obsequio
    - Hacer que obsequios expiren y reaparezcan
    - Verificar recolección del jugador
    - Crear nuevos obsequios en posiciones válidas
    """

    def __init__(self, laberinto, tiempo_vida_frames: int):
        """
        Inicializa el gestor de obsequios.

        Args:
            laberinto: Instancia del laberinto con obsequios iniciales
            tiempo_vida_frames: Número de frames antes de que expire un obsequio
        """
        self.laberinto = laberinto
        self.tiempo_vida_obsequio = tiempo_vida_frames
        self.obsequios_timers: dict[tuple[int, int], int] = {}
        self._inicializar_timers()

    def _inicializar_timers(self):
        """Crea un timer de vida para cada obsequio inicial del laberinto."""
        for posicion in self.laberinto._obsequios.keys():
            self.obsequios_timers[posicion] = self.tiempo_vida_obsequio

    def actualizar(self):
        """
        Actualiza los timers de todos los obsequios activos.

        Resta 1 frame a cada timer. Si un obsequio expira (timer <= 0),
        lo elimina y crea uno nuevo en otra posición.
        """
        obsequios_expirados = []
        for posicion, tiempo_restante in self.obsequios_timers.items():
            self.obsequios_timers[posicion] = tiempo_restante - 1
            if self.obsequios_timers[posicion] <= 0:
                obsequios_expirados.append(posicion)

        for posicion in obsequios_expirados:
            if posicion in self.laberinto._obsequios:
                valor = self.laberinto._obsequios[posicion].valor
                del self.laberinto._obsequios[posicion]
                del self.obsequios_timers[posicion]
                self.crear_nuevo_obsequio(valor)

    def verificar_recoleccion(self, posicion_celda: tuple[int, int]) -> int:
        """
        Verifica si hay un obsequio en la celda especificada y lo recolecta.

        Args:
            posicion_celda: Tupla (columna, fila) de la celda a verificar

        Returns:
            Puntos obtenidos (0 si no había obsequio)
        """
        puntos = self.laberinto.recolectar_obsequio(posicion_celda)
        if puntos > 0:
            # Eliminar timer y crear nuevo obsequio
            if posicion_celda in self.obsequios_timers:
                del self.obsequios_timers[posicion_celda]
            self.crear_nuevo_obsequio()
        return puntos

    def crear_nuevo_obsequio(self, valor: int = 10):
        """
        Coloca un obsequio en una celda libre aleatoria.

        Busca celdas que sean:
        - Pasillos válidos (verificados con _pasillos del laberinto)
        - Sin obsequios existentes
        - No sean posiciones de spawn

        Args:
            valor: Valor en puntos del obsequio (por defecto 10)
        """
        # Usar directamente la lista de pasillos procesados del laberinto
        # para garantizar que solo se elijan celdas realmente transitables
        posiciones_validas = []

        for posicion in self.laberinto._pasillos:
            # Verificar que:
            # 1. No haya ya un obsequio en esa posición
            # 2. No sea la posición de spawn del jugador
            # 3. No sea la posición de spawn del enemigo
            if (
                posicion not in self.laberinto._obsequios
                and posicion != self.laberinto.jugador_inicio
                and posicion != self.laberinto.computadora_inicio
            ):
                posiciones_validas.append(posicion)

        if posiciones_validas:
            nueva_posicion = random.choice(posiciones_validas)
            self.laberinto._obsequios[nueva_posicion] = Obsequio(nueva_posicion, valor)
            self.obsequios_timers[nueva_posicion] = self.tiempo_vida_obsequio

    def obtener_cantidad_activos(self) -> int:
        """Retorna la cantidad de obsequios actualmente en el laberinto."""
        return len(self.laberinto._obsequios)
