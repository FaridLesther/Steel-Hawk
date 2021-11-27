import pygame


class MenuPrincipal(pygame.Rect):
    def __init__(self):
        self.jugar = Boton((720/2, 79),'Graficos/Menu/Jugar/')
        self.controles = Boton((720 / 2, self.jugar.rect.top + 121), 'Graficos/Menu/Controles/')
        self.atras = Boton((720 / 2, self.controles.rect.top + 121), 'Graficos/Menu/Atras/')
        self.tecladoMouse = Boton((720/3, 960/2),'Graficos/Menu/BotonOnOff/')

    def dibujar(self, superficie, configuraciones):
        if not(configuraciones):
            self.jugar.dibujar(superficie)
            self.controles.dibujar(superficie)
        else:
            self.atras.dibujar(superficie)
            self.tecladoMouse.imagen = self.tecladoMouse.estados[self.tecladoMouse.posImagen]
            superficie.blit(self.tecladoMouse.imagen, self.tecladoMouse.rect)


class Boton(pygame.sprite.Sprite):
    def __init__(self, posicion, ruta):
        self.estados = []
        for i in range(1, 3):
            self.estados.append(pygame.image.load(ruta+str(i)+'.png'))

        self.posImagen = 0
        self.imagen = self.estados[self.posImagen]
        self.rect = self.imagen.get_rect()
        self.rect.topleft = posicion  # ancho y alto de la magen png
        self.tiempoEstado = 1
        self.rangoDisparo = 1
        self.disparos = []
        self.explosion = pygame.mixer.Sound("Sonidos/Explosion.wav")
        self.vivo = True

    def dibujar(self , superficie):
        raton = pygame.Rect(pygame.mouse.get_pos(), (1,1))
        if self.rect.colliderect(raton):
            self.posImagen = 1
        else:
            self.posImagen = 0

        self.imagen = self.estados[self.posImagen]
        superficie.blit(self.imagen, self.rect)
