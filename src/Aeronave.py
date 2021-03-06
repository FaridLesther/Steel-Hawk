import pygame
import Disparo
from random import randint


class Avion(pygame.sprite.Sprite):

    def __init__(self, posicion):
        # ancho y alto de la magen png
        ancho = 112
        alto = 157
        self.cartucho = []  # lista que contiene los disparos
        self.capasDisparos = 1
        # se carga el sprite del avion
        self.avion = pygame.image.load('Graficos/avion.png')
        self.avion.set_clip(pygame.Rect(0, 0, ancho, alto))
        self.imagen = self.avion.subsurface(self.avion.get_clip())
        self.rect = self.imagen.get_rect()
        self.rect.topleft = posicion
        self.frame = 0
        self.AlabeoIzquierdo = {0: (ancho * 5, 0, ancho, alto)}
        self.AlabeoDerecho = {0: (ancho * 4, 0, ancho, alto)}
        self.acelerar = {0: (ancho, 0, ancho, alto), 1: (
            ancho * 2, 0, ancho, alto), 2: (ancho * 3, 0, ancho, alto)}
        self.frenar = {0: (0, 0, ancho, alto)}
        self.presionarGatillo = False

        self.explosion = []
        for i in range(3):
            self.explosion.append(pygame.image.load(
                'Graficos/explocion/' + str(i) + '.png'))

        self.raton = False

    def cargarDisparo(self, x, y):
        sonidoDisparo = pygame.mixer.Sound("Sonidos/disparo1.wav")
        sonidoDisparo.play()
        disparo = Disparo.Disparo(x, y, 'Graficos/Disparo.png')
        self.cartucho.append(disparo)
        if self.capasDisparos > 3:
            for i in self.cartucho:
                i.velocidad += 1

    def dibujar(self, superficie):
        if self.capasDisparos > 0:
            superficie.blit(self.imagen, self.rect)
            # dibujar los disparos del avion en pantalla
            if len(self.cartucho) > 0:
                for i in self.cartucho:
                    superficie.blit(i.disparo, i.rect)
                    i.trayectoria(False)
                    if i.rect.top < 0:
                        self.cartucho.remove(i)
        else:
            explocion = self.explosion[randint(0, 2)]
            rect = explocion.get_rect()
            rect.topleft = self.rect.center
            rect.top -= 80
            rect.left -= 50
            superficie.blit(explocion, rect)

    def get_frame(self, frame_set):
        self.frame += 1
        if self.frame > (len(frame_set) - 1):
            self.frame = 0
        return frame_set[self.frame]

    def recortar(self, recuadro):
        if type(recuadro) is dict:
            self.avion.set_clip(pygame.Rect(self.get_frame(recuadro)))
        else:
            self.avion.set_clip(pygame.Rect(recuadro))
        return recuadro

    # metodo que actualizara la imagen en distintas posiciones de la pantalla
    def update(self, direccion):
        # si la tecla presionada es la flecha izquierda se le
        # restan 5 unidades a x dando el efecto de movimiento a
        # la izquierda, En la condicion se verifica que el avion
        # este en el limite de la pantalla
        if direccion == 'left' and self.rect.x != -6:
            self.recortar(self.AlabeoIzquierdo)
            self.rect.x -= 5
            if self.rect.x < -2:
                self.rect.x = 0

        # si la tecla presionada es la flecha derecha se le
        # suman 5 unidades a x dando el efecto de movimiento a
        # la derecha, En la condicion se verifica que el avion
        # este en el limite de la pantalla
        if direccion == 'right' and self.rect.x != 854:
            self.recortar(self.AlabeoDerecho)
            self.rect.x += 5
            if self.rect.x > 858:
                self.rect.x = 858

        # si la tecla presionada es la flecha arriba se le
        # restan 5 unidades a y dando el efecto de movimiento
        # hacia arriba, En la condicion se verifica que el avion
        # este en el limite de la pantalla
        if direccion == 'up' and self.rect.y != 3:
            self.recortar(self.acelerar)
            self.rect.y -= 5
            if self.rect.y < 3:
                self.rect.y = 3
        # si la tecla presionada es la flecha abajo se le
        # suman 5 unidades a y dando el efecto de movimiento
        # hacia abajo, En la condicion se verifica que el avion
        # este en el limite de la pantalla
        if direccion == 'down' and self.rect.y != 588:
            self.recortar(self.frenar)
            self.rect.y += 5
            if self.rect.y > 588:
                self.rect.y = 588

        # En este paso se verifica la posicion en la que quedo el avion
        # si quedo en posicion derecha o izquierda se establece en la
        # posicion por defecto
        if direccion == 'stand':
            self.avion.set_clip(pygame.Rect(0, 0, 104, 126))

        # se actualiza la posicion de la imagen
        self.imagen = self.avion.subsurface(self.avion.get_clip())

    def disparar(self):
        if self.presionarGatillo:
            if len(self.cartucho) < self.capasDisparos:
                x, y = self.rect.center
                self.cargarDisparo(x, y - 120)
                if self.capasDisparos > 1:
                    self.cargarDisparo(x + 25, y - 75)
                if self.capasDisparos > 2:
                    self.cargarDisparo(x - 25, y - 75)

    # metodo para manejar los eventos del teclado
    def eventosDelTeclado(self, event):
        if not self.raton and self.capasDisparos > 0:
            # captura los estados de las teclas
            # devuelve 1 si la tecla esta presionada, 0 si la tecla esta sin presionar
            teclas_estado = pygame.key.get_pressed()

            # cuatro direcciones; derecha, izquierda ,arriba, abajo
            if teclas_estado[pygame.K_LEFT] == 1:
                self.update('left')
            if teclas_estado[pygame.K_RIGHT] == 1:
                self.update('right')
            if teclas_estado[pygame.K_UP] == 1:
                self.update('up')
            if teclas_estado[pygame.K_DOWN] == 1:
                self.update('down')

            # boton para cargarDisparo en este caso la letra z
            if teclas_estado[pygame.K_z] == 1:
                self.presionarGatillo = True
                self.disparar()

            # verificacion de las teclas que no estan presionadas para
            # devolver la posicion del avion de acuerdo a ese estado
            if teclas_estado[pygame.K_LEFT] == 0 and teclas_estado[pygame.K_RIGHT] == 0 and teclas_estado[pygame.K_UP] == 0:
                self.update('stand')

            if teclas_estado[pygame.K_z] == 0:
                self.presionarGatillo = False

    def mostrar_vida(self, superficie):  # yop
        fuente = pygame.font.Font(None, 35)
        texto = fuente.render(str(self.capasDisparos), 0, (255, 0, 0))
        superficie.blit(texto, (self.rect.x + 50, self.rect.y - 30))

    def detectar_impacto(self, lista):  # yop
        if self.capasDisparos > 0:
            if len(lista) > 0:
                for enemigo in lista:
                    if enemigo.rect.colliderect(self.rect) and enemigo.vivo:
                        self.capasDisparos -= 1

    def detectar_potenciador(self, potenciadores):  # yop
        if self.capasDisparos < 5 and len(potenciadores) > 0:
            for potenciador in potenciadores:
                if potenciador.rect.colliderect(self.rect):
                    potenciadores.remove(potenciador)
                    self.capasDisparos += 1

    # yop metodo que detecta el impacto de los disparos del enemigo con el avion
    # yop Diferenciar de quien proviene el disparo y respecto a ello eliminar la capa o no
    def detectar_disparo(self, enemigos):
        if self.capasDisparos > 0:
            if len(enemigos) > 0:
                for enemigo in enemigos:
                    for disparo in enemigo.disparos:
                        if disparo.rect.colliderect(self.rect) and enemigo.vivo:
                            self.capasDisparos -= 1
                            enemigo.disparos.remove(disparo)
