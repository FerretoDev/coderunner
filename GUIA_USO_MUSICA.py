#!/usr/bin/env python3
"""
Guía rápida de uso del Sistema de Música en CodeRunner

Este archivo muestra ejemplos de cómo usar el sistema de música
en diferentes partes del juego.
"""

# ============================================================================
# EJEMPLO 1: Uso básico en PantallaJuego (ya implementado)
# ============================================================================

"""
En el __init__ de PantallaJuego:

    # Sistema de sonido (singleton) y reproducir música de fondo
    self.sistema_sonido = SistemaSonido()
    self.sistema_sonido.reproducir_musica_fondo()
"""

# ============================================================================
# EJEMPLO 2: Pausar/Reanudar música en eventos (ya implementado)
# ============================================================================

"""
En manejar_eventos():

    if evento.key == pygame.K_p:
        self.pausado = not self.pausado
        # Pausar/reanudar música según el estado
        if self.pausado:
            self.sistema_sonido.pausar_musica()
        else:
            self.sistema_sonido.reanudar_musica()
"""

# ============================================================================
# EJEMPLO 3: Efectos de sonido en eventos del juego (ya implementado)
# ============================================================================

"""
Cuando el jugador es capturado:

    def _verificar_captura(self):
        if distancia < radio_captura:
            # Reproducir sonido de captura
            self.sistema_sonido.reproducir_captura()
            self.jugador.perder_vida()
            ...

Cuando se recolecta un obsequio:

    def _verificar_recoleccion_obsequios(self):
        puntos = self.laberinto.recolectar_obsequio(posicion_celda)
        if puntos > 0:
            # Reproducir sonido de recolección
            self.sistema_sonido.reproducir_obsequio()
            self.jugador.sumar_puntos(puntos)
            ...
"""

# ============================================================================
# EJEMPLO 4: Detener música al finalizar (ya implementado)
# ============================================================================

"""
En el método ejecutar() al salir:

    def ejecutar(self):
        ejecutando = True
        while ejecutando:
            ...
            if resultado == "salir":
                ejecutando = False
        
        # Detener la música al salir
        self.sistema_sonido.detener_musica()
"""

# ============================================================================
# EJEMPLO 5: Control manual de volumen
# ============================================================================

"""
Si quieres ajustar el volumen dinámicamente:

    # Bajar volumen cuando el jugador tiene pocas vidas
    if self.jugador.vidas <= 1:
        self.sistema_sonido.ajustar_volumen_musica(0.2)
    else:
        self.sistema_sonido.ajustar_volumen_musica(0.4)
"""

# ============================================================================
# EJEMPLO 6: Agregar efectos de sonido reales (opcional)
# ============================================================================

"""
Para agregar archivos de sonido reales, modificar SistemaSonido.__init__:

    def __init__(self):
        ...
        # Cargar efectos de sonido
        try:
            self.sonido_movimiento = pygame.mixer.Sound("src/data/movimiento.wav")
            self.sonido_captura = pygame.mixer.Sound("src/data/captura.wav")
            self.sonido_obsequio = pygame.mixer.Sound("src/data/obsequio.wav")
            
            # Ajustar volumen de efectos
            self.sonido_movimiento.set_volume(self.volumen_efectos)
            self.sonido_captura.set_volume(self.volumen_efectos)
            self.sonido_obsequio.set_volume(self.volumen_efectos)
        except pygame.error:
            print("No se pudieron cargar algunos efectos de sonido")

Y luego en los métodos de reproducción:

    def reproducir_movimiento(self):
        if self.sonidos_activos and self.sonido_movimiento:
            self.sonido_movimiento.play()
    
    def reproducir_captura(self):
        if self.sonidos_activos and self.sonido_captura:
            self.sonido_captura.play()
    
    def reproducir_obsequio(self):
        if self.sonidos_activos and self.sonido_obsequio:
            self.sonido_obsequio.play()
"""

# ============================================================================
# EJEMPLO 7: Usar el sistema desde cualquier parte del código
# ============================================================================

"""
Gracias al patrón singleton, puedes acceder al sistema desde cualquier lugar:

    from models.sistema_sonido import SistemaSonido
    
    # Obtener la instancia (siempre será la misma)
    sistema = SistemaSonido()
    
    # Usar cualquier método
    sistema.pausar_musica()
    sistema.ajustar_volumen_musica(0.5)
"""

# ============================================================================
# CONTROLES PARA EL USUARIO
# ============================================================================

"""
Controles disponibles en el juego:

    P - Pausar juego (también pausa la música)
    U - Activar/Desactivar música de fondo
    ESC - Salir (detiene la música automáticamente)
    
Estos se muestran en el HUD durante el juego.
"""

# ============================================================================
# NOTAS TÉCNICAS
# ============================================================================

"""
- El mixer se inicializa a 44.1kHz, 16-bit, estéreo
- La música se reproduce en loop infinito (-1)
- El volumen por defecto de música es 0.4 (40%)
- El volumen por defecto de efectos es 0.6 (60%)
- Si el mixer no está disponible, el sistema se desactiva silenciosamente
- El archivo de música debe estar en: src/data/MusicaPerrona.mp3
"""

print(__doc__)
