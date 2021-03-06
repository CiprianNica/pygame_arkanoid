import pygame as pg
from Arkanoid import GAME_DIMENSIONS, FPS, DIMENSIONES_LADRILLO
from pygame.locals import *

import random
import sys
import enum


pg.init()

class PelotaStatus(enum.Enum):
    Viva = 0
    Explotando = 1
    Muerta = 2


class Ladrillo(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface(DIMENSIONES_LADRILLO)
        self.rect = self.image.get_rect(x=x, y=y)
        self.image.fill((255, 255, 255))
        pg.draw.rect(self.image, (255, 0, 0), Rect((2, 2),(self.rect.w-4, self.rect.h-4)))

class Raqueta(pg.sprite.Sprite):
    def __init__(self, x, y, vx):
        pg.sprite.Sprite.__init__(self)
        self.vx = vx
        self.vidas = 3
        self.image = pg.image.load("resources/images/regular_racket.png")
        self.rect = self.image.get_rect(x=x, y=y)

    def update(self, dt):
        self.rect.x += self.vx
        if self.rect.x + 128 >= GAME_DIMENSIONS[0]:
            self.rect.x = GAME_DIMENSIONS[0] - 128
        if self.rect.x <= 0:
            self.rect.x = 0
    
    def manejar_eventos(self):
        teclas_pulsadas = pg.key.get_pressed()
        if teclas_pulsadas[K_RIGHT]:
            self.vx = 10
        elif teclas_pulsadas[K_LEFT]:
            self.vx = -10
        else:
            self.vx = 0

class Pelota(pg.sprite.Sprite):
    imagenes_files = ['brown_ball.png', 'blue_ball.png', 'red_ball.png', 'green_ball.png']
    num_imgs_explosion = 8
    retardo_animaciones = 5

    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self) # o super().__init__()
        
        self.xo =x
        self.yo = y
        self.velocidad_inicial()
        self.imagenes = self.cargaImagenes()
        self.imagenes_explosion = self.cargaExplosion()
        self.imagen_act = 0
        self.ix_explosion = 0
        self.ciclos_tras_refresco = 0
        self.ticks_acumulados = 0
        self.ticks_por_frame_de_animacion = 1000/FPS * self.retardo_animaciones
        self.status = PelotaStatus.Viva

        self.image = self.imagenes[self.imagen_act]
        self.rect = self.image.get_rect(x=x, y=y)
    
    def reiniciar(self):
        self.ix_explosion = 0
        self.ticks_acumulados = 0
        self.status = PelotaStatus.Viva
        self.rect.x = self.xo
        self.rect.y = self.yo
        self.velocidad_inicial()

    def velocidad_inicial(self):
        self.vx = random.randint(2, 5)* random.choice([1, -1])
        self.vy = random.randint(2, 5)* random.choice([1, -1])


    def cargaExplosion(self):
        return [pg.image.load(f"resources/images/explosion0{i}.png") for i in range(self.num_imgs_explosion)]

    def cargaImagenes(self):
        lista_imagenes = []
        for img in self.imagenes_files:
            lista_imagenes.append(pg.image.load(f"resources/images/{img}"))
        return lista_imagenes


    def actualizar_posicion(self):
        if self.status == PelotaStatus.Explotando:
            return
        '''
        Gestionar posicion de pelota
        '''
        if self.rect.left <= 0 or self.rect.right >= GAME_DIMENSIONS[0]:
            self.vx = -self.vx

        if self.rect.top <= 0:
            self.vy = -self.vy

        if self.rect.bottom >= GAME_DIMENSIONS[1]:
            self.status = PelotaStatus.Explotando
            self.ciclos_tras_refresco = 0
            return

        self.rect.x += self.vx
        self.rect.y += self.vy

    def actualizar_disfraz(self):
        '''
        Gestionar imagen activa (disfraz) de pelota
        '''
        self.ciclos_tras_refresco += 1

        if self.ciclos_tras_refresco % self.retardo_animaciones == 0:
            self.imagen_act += 1
            if self.imagen_act >= len(self.imagenes):
                self.imagen_act = 0

        self.image = self.imagenes[self.imagen_act]

    def explosion(self, dt):

        if self.ix_explosion >= len(self.imagenes_explosion):
            self.status = PelotaStatus.Muerta
            return
        self.image= self.imagenes_explosion[self.ix_explosion]

        self.ticks_acumulados += dt
        if self.ticks_acumulados >= self.ticks_por_frame_de_animacion:
            self.ix_explosion += 1
            self.ticks_acumulados = 0
        return False

    def comprobar_colision(self, algo):
        if self.rect.colliderect(algo.rect):
            self.vy *= -1
            return True

    def update(self, dt):
        self.actualizar_posicion()

        if self.status == PelotaStatus.Explotando:
            return self.explosion(dt)
        else:
            self.actualizar_disfraz()

class Game:
    def __init__(self):

        self.pantalla = pg.display.set_mode(GAME_DIMENSIONS)
        pg.display.set_caption("Futuro Arcanoid")

        self.pelota = Pelota(400, 300)
        self.raqueta = Raqueta(336, 550, 0)

        self.cuenta_vidas = pg.font.Font("resources/fonts/ReggaeOne-Regular.ttf", 120)
        self.jugadores = pg.sprite.Group(self.raqueta)
        self.ladrillos = self.crea_ladrillos()
        self.pelotas = pg.sprite.Group(self.pelota)
        self.todos = pg.sprite.Group(self.ladrillos, self.jugadores, self.pelotas)

        self.clock = pg.time.Clock()

    def crea_ladrillos(self):
        ladrillos = pg.sprite.Group()
        xo = 22
        yo = 36
        for c in range(18):
            for f in range(5):
                l = Ladrillo(xo+c*DIMENSIONES_LADRILLO[0], yo+f*DIMENSIONES_LADRILLO[1])
                ladrillos.add(l)
        return ladrillos

    def bucle_principal(self):
        game_over = False

        while not game_over:
            dt = self.clock.tick(FPS)

        # Gestion de eventos

            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:# para poder cerrar la ventana del juego(evento QUIT)
                    pg.quit()
                    sys.exit()
            self.raqueta.manejar_eventos()

        # actualizacion de elementos del juego

            self.todos.update(dt)

            self.pelota.comprobar_colision(self.raqueta)
            if self.pelota.status == PelotaStatus.Muerta:
                self.raqueta.vidas -=1
                if self.raqueta.vidas == 0:
                    game_over = True
                else:
                    self.pelota.reiniciar()

            for ladrillo in self.ladrillos:
                if self.pelota.comprobar_colision(ladrillo):
                    self.ladrillos.remove(ladrillo)
                    self.todos.remove(ladrillo)

            Svidas = self.cuenta_vidas.render(str(self.raqueta.vidas), True, (255, 255, 255))
            Rvidas = Svidas.get_rect(bottomright=(1195, 795))

            Sladrillos = self.cuenta_vidas.render("una palabra", True, (0,255, 255))
            Rladrillos = Sladrillos.get_rect(bottomleft=(5, 595))

            self.pantalla.fill((0, 0, 255))
            self.todos.draw(self.pantalla)

            self.pantalla.blit(Svidas, (Rvidas.x, Rvidas.y))
            self.pantalla.blit(Sladrillos, (Rladrillos.x, Rladrillos.y))


        # Refrescar pantalla

            pg.display.flip()


