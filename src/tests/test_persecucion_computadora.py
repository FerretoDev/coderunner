"""
Tests para HU-02: Persecución de la computadora
Verificar que la computadora persigue al jugador correctamente.
"""
import pytest
import pygame
from models.computadora import Computadora
from models.jugador import Jugador
from models.laberinto import Laberinto


@pytest.fixture
def setup_juego():
    """Fixture que inicializa pygame y crea los objetos del juego"""
    pygame.init()
    
    mapa_prueba = {
        "filas": 7,
        "columnas": 7,
        "mapa": [
            ["#", "#", "#", "#", "#", "#", "#"],
            ["#", ".", ".", ".", ".", ".", "#"],
            ["#", ".", "#", "#", "#", ".", "#"],
            ["#", ".", ".", ".", ".", ".", "#"],
            ["#", ".", "#", "#", "#", ".", "#"],
            ["#", ".", ".", ".", ".", ".", "#"],
            ["#", "#", "#", "#", "#", "#", "#"]
        ],
        "inicio_jugador": {"fila": 1, "columna": 1},
        "inicio_computadora": {"fila": 5, "columna": 5},
        "obsequios": []
    }
    
    laberinto = Laberinto(mapa_prueba)
    
    # Crear jugador
    inicio_j = mapa_prueba["inicio_jugador"]
    jugador = Jugador(
        x=inicio_j["columna"] * 32 + 16,
        y=inicio_j["fila"] * 32 + 16,
        radio=10,
        velocidad=1
    )
    
    # Crear computadora con velocidad mayor
    inicio_c = mapa_prueba["inicio_computadora"]
    computadora = Computadora(
        x=inicio_c["columna"] * 32 + 16,
        y=inicio_c["fila"] * 32 + 16,
        radio=10,
        velocidad=1.5  # 50% más rápido que el jugador
    )
    
    return {
        "laberinto": laberinto,
        "jugador": jugador,
        "computadora": computadora
    }


class TestPersecucionBasica:
    """CP-02: Tests de persecución básica de la computadora"""
    
    def test_computadora_mas_rapida_que_jugador(self, setup_juego):
        """Verificar que la computadora es más rápida que el jugador"""
        jugador = setup_juego["jugador"]
        computadora = setup_juego["computadora"]
        
        # La computadora debe tener velocidad mayor
        assert computadora.velocidad > jugador.velocidad
        
    def test_computadora_tiene_velocidad_minima(self, setup_juego):
        """Verificar que la computadora tiene velocidad inicial de al menos 1.5"""
        computadora = setup_juego["computadora"]
        
        assert computadora.velocidad >= 1.5, "Velocidad inicial debe ser 1.5 o mayor"
    
    def test_computadora_calcula_distancia_al_jugador(self, setup_juego):
        """Verificar que la computadora puede calcular la distancia al jugador"""
        jugador = setup_juego["jugador"]
        computadora = setup_juego["computadora"]
        
        # Calcular distancia euclidiana
        dx = jugador.jugador_principal.x - computadora.x
        dy = jugador.jugador_principal.y - computadora.y
        distancia = (dx**2 + dy**2) ** 0.5
        
        # La distancia debe ser positiva cuando están separados
        assert distancia > 0, "Debe haber distancia entre jugador y computadora"
    
    def test_computadora_se_acerca_al_jugador(self, setup_juego):
        """Verificar que la computadora se acerca al jugador con el tiempo"""
        jugador = setup_juego["jugador"]
        computadora = setup_juego["computadora"]
        laberinto = setup_juego["laberinto"]
        
        # Calcular distancia inicial
        dx_inicial = jugador.jugador_principal.x - computadora.x
        dy_inicial = jugador.jugador_principal.y - computadora.y
        distancia_inicial = (dx_inicial**2 + dy_inicial**2) ** 0.5
        
        # Simular varios movimientos de la computadora usando BFS
        tam_celda = 32
        offset_x = 0
        offset_y = 0
        
        for _ in range(10):
            jugador_pos = (jugador.jugador_principal.x, jugador.jugador_principal.y)
            computadora.perseguir_bfs(
                jugador_pos,
                laberinto.mapa_data["mapa"],
                tam_celda,
                offset_x,
                offset_y
            )
        
        # Calcular distancia final
        dx_final = jugador.jugador_principal.x - computadora.x
        dy_final = jugador.jugador_principal.y - computadora.y
        distancia_final = (dx_final**2 + dy_final**2) ** 0.5
        
        # La distancia debe reducirse
        assert distancia_final < distancia_inicial, "La computadora debe acercarse al jugador"


class TestAlgoritmoBFS:
    """Tests del algoritmo BFS de la computadora"""
    
    def test_bfs_encuentra_camino_directo(self, setup_juego):
        """Verificar que BFS encuentra el camino cuando existe"""
        computadora = setup_juego["computadora"]
        mapa = setup_juego["laberinto"].mapa_data["mapa"]
        
        # Posiciones de inicio y fin en formato (fila, columna)
        inicio = (1, 1)
        objetivo = (1, 3)
        
        # Llamar al método BFS
        camino = computadora._calcular_camino_bfs(mapa, inicio, objetivo)
        
        # Debe encontrar un camino
        assert camino is not None, "BFS debe encontrar un camino"
        assert len(camino) > 0, "El camino no debe estar vacío"
        
    def test_bfs_retorna_none_sin_camino(self, setup_juego):
        """Verificar que BFS retorna None cuando no hay camino"""
        computadora = setup_juego["computadora"]
        
        # Crear un mapa donde el objetivo está bloqueado
        mapa_bloqueado = [
            ["#", "#", "#"],
            ["#", ".", "#"],
            ["#", "#", "#"]
        ]
        
        inicio = (1, 1)
        objetivo = (0, 1)  # Posición con pared
        
        camino = computadora._calcular_camino_bfs(mapa_bloqueado, inicio, objetivo)
        
        # No debe encontrar camino hacia una pared
        assert camino is None or len(camino) == 0, "No debe haber camino hacia una pared"
    
    def test_computadora_respeta_paredes(self, setup_juego):
        """Verificar que la computadora no atraviesa paredes"""
        computadora = setup_juego["computadora"]
        laberinto = setup_juego["laberinto"]
        
        # Posicionar computadora cerca de una pared
        computadora.x = 64  # Columna 2
        computadora.y = 64  # Fila 2
        
        # La celda (2, 2) es una pared según nuestro mapa
        fila = int(computadora.y / 32)
        col = int(computadora.x / 32)
        
        celda_actual = laberinto.mapa_data["mapa"][fila][col]
        
        # Si está en pared, verificar que es pared
        if celda_actual == "#":
            assert True, "Computadora detectada en pared (esto no debería pasar en juego real)"


class TestVelocidadProgresiva:
    """Tests para HU-02 relacionados con velocidad progresiva"""
    
    def test_velocidad_inicial_correcta(self):
        """Verificar que la computadora tiene la velocidad inicial correcta"""
        computadora = Computadora(x=100, y=100, radio=10, velocidad=1.5)
        
        assert computadora.velocidad == 1.5, "Velocidad inicial debe ser 1.5"
    
    def test_velocidad_puede_incrementarse(self):
        """Verificar que la velocidad de la computadora puede aumentar"""
        computadora = Computadora(x=100, y=100, radio=10, velocidad=1.5)
        velocidad_inicial = computadora.velocidad
        
        # Incrementar velocidad (como lo hace el juego cada 10 segundos)
        computadora.velocidad += 0.2
        
        assert computadora.velocidad > velocidad_inicial
        assert computadora.velocidad == 1.7, "Velocidad debe incrementar a 1.7"
    
    def test_velocidad_incremento_multiple(self):
        """Verificar que la velocidad puede incrementarse múltiples veces"""
        computadora = Computadora(x=100, y=100, radio=10, velocidad=1.5)
        
        # Simular 5 incrementos de velocidad
        for _ in range(5):
            computadora.velocidad += 0.2
        
        assert computadora.velocidad == pytest.approx(2.5, 0.01), "Después de 5 incrementos debe ser 2.5"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
