import Enemigo
import Disparo
from random import randint


class Torreta(Enemigo.Enemigo):
    def __init__(self, posicion, numAnimaciones: int, ruta: str):
        super().__init__(posicion, numAnimaciones, ruta)
        self.vida = 200

    def disparar(self, x, y):
        disparo = Disparo.Disparo(x - 10, y - 50, "Graficos/disparo2.png")
        self.disparos.append(disparo)

    def comportamiento(self, tiempoEstado, superficie):
        self.rect.top += 1
        if self.vivo:
            if self.tiempoEstado <= int(tiempoEstado):
                self.posImagen += 1
                self.tiempoEstado += 1

                if self.posImagen > len(self.estados) - 4:
                    self.posImagen = 0

                if self.vida <= 0:
                    self.vivo = False
                    self.explosion.play()

            if randint(0, 100) < self.rangoDisparo:
                x, y = self.rect.center
                self.disparar(x, y + 80)

            if len(self.disparos) > 0:
                for i in self.disparos:
                    i.velocidad = 5
                    superficie.blit(i.disparo, i.rect)
                    if self.rect.left > 500:
                        i.trayectoriaDiagonal(False)
                    else:
                        i.trayectoriaDiagonal(True)
                    if i.rect.top > 800:
                        self.disparos.remove(i)

        else:
            self.posImagen = len(self.estados) - randint(1, 3)

    def mostrar_vida(self, superficie):  # yop
        fuente = super().mostrar_vida(superficie)
        texto = fuente.render(str(int(self.vida*(1/2))) + "%", 0, (255, 0, 0))
        superficie.blit(texto, (self.rect.x + 10, self.rect.y + 40))
