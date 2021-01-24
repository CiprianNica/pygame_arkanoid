import pygame as pg
import sys
import random
class Game:
    def __init__(self):
        self.pantalla = pg.display.set_mode( (800, 600) )
        pg.display.set_caption("Futuro Arcanoid")

    def bucle_principal(self):
        game_over = False
        while not game_over:
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:# para poder cerrar la ventana del juego(evento QUIT)
                    pg.quit()
                    sys.exit()

            self.pantalla.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
            pg.display.flip()


if __name__ == '__main__':
    pg.init() #inicializar pygame
    game = Game() # creamos la instancia de nuestro juego
    game.bucle_principal()