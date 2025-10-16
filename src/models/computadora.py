import math

import pygame

from .personaje import Personaje


class Computadora(Personaje):
    """Enemiga que persigue al jugador con IA mejorada"""

    def __init__(self, x: int, y: int, radio: int = 10, velocidad: float = 2.5):
        super().__init__(x, y, radio, velocidad)
        self.color = (255, 50, 50)
        self.computadora_principal = pygame.Rect(x, y, radio * 2, radio * 2)

    def perseguir(self, jugador, laberinto=None):
        """
        Persigue al jugador con IA mejorada que evita obstáculos
        """
        # Obtener posición del jugador
        objetivo_x = jugador.jugador_principal.centerx
        objetivo_y = jugador.jugador_principal.centery

        # Posición actual de la computadora
        actual_x = self.computadora_principal.centerx
        actual_y = self.computadora_principal.centery

        # Calcular diferencia
        dx = objetivo_x - actual_x
        dy = objetivo_y - actual_y

        # Calcular distancia total
        distancia = (dx**2 + dy**2) ** 0.5

        if distancia > 0:
            # Normalizar el movimiento
            velocidad_x = (dx / distancia) * self.velocidad
            velocidad_y = (dy / distancia) * self.velocidad

            # Intentar movimiento directo primero
            nueva_x = self.computadora_principal.x + velocidad_x
            nueva_y = self.computadora_principal.y + velocidad_y

            # Crear rectángulo temporal para probar colisiones
            temp_rect = pygame.Rect(
                nueva_x,
                nueva_y,
                self.computadora_principal.width,
                self.computadora_principal.height,
            )

            # Verificar si hay colisión con la nueva posición
            hay_colision = False
            for muro in getattr(self, "_muros_cache", []):
                if temp_rect.colliderect(muro):
                    hay_colision = True
                    break

            if not hay_colision:
                # Movimiento directo exitoso
                self._aplicar_movimiento(nueva_x, nueva_y)
            else:
                # Hay colisión, intentar movimientos alternativos
                self._mover_rodeando_obstaculos(velocidad_x, velocidad_y)

    def _aplicar_movimiento(self, nueva_x, nueva_y):
        """Aplica el movimiento validando límites"""
        # Validar límites del mapa
        limite_x = (20 * 32) - self.radio * 2
        limite_y = (15 * 32) - self.radio * 2

        # Mantener dentro de los límites
        nueva_x = max(0, min(nueva_x, limite_x))
        nueva_y = max(0, min(nueva_y, limite_y))

        # Aplicar el movimiento
        self.computadora_principal.x = nueva_x
        self.computadora_principal.y = nueva_y

        # Actualizar coordenadas internas
        self.x = self.computadora_principal.x
        self.y = self.computadora_principal.y

    def _mover_rodeando_obstaculos(self, velocidad_x, velocidad_y):
        """Intenta movimientos alternativos para rodear obstáculos"""
        movimientos_alternativos = [
            # Intentar solo movimiento horizontal
            (velocidad_x, 0),
            # Intentar solo movimiento vertical
            (0, velocidad_y),
            # Intentar movimientos diagonales
            (velocidad_x * 0.7, velocidad_y * 0.7),
            (velocidad_x * 0.7, -velocidad_y * 0.7),
            (-velocidad_x * 0.7, velocidad_y * 0.7),
            # Movimiento perpendicular
            (-velocidad_y, velocidad_x),
            (velocidad_y, -velocidad_x),
        ]

        for vel_x, vel_y in movimientos_alternativos:
            nueva_x = self.computadora_principal.x + vel_x
            nueva_y = self.computadora_principal.y + vel_y

            # Crear rectángulo temporal
            temp_rect = pygame.Rect(
                nueva_x,
                nueva_y,
                self.computadora_principal.width,
                self.computadora_principal.height,
            )

            # Verificar si este movimiento es válido
            hay_colision = False
            for muro in getattr(self, "_muros_cache", []):
                if temp_rect.colliderect(muro):
                    hay_colision = True
                    break

            if not hay_colision:
                # Movimiento exitoso
                self._aplicar_movimiento(nueva_x, nueva_y)
                return

        # Si ningún movimiento funciona, quedarse quieto
        pass

    def actualizar_muros_cache(self, muros):
        """Actualiza el cache de muros para optimizar colisiones"""
        self._muros_cache = muros

    def colisiona_con_muros(self, muros):
        """Método legacy - ahora la lógica está en perseguir()"""
        # Actualizar cache de muros
        self.actualizar_muros_cache(muros)
        return False  # Ya no necesitamos hacer nada aquí

    def dibujar_computadora_principal(self, screen):
        """Dibuja a la computadora con efecto de peligro dinámico"""
        centro = self.computadora_principal.center

        # Efecto pulsante basado en frame count
        frame_count = getattr(self, "_frame_count", 0)
        self._frame_count = frame_count + 1

        # Crear efecto de pulsación
        pulso = abs(math.sin(frame_count * 0.2)) * 3
        radio_pulso = self.radio + pulso

        # Color que varía con la pulsación
        intensidad = int(200 + 55 * abs(math.sin(frame_count * 0.15)))
        color_principal = (intensidad, 50, 50)

        # Dibujar círculo principal con pulsación
        pygame.draw.circle(screen, color_principal, centro, int(radio_pulso))

        # Borde blanco
        pygame.draw.circle(screen, (255, 255, 255), centro, int(radio_pulso), 2)

        # Centro más oscuro para definir mejor la forma
        pygame.draw.circle(screen, (180, 30, 30), centro, int(self.radio * 0.6))

        # Pequeños "ojos" o puntos brillantes para hacerla más visible
        ojo_offset = 4
        pygame.draw.circle(
            screen, (255, 255, 255), (centro[0] - ojo_offset, centro[1] - 2), 2
        )
        pygame.draw.circle(
            screen, (255, 255, 255), (centro[0] + ojo_offset, centro[1] - 2), 2
        )

    def mover(self, direccion: str) -> None:
        """Movimiento simple (no usado en persecución)"""
        paso = self.velocidad
        if direccion == "arriba":
            self.computadora_principal.y -= paso
        elif direccion == "abajo":
            self.computadora_principal.y += paso
        elif direccion == "izquierda":
            self.computadora_principal.x -= paso
        elif direccion == "derecha":
            self.computadora_principal.x += paso

        self.x = self.computadora_principal.x
        self.y = self.computadora_principal.y
