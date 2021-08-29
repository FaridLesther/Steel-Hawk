import Enemigo
import Disparo
from random import randint


class Helicoptero(Enemigo.Enemigo):
    def __init__(self, posicion, numAnimaciones: int, ruta: str):
        super().__init__(posicion, numAnimaciones, ruta)
        self.vida = 1600

    def disparar(self, x, y):
        disparo = Disparo.Disparo(x - 10, y, "Graficos/disparo3.png")
        self.disparos.append(disparo)

    def comportamiento(self, tiempoEstado, superficie, posAvion):
        # control de aparicion
        if self.vivo:
            if self.rect.top < 5:
                self.rect.top += 1
            # seguimiento al avion
            if self.rect.left < posAvion:
                self.rect.left += 2
            else:
                self.rect.left -= 2

            if self.vida <= 0:
                self.vivo = False
                self.explosion.play()

              # control de la animacion
            if self.tiempoEstado <= int(tiempoEstado):
                self.posImagen += 1
                self.tiempoEstado += 1
            if self.posImagen > len(self.estados) - 4:
                self.posImagen = 0

            # control de disparos
            if randint(0, 20) < self.rangoDisparo and self.rect.top > -3:
                posAvion, y = self.rect.center
                self.disparar(posAvion, y + 80)
            if len(self.disparos) > 0:
                for i in self.disparos:
                    i.velocidad = 5
                    superficie.blit(i.disparo, i.rect)
                    i.trayectoria(True)
                    if i.rect.top > 800:
                        self.disparos.remove(i)

        else:
            self.rect.top += 1
            self.posImagen = len(self.estados) - randint(1, 3)

    def mostrar_vida(self, superficie):  # yop
        x, y = self.rect.center
        # yop se hereda la fuente de la Clase Enemigo
        fuente = super().mostrar_vida(superficie)
        # yop texto de la vida del enemigo en formato de porcentaje
        texto = fuente.render(str(int(self.vida*(1/4))) + "%", 0, (255, 0, 0))
        # coloca el texto en la superficie(en este caso la ventana)
        superficie.blit(texto, (x + 10, y-50))
