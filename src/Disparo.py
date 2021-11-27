import pygame
class Disparo(pygame.sprite.Sprite):
    def __init__(self, coordenada_x, coordenada_y, ruta):
        self.disparo = pygame.image.load(ruta)
        self.rect = self.disparo.get_rect()
        self.velocidad = 15
        self.rect.top = coordenada_y
        self.rect.left = coordenada_x

    def trayectoria(self, enemigo:bool):
        if enemigo:
            self.rect.top += self.velocidad
        else:
            self.rect.top -= self.velocidad

    def trayectoriaDiagonal(self, derecha:bool):
        if derecha:
            self.rect.left += self.velocidad
            self.rect.top += self.velocidad
        else:
            self.rect.left -= self.velocidad
            self.rect.top += self.velocidad
