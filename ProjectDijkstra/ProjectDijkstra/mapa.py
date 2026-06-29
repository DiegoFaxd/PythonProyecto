import pygame
import os
import random

TAM_CASILLA = 50 
COLOR_MURO = (40, 40, 40)
COLOR_CAMINO = (210, 210, 210)

class Mapa:

    def __init__(self):
        # 1 es muro, 0 es camino libre
        self.matriz = [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,1,1,1,0,1,1,1,1,1,0,1,0,1,1,1,0,1,1,1,0,1,0,1],
            [1,0,0,0,1,0,0,0,0,0,1,0,1,0,0,0,1,0,0,0,1,0,0,0,1],
            [1,1,1,0,1,1,1,1,1,0,1,0,1,1,1,0,1,1,1,0,1,1,1,0,1],
            [1,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,1],
            [1,0,1,1,1,1,1,1,1,0,1,1,1,0,1,1,1,1,1,0,1,1,1,0,1],
            [1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1],
            [1,1,1,0,1,0,1,1,1,1,1,0,1,1,1,1,1,0,1,0,1,1,0,1,1],
            [1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,1],
            [1,0,1,0,1,1,1,0,1,1,1,1,1,1,1,1,1,0,1,0,1,1,1,0,1],
            [1,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1],
            [1,0,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,1,1,0,1,1,1,0,1],
            [1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,1,1,0,1],    
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        ]
        
        # Dimensiones del laberinto
        self.columnas = len(self.matriz[0])
        self.filas = len(self.matriz)
        self.ancho_total = self.columnas * TAM_CASILLA
        self.alto_total = self.filas * TAM_CASILLA
        
        base_dir = os.path.dirname(__file__)
        self.img_muro = None
        self.img_piso = None
        self.img_fondo = None

        self.pos_salida = (15, 23)  
        
        # Generamos las posiciones de llaves y salida aleatoriamente
        self.llaves, self.pos_salida = self.generar_llaves_y_salida(
            cantidad_llaves=3,
            pos_jugador=(1, 1),
            pos_zombi=(7, 13)
        )
        
        # Bloque de carga de texturas...
        ruta_muro = os.path.join(base_dir, "recursos", "sprites", "muro2.jpg")
        if os.path.exists(ruta_muro):
            try:
                self.img_muro = pygame.image.load(ruta_muro).convert_alpha()
                self.img_muro = pygame.transform.scale(self.img_muro, (TAM_CASILLA, TAM_CASILLA))
            except: pass
                
        ruta_piso = os.path.join(base_dir, "recursos", "sprites", "pasto.png")
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
                self.img_fondo = pygame.transform.scale(self.img_fondo, (self.ancho_total, self.alto_total))
            except: pass

        # Superficie para dibujar el mapa una sola vez y mejorar el rendimiento (optimización)
        self.superficie_estatica = pygame.Surface((self.ancho_total, self.alto_total))
        self.pre_renderizar_mapa()

    def pre_renderizar_mapa(self):
        # Pinta el mapa estático completo en memoria
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
        # Solo dibuja la imagen pre-renderizada en vez de bloque por bloque
        pantalla.blit(self.superficie_estatica, (0, 0))

    def es_camino(self, fila, columna):
        # Verifica que la coordenada esté dentro del mapa y sea un 0
        if 0 <= fila < self.filas and 0 <= columna < self.columnas:
            return self.matriz[fila][columna] == 0
        return False

    def vecinos(self, fila, columna):
        # Retorna las casillas transitables adyacentes a una posición
        movimientos = [(-1,0), (1,0), (0,-1), (0,1)]
        lista = []
        for df, dc in movimientos:
            nf = fila + df
            nc = columna + dc
            if self.es_camino(nf, nc):
                lista.append((nf, nc))
        return lista
    
    def generar_llaves_y_salida(self, cantidad_llaves, pos_jugador, pos_zombi):
        # Evita poner llaves donde aparecen los personajes
        excluir_base = [pos_jugador, pos_zombi]
        # Saca todas las casillas libres (ceros)
        celdas_libres = [
            (f, c) for f in range(self.filas) for c in range(self.columnas)
            if self.matriz[f][c] == 0 and (f, c) not in excluir_base
        ]

        # Intenta colocar los objetos aleatoriamente y valida que se puedan alcanzar
        for _ in range(200):
            seleccion = random.sample(celdas_libres, cantidad_llaves + 1)
            llaves = seleccion[:cantidad_llaves]
            salida = seleccion[cantidad_llaves]

            puntos_a_validar = llaves + [salida]
            # BFS valida si hay ruta posible hacia cada objeto
            if all(self.hay_camino(pos_jugador, p) for p in puntos_a_validar):
                return llaves, salida

        # Si falla (raro), pone posiciones por defecto
        return [(1, 5), (9, 11), (15, 5)], (15, 23)

    def hay_camino(self, origen, destino):
        # Algoritmo BFS para comprobar si un punto es alcanzable (Filtro de seguridad)
        if origen == destino:
            return True
        visitados = {origen}
        cola = [origen]
        while cola:
            actual = cola.pop(0)
            for vecino in self.vecinos(*actual):
                if vecino == destino:
                    return True
                if vecino not in visitados:
                    visitados.add(vecino)
                    cola.append(vecino)
        return False