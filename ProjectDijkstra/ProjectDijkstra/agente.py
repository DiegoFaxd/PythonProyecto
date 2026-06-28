import pygame
import os
from dijkstra import Dijkstra

from utils import resource_path

RECURSOS_DIR = resource_path("recursos")

class Agente:

    def __init__(self, mapa, posicion_inicial):
        self.mapa = mapa
        self.posicion = posicion_inicial
        self.ruta = []
        self.dijkstra = Dijkstra(mapa)
        
        ruta_zombi = os.path.join(RECURSOS_DIR, "sprites", "zombi.png")
        self.img_zombi = None
        if os.path.exists(ruta_zombi):
            try:
                self.img_zombi = pygame.image.load(ruta_zombi).convert_alpha()
                self.img_zombi = pygame.transform.scale(self.img_zombi, (50, 50))
            except: pass

    def percibir(self, posicion_jugador):
        self.posicion_jugador = posicion_jugador

    def calcular_ruta(self):
        self.ruta = self.dijkstra.calcular_ruta(self.posicion, self.posicion_jugador)

    def mover(self):
        if len(self.ruta) > 1:
            self.posicion = self.ruta[1]

    def actualizar(self, posicion_jugador):
        self.percibir(posicion_jugador)
        self.calcular_ruta()
        self.mover()

    def obtener_posicion(self):
        return self.posicion

    def obtener_ruta(self):
        return self.ruta
    
    def dibujar(self, pantalla):
        x = self.posicion[1] * 50
        y = self.posicion[0] * 50
        if self.img_zombi:
            pantalla.blit(self.img_zombi, (x, y))
        else:
            pygame.draw.circle(pantalla, (255, 0, 0), (x + 25, y + 25), 18)