import pygame as pg
import sys
import random
import entidades


class Game:
    def __init__(self):
        self.pantalla = pg.display.set_mode( (800, 600) )
        pg.display.set_caption("Futuro Arcanoid")
        self.pelota = entidades.Pelota(400, 300, 10, 10, (251, 202, 239), 25)

    def bucle_principal(self):
        game_over = False
        while not game_over:
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:# para poder cerrar la ventana del juego(evento QUIT)
                    pg.quit()
                    sys.exit()

            if self.pelota.left <= 0 or self.pelota.right >= 800:
                self.pelota.vx = -self.pelota.vx

            if self.pelota.top <= 0 or self.pelota.bottom >= 600:
                self.pelota.vy = -self.pelota.vy

            self.pantalla.fill((0, 0, 255))
            self.pantalla.blit(self.pelota.imagen, (self.pelota.x, self.pelota.y))


            self.pelota.x += self.pelota.vx
            self.pelota.y += self.pelota.vy


            pg.display.flip()


if __name__ == '__main__':
    pg.init() #inicializar pygame
    game = Game() # creamos la instancia de nuestro juego
    game.bucle_principal()