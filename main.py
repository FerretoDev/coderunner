class Jugador:
    def __init__(self, nombre, posicion):
        self.nombre = nombre
        self.posicion = posicion       #primera prueba de cambio de Paulo

    def mover(self, nueva_posicion):
        self.posicion = nueva_posicion
        print(f"{self.nombre} se ha movido a la posición {self.posicion}")
        
        
def saludar():
    print('Hola')
    
