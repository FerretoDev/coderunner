jugador = 0

def sumar_puntos(puntos = 10):
    global jugador
    jugador += puntos
    return jugador

if not jugador ==10:
    raise Exception("Error en sumar puntos")
else:
    print("Puntos sumados correctamente")

