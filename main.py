from random import randint
import pygame
import Aeronave
from Torreta import Torreta
from Helicoptero import Helicoptero
from MenuPrincipal import MenuPrincipal
from Potenciador import Potenciador

# Inicializa todos los modulos de pygame para poder utilizarlos
pygame.init()

ancho = 960
alto = 720

# creacion de una ventana
ventana = pygame.display.set_mode((ancho, alto))
# Nombre de la etiqueta de la ventana
pygame.display.set_caption("Steel Hawk proyecto de POO")
clock = pygame.time.Clock()
menu = MenuPrincipal()

fondo = pygame.image.load("Graficos/Fondo.gif")
fondoRect = fondo.get_rect()
fondoRect.topleft = (0, -16920)  # 17644

avion = Aeronave.Avion((ancho / 2.5, alto / 1.3))

potenciadores = []
listaDeTorretas = []
listaDeHelicopteros = []

pygame.mixer.music.load("Sonidos/fondo.mp3")  # musica de fondo

# Ciclo para mostrar la ventana
# se ejecutara hasta que la variable booleana salir sea verdadera
salir = False
play = False
configuracion = False
mauseControl = False
ventana.fill(pygame.Color('gray'))


def nivel1():
    fondoRect.topleft = (0, -16920)
    avion.capasDisparos = 1
    n = 0
    for i in range(4):
        n -= 50
        potenciadores.append(Potenciador((ancho/2.5, n)))
        n -= 3100
    n = 0
    for i in range(16):
        n -= 300
        listaDeTorretas.append(Torreta((ancho/4, n), 9, "torreta"))
        n -= 600
        listaDeTorretas.append(Torreta((ancho/1.5, n), 9, "torreta"))
        n -= 15
        listaDeTorretas.append(Torreta((ancho/5, n), 9, "torreta"))

    n = 0
    for i in range(5):
        n -= 3300
        listaDeHelicopteros.append(Helicoptero(
            (ancho / 2, n), 7, "helicoptero"))
    n = 0


def reiniciarObjetos():
    potenciadores.clear()
    listaDeTorretas.clear()
    listaDeHelicopteros.clear()
    ventana.fill(pygame.Color('gray'))


nivel1()
while not salir:
    for event in pygame.event.get():
        if not play:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect(pygame.mouse.get_pos(), (1, 1)).colliderect(menu.jugar):
                    play = True
                    # reproduccion de la musica de fondo
                    pygame.mixer.music.play(4)
                if pygame.Rect(pygame.mouse.get_pos(), (1, 1)).colliderect(menu.controles):
                    configuracion = True
                if pygame.Rect(pygame.mouse.get_pos(), (1, 1)).colliderect(menu.atras):
                    configuracion = False
                if pygame.Rect(pygame.mouse.get_pos(), (1, 1)).colliderect(menu.tecladoMouse):
                    if not mauseControl:
                        mauseControl = True
                    else:
                        mauseControl = False
                    if mauseControl:
                        avion.raton = True
                        menu.tecladoMouse.posImagen = 1
                    else:
                        avion.raton = False
                        menu.tecladoMouse.posImagen = 0
                ventana.fill(pygame.Color('gray'))

        # Verifica si se presiona el boton de cerrar la ventana, en caso verdadero
        # hace verdadera la variable booleana salir y termina el ciclo
        if event.type == pygame.QUIT:
            salir = True

    if not play:
        menu.dibujar(ventana, configuracion)
    else:
        # Si el avion se queda sin disparos significa que se perdio el juego
        if avion.capasDisparos <= 0:
            key_states = pygame.key.get_pressed()
            pygame.mixer.music.stop()
            ventana.blit(pygame.font.Font(None, 75).render(
                "Has perdido", 0, (0, 0, 0)), (ancho/3, alto/3))
            ventana.blit(pygame.font.Font(None, 75).render(
                "Presiona enter para", 0, (0, 0, 0)), (ancho / 4, alto / 2))
            ventana.blit(pygame.font.Font(None, 75).render(
                "volver al menu", 0, (0, 0, 0)), (ancho / 3, alto/1.5))

            if key_states[pygame.K_RETURN] == 1:
                reiniciarObjetos()
                avion = Aeronave.Avion((ancho / 2.5, alto / 1.3))
                nivel1()
                play = False

        elif avion.capasDisparos > 0 >= len(listaDeTorretas):
            key_states = pygame.key.get_pressed()
            pygame.mixer.music.stop()
            ventana.blit(pygame.font.Font(None, 75).render(
                "Has ganado", 0, (0, 0, 0)), (ancho / 3, alto / 3))
            ventana.blit(pygame.font.Font(None, 75).render(
                "Presiona enter para", 0, (0, 0, 0)), (ancho / 4, alto / 2))
            ventana.blit(pygame.font.Font(None, 75).render(
                "volver al menu", 0, (0, 0, 0)), (ancho / 3, alto / 1.5))
            if key_states[pygame.K_RETURN] == 1:
                reiniciarObjetos()
                avion = Aeronave.Avion((ancho / 2.5, alto / 1.3))
                nivel1()
                play = False
        else:
            tiempoEstado = pygame.time.get_ticks() / 50
            # Metodo para rellenar la ventana con un color
            ventana.fill(pygame.Color(70, 80, 150))
            ventana.blit(fondo, fondoRect)
            fondoRect.top += 1

            if len(potenciadores) > 0:
                potenciadores[0].dibujar(tiempoEstado, ventana, avion)

            if len(listaDeTorretas) > 0:
                for x in listaDeTorretas:
                    x.comportamiento(tiempoEstado, ventana)
                    if x.rect.top >= -100:
                        x.dibujar(ventana)
                        # yop muestra la vida del enemigo correspondiente
                        x.mostrar_vida(ventana)
                        if not x.vivo or x.rect.top > 700:
                            if randint(0, 100) == 25:
                                listaDeTorretas.remove(x)
                        x.detImpacto(avion.cartucho)

            if len(listaDeHelicopteros) > 0:
                for x in listaDeHelicopteros:
                    x.comportamiento(tiempoEstado, ventana, avion.rect.left)
                    if x.rect.top >= -100:
                        x.dibujar(ventana)
                        # yop muestra la vida del enemigo correspondiente
                        x.mostrar_vida(ventana)
                        if not x.vivo or x.rect.top > 700:
                            if randint(0, 100) == 25:
                                listaDeHelicopteros.remove(x)
                        x.detImpacto(avion.cartucho)

            avion.detectar_disparo(listaDeHelicopteros)  # yop
            avion.detectar_disparo(listaDeTorretas)  # yop
            avion.detectar_potenciador(potenciadores)
            avion.detectar_impacto(listaDeTorretas)
            avion.dibujar(ventana)  # metodo para dibujar el avion en pantalla
            avion.mostrar_vida(ventana)  # yop Muestra la vida del avion
            # disparar se activa solo si el gatillo esta presionado, ver este metodo en la clase aeronave
            avion.disparar()
            # llamada al metodo para manejar los eventos del teclado del avion
            avion.eventosDelTeclado(event)

    pygame.display.flip()
    clock.tick(90)  # para regular cuantos frames se ejecutan cada segundo

pygame.quit()
