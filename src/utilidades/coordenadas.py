"""
Utilidades para conversión entre coordenadas de píxeles y celdas del laberinto.

Este módulo centraliza las funciones de conversión de coordenadas que se usan
en diferentes partes del juego (Computadora, PantallaJuego, etc.).
"""


class ConversorCoordenadas:
    """
    Clase auxiliar para convertir entre coordenadas de píxeles y celdas del laberinto.

    Proporciona métodos estáticos para:
    - Convertir coordenadas de píxeles a índices de celda (fila, columna)
    - Convertir índices de celda al centro en píxeles
    """

    @staticmethod
    def pixel_a_celda(
        x_px: int, y_px: int, tam_celda: int, offset_x: int = 0, offset_y: int = 0
    ) -> tuple[int, int]:
        """
        Convierte coordenadas de píxeles a índices de celda (fila, columna).

        Args:
            x_px: Coordenada X en píxeles
            y_px: Coordenada Y en píxeles
            tam_celda: Tamaño de cada celda en píxeles
            offset_x: Desplazamiento horizontal del laberinto (por defecto 0)
            offset_y: Desplazamiento vertical del laberinto (por defecto 0)

        Returns:
            Tupla (fila, columna) con los índices de la celda

        Example:
            >>> ConversorCoordenadas.pixel_a_celda(100, 200, 32, 20, 40)
            (5, 2)  # Fila 5, Columna 2
        """
        x_rel = x_px - offset_x  # Ajustar por offset de centrado
        y_rel = y_px - offset_y
        col = max(0, x_rel // tam_celda)
        fila = max(0, y_rel // tam_celda)
        return int(fila), int(col)

    @staticmethod
    def celda_a_pixel_centro(
        fila: int, col: int, tam_celda: int, offset_x: int = 0, offset_y: int = 0
    ) -> tuple[int, int]:
        """
        Convierte índices de celda (fila, columna) a píxeles del centro de la celda.

        Args:
            fila: Índice de fila en el laberinto
            col: Índice de columna en el laberinto
            tam_celda: Tamaño de cada celda en píxeles
            offset_x: Desplazamiento horizontal del laberinto (por defecto 0)
            offset_y: Desplazamiento vertical del laberinto (por defecto 0)

        Returns:
            Tupla (x, y) con las coordenadas del centro en píxeles

        Example:
            >>> ConversorCoordenadas.celda_a_pixel_centro(5, 2, 32, 20, 40)
            (100, 200)  # Centro de la celda en píxeles
        """
        cx = col * tam_celda + tam_celda // 2 + offset_x
        cy = fila * tam_celda + tam_celda // 2 + offset_y
        return cx, cy

    @staticmethod
    def esta_en_celda(
        x_px: int,
        y_px: int,
        fila: int,
        col: int,
        tam_celda: int,
        offset_x: int = 0,
        offset_y: int = 0,
    ) -> bool:
        """
        Verifica si unas coordenadas en píxeles están dentro de una celda específica.

        Args:
            x_px: Coordenada X en píxeles
            y_px: Coordenada Y en píxeles
            fila: Índice de fila de la celda a verificar
            col: Índice de columna de la celda a verificar
            tam_celda: Tamaño de cada celda en píxeles
            offset_x: Desplazamiento horizontal del laberinto (por defecto 0)
            offset_y: Desplazamiento vertical del laberinto (por defecto 0)

        Returns:
            True si las coordenadas están en la celda, False en caso contrario

        Example:
            >>> ConversorCoordenadas.esta_en_celda(100, 200, 5, 2, 32, 20, 40)
            True
        """
        f, c = ConversorCoordenadas.pixel_a_celda(
            x_px, y_px, tam_celda, offset_x, offset_y
        )
        return f == fila and c == col
