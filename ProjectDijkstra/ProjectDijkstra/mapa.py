import pygame
import os

# ¡Casillas más grandes! Cambiado de 40 a 50 para que todo se vea más imponente
TAM_CASILLA = 50 
COLOR_MURO = (40, 40, 40)
COLOR_CAMINO = (210, 210, 210)

class Mapa:

    def __init__(self):
        self.matriz = [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,1,1,1,0,1,1,1,1,1,0,1,0,1,1,1,0,1,1,1,0,1,0,1],
            [1,0,0,0,1,0,0,0,0,0,1,0,1,0,0,0,1,0,0,0,1,0,0,0,1],
            [1,1,1,0,1,1,1,1,1,0,1,0,1,1,1,0,1,1,1,0,1,1,1,0,1],
            [1,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,1],
            [1,0,1,1,1,1,1,1,1,0,1,1,1,0,1,1,1,1,1,0,1,1,1,0,1],
            [1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1],
            [1,1,1,0,1,0,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,0,1,1,1],
            [1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,1],
            [1,0,1,0,1,1,1,0,1,1,1,1,1,1,1,0,1,0,1,0,1,1,1,0,1],
            [1,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,1],
            [1,0,1,1,1,1,1,1,1,0,1,1,1,0,1,1,1,1,1,1,1,1,1,0,1],
            [1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,0,1,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        ]
        
        # Cálculo dinámico del tamaño según las dimensiones de la matriz
        self.columnas = len(self.matriz[0])
        self.filas = len(self.matriz)
        self.ancho_total = self.columnas * TAM_CASILLA
        self.alto_total = self.filas * TAM_CASILLA
        
        base_dir = os.path.dirname(__file__)
        
        self.img_muro = None
        self.img_piso = None
        self.img_fondo = None
        
        # 1. CARGAR Y ADAPTAR SPRITES AL NUEVO TAMAÑO
        ruta_muro = os.path.join(base_dir, "recursos", "sprites", "muro.png")
        if os.path.exists(ruta_muro):
            try:
                self.img_muro = pygame.image.load(ruta_muro).convert_alpha()
                self.img_muro = pygame.transform.scale(self.img_muro, (TAM_CASILLA, TAM_CASILLA))
            except: pass
                
        ruta_piso = os.path.join(base_dir, "recursos", "sprites", "piso.png")
        if os.path.exists(ruta_piso):
            try:
                self.img_piso = pygame.image.load(ruta_piso).convert_alpha()
                self.img_piso = pygame.transform.scale(self.img_piso, (TAM_CASILLA, TAM_CASILLA))
            except: pass

        ruta_fondo = os.path.join(base_dir, "recursos", "fondos", "fondo_juego.png")
        if not os.path.exists(ruta_fondo):
            ruta_fondo = os.path.join(base_dir, "recursos", "fondo_juego.png")

        if os.path.exists(ruta_fondo):
            try:
                self.img_fondo = pygame.image.load(ruta_fondo).convert()
                # Escalamos el fondo automáticamente al nuevo tamaño total calculado
                self.img_fondo = pygame.transform.scale(self.img_fondo, (self.ancho_total, self.alto_total))
            except: pass

        # 2. PRE-RENDERIZADO AJUSTADO
        self.superficie_estatica = pygame.Surface((self.ancho_total, self.alto_total))
        self.pre_renderizar_mapa()

    def pre_renderizar_mapa(self):
        if self.img_fondo:
            self.superficie_estatica.blit(self.img_fondo, (0, 0))
        else:
            self.superficie_estatica.fill((35, 35, 35))

        for fila in range(self.filas):
            for columna in range(self.columnas):
                x = columna * TAM_CASILLA
                y = fila * TAM_CASILLA

                if self.matriz[fila][columna] == 1:
                    if self.img_muro:
                        self.superficie_estatica.blit(self.img_muro, (x, y))
                    else:
                        pygame.draw.rect(self.superficie_estatica, COLOR_MURO, (x, y, TAM_CASILLA, TAM_CASILLA))
                else:
                    if self.img_piso:
                        self.superficie_estatica.blit(self.img_piso, (x, y))
                    elif not self.img_fondo:
                        pygame.draw.rect(self.superficie_estatica, COLOR_CAMINO, (x, y, TAM_CASILLA, TAM_CASILLA))

    def dibujar(self, pantalla):
        pantalla.blit(self.superficie_estatica, (0, 0))

    def es_camino(self, fila, columna):
        if 0 <= fila < self.filas and 0 <= columna < self.columnas:
            return self.matriz[fila][columna] == 0
        return False

    def vecinos(self, fila, columna):
        movimientos = [(-1,0), (1,0), (0,-1), (0,1)]
        lista = []
        for df, dc in movimientos:
            nf = fila + df
            nc = columna + dc
            if self.es_camino(nf, nc):
                lista.append((nf, nc))
        return lista