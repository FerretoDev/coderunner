import os

import pygame

from game.interfaz import Interfaz
from game.juego import Juego


def listar_laberintos():
    """Lista todos los laberintos disponibles"""
    directorio = "src/data"
    laberintos = []

    if os.path.exists(directorio):
        for archivo in os.listdir(directorio):
            if archivo.endswith(".json") and archivo != "salon_fama.json":
                laberintos.append(archivo)

    return laberintos


def main():
    # Inicializar Pygame
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("CodeRunner")

    # Crear interfaz
    interfaz = Interfaz(screen)

    # Mostrar menú principal
    opcion = interfaz.mostrar_menu()

    if opcion == 1:  # Iniciar Juego
        print("\n🎮 Iniciando juego...")
        nombre = input("Ingresa tu nombre: ")

        # Mostrar laberintos disponibles
        laberintos = listar_laberintos()
        print("\n📂 Laberintos disponibles:")
        for i, lab in enumerate(laberintos, 1):
            print(f"  {i}. {lab}")

        seleccion = input(
            f"\nSelecciona un laberinto (1-{len(laberintos)}) [1]: "
        ).strip()

        if seleccion == "" or not seleccion.isdigit():
            archivo_lab = f"src/data/{laberintos[0]}"
        else:
            idx = int(seleccion) - 1
            if 0 <= idx < len(laberintos):
                archivo_lab = f"src/data/{laberintos[idx]}"
            else:
                archivo_lab = f"src/data/{laberintos[0]}"

        print(f"✅ Cargando: {archivo_lab}\n")

        juego = Juego()
        juego.iniciar(nombre, screen, archivo_lab)

    elif opcion == 2:  # Salón de la Fama
        from models.salon_fama import SalonFama

        salon = SalonFama()
        interfaz.mostrar_salon_fama(salon)

    elif opcion == 3:  # Administración
        print("\n🔐 Panel de Administración")
        clave = input("Ingresa la clave: ")

        from models.administrador import Administrador

        admin = Administrador()

        if admin.autenticar(clave):
            print("✅ Acceso concedido")

            # Mostrar opciones de admin
            print("\n1. Listar laberintos")
            print("2. Reiniciar Salón de la Fama")
            print("3. Volver")

            opcion_admin = input("\nSelecciona una opción: ")

            if opcion_admin == "1":
                laberintos = admin.listar_laberintos()
                print(f"\n📂 Laberintos encontrados: {len(laberintos)}")
                for lab in laberintos:
                    print(f"  - {lab}")

            elif opcion_admin == "2":
                from models.salon_fama import SalonFama

                salon = SalonFama()
                confirmacion = input("¿Reiniciar Salón de la Fama? (s/n): ")
                if confirmacion.lower() == "s":
                    admin.reiniciar_salon_fama(salon)
        else:
            print("❌ Clave incorrecta")

    # Cerrar Pygame
    pygame.quit()


if __name__ == "__main__":
    main()
