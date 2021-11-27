import pygame


class Potenciador(pygame.sprite.Sprite):
    def __init__(self, posicion):
        # ancho y alto de la magen png
        ancho = 88
        alto = 89
        self.potenciador = pygame.image.load('Graficos/Pontenciador.png')
        self.potenciador.set_clip(pygame.Rect(0, 0, ancho, alto))
        self.imagen = self.potenciador.subsurface(self.potenciador.get_clip())
        self.rect = self.imagen.get_rect()
        self.rect.topleft = posicion
        self.frame = 0
        self.estados = {0: (ancho, 0, ancho, alto), 1: (ancho * 3, 0, ancho, alto),
                        2: (ancho * 2, 0, ancho, alto), 3: (ancho * 4, 0, ancho, alto),
                        4: (ancho * 5, 0, ancho, alto), 5: (ancho, 0, ancho, alto)}
        self.estadoActual = 0
        self.tiempoEstado = 1


    def dibujar(self, tiempoEstado, superficie,  posAvion):
        superficie.blit(self.imagen, self.rect)
        self.update(tiempoEstado)

        if posAvion.rect.left > self.rect.left > 100:
            self.rect.left -= 4
        elif posAvion.rect.left < self.rect.left < 800:
            self.rect.left += 4

        self.rect.top += 2

    def get_frame(self, frame_set):
        self.frame += 1
        if self.frame > (len(frame_set) - 1):
            self.frame = 0
        return frame_set[self.frame]

    def recortar(self, recuadro):
        if type(recuadro) is dict:
            self.potenciador.set_clip(pygame.Rect(self.get_frame(recuadro)))
        else:
            self.potenciador.set_clip(pygame.Rect(recuadro))
        return recuadro

    #metodo que actualizara la imagen en distintas posiciones de la pantalla
    def update(self, tiempo):
        if self.tiempoEstado < int(tiempo):
            self.estadoActual += 1
            self.tiempoEstado += 2

        if self.estadoActual > 5:
            self.estadoActual = 0

        self.recortar(self.estados[self.estadoActual])

        #se actualiza la posicion de la imagen
        self.imagen = self.potenciador.subsurface(self.potenciador.get_clip())