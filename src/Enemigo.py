import pygame
import abc

class Enemigo(pygame.sprite.Sprite):
    #metodo inicializador
    #argumentos: posicion; recibe la posision a dibujar en pantalla
    #            numAnimaciones; recibe el numero de imagenes que se cargaran
    #            ruta: recibe la ruta en la que se encuentran las imagenes
    def __init__(self, posicion, numAnimaciones:int, ruta:str):
        self.estados = []
        for i in range(1,numAnimaciones + 1):
            self.estados.append(pygame.image.load('Graficos/' + ruta + '/' + str(i) + '.png'))

        self.posImagen = 0
        self.imagen = self.estados[self.posImagen]
        self.rect = self.imagen.get_rect()
        self.rect.topleft = posicion # ancho y alto de la magen png
        self.tiempoEstado = 1
        self.rangoDisparo = 1
        self.disparos = []
        self.explosion = pygame.mixer.Sound("Sonidos/Explosion.wav")
        self.vivo = True

    # metodo que dibuja el objeto en una ventana pasada por el argumento superficie
    def dibujar(self , superficie):
        self.imagen = self.estados[self.posImagen]
        superficie.blit(self.imagen, self.rect)

    #metodo que detecta el impacto de los disparos del avion con el enemigo
    def detImpacto(self , listaDisparos:list):
        if self.vivo:
            if len(listaDisparos) > 0:
                for x in listaDisparos:
                    if x.rect.colliderect(self.rect):
                        self.vida -= 25
                        listaDisparos.remove(x)

    @abc.abstractclassmethod
    def disparar(self, x , y ):
        """metodo para activar los disparos del enemigo"""

    def mostrar_vida(self, superficie):  # crea una fuente para poder mostrar la vida
        return pygame.font.Font(None, 25)
