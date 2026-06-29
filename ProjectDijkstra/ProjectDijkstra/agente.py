import pygame
import os
from dijkstra import Dijkstra

from utils import resource_path

# Ruta base para buscar las imágenes y sonidos
RECURSOS_DIR = resource_path("recursos")

class Agente:

    def __init__(self, mapa, posicion_inicial):
        # El zombi necesita conocer el mapa para moverse
        self.mapa = mapa
        self.posicion = posicion_inicial
        self.ruta = [] # Lista que guardará los pasos hasta el jugador
        self.dijkstra = Dijkstra(mapa) # Instancia de nuestro algoritmo
        
        # Cargamos la imagen del zombi
        ruta_zombi = os.path.join(RECURSOS_DIR, "sprites", "zombi.png")
        self.img_zombi = None
        if os.path.exists(ruta_zombi):
            try:
                self.img_zombi = pygame.image.load(ruta_zombi).convert_alpha()
                self.img_zombi = pygame.transform.scale(self.img_zombi, (50, 50))
            except: pass

    def percibir(self, posicion_jugador):
        # Actualiza la ubicación actual del objetivo (el jugador)
        self.posicion_jugador = posicion_jugador

    def calcular_ruta(self):
        # Llama a Dijkstra para calcular el camino más corto hacia el jugador
        self.ruta = self.dijkstra.calcular_ruta(self.posicion, self.posicion_jugador)

    def mover(self):
        # Si hay una ruta válida, el zombi avanza a la siguiente casilla (índice 1)
        if len(self.ruta) > 1:
            self.posicion = self.ruta[1]

    def actualizar(self, posicion_jugador):
        # Ciclo de vida del agente: mira dónde estás, piensa la ruta y camina
        self.percibir(posicion_jugador)
        self.calcular_ruta()
        self.mover()

    def obtener_posicion(self):
        # Retorna la coordenada actual del zombi
        return self.posicion

    def obtener_ruta(self):
        # Retorna todo el camino calculado (útil para dibujarlo en pantalla)
        return self.ruta
    
    def dibujar(self, pantalla):
        # Calcula las coordenadas en píxeles (cada celda mide 50x50)
        x = self.posicion[1] * 50
        y = self.posicion[0] * 50
        
        # Pinta la imagen del zombi o un círculo rojo si no encuentra la imagen
        if self.img_zombi:
            pantalla.blit(self.img_zombi, (x, y))
        else:
            pygame.draw.circle(pantalla, (255, 0, 0), (x + 25, y + 25), 18)