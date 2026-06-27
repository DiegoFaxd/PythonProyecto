import pygame
import sys
import os

# Sincronizado perfectamente con las dimensiones extendidas del mapa
ANCHO = 1250
ALTO = 850
COLOR_FONDO = (35, 35, 35)
COLOR_BOTON = (50, 140, 220)
COLOR_BOTON_HOVER = (70, 170, 255)
COLOR_TEXTO = (255, 255, 255)

pygame.font.init()

# Rutas dinámicas para que encuentre los archivos en cualquier PC sin errores
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RECURSOS_DIR = os.path.join(BASE_DIR, "recursos")

RUTA_FUENTE = os.path.join(RECURSOS_DIR, "fuentes", "PressStart2P-Regular.ttf")
if os.path.exists(RUTA_FUENTE):
    FUENTE_TITULO = pygame.font.Font(RUTA_FUENTE, 32)
    FUENTE_BOTON = pygame.font.Font(RUTA_FUENTE, 16)
    FUENTE_INFO = pygame.font.Font(RUTA_FUENTE, 11)
else:
    FUENTE_TITULO = pygame.font.SysFont("Arial", 48, bold=True)
    FUENTE_BOTON = pygame.font.SysFont("Arial", 28)
    FUENTE_INFO = pygame.font.SysFont("Arial", 18)

class Boton:

    def __init__(self, x, y, ancho, alto, texto):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.texto = texto

    def dibujar(self, pantalla):
        mouse = pygame.mouse.get_pos()
        color = COLOR_BOTON_HOVER if self.rect.collidepoint(mouse) else COLOR_BOTON

        pygame.draw.rect(pantalla, color, self.rect, border_radius=12)
        # False = pixelado perfecto
        texto = FUENTE_BOTON.render(self.texto, False, COLOR_TEXTO) 
        pantalla.blit(texto, texto.get_rect(center=self.rect.center))

    def clic(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            return self.rect.collidepoint(evento.pos)
        return False


class MenuPrincipal:

    def __init__(self, pantalla):
        self.pantalla = pantalla
        
        #Centrado automático de botones en base al nuevo ancho horizontal (1250)
        ancho_btn = 200
        alto_btn = 60
        x_centrado = (ANCHO - ancho_btn) // 2
        
        # Alturas ajustadas para que no se vean muy arriba en la pantalla gigante de 850
        self.boton_jugar = Boton(x_centrado, 360, ancho_btn, alto_btn, "JUGAR")
        self.boton_salir = Boton(x_centrado, 460, ancho_btn, alto_btn, "SALIR")
        
        # Ruta dinámica para el fondo
        ruta_fondo = os.path.join(RECURSOS_DIR, "fondos", "fondo_juego.png")
        self.img_fondo = None
        if os.path.exists(ruta_fondo):
            try:
                self.img_fondo = pygame.image.load(ruta_fondo).convert()
                self.img_fondo = pygame.transform.scale(self.img_fondo, (ANCHO, ALTO))
            except: pass

    def dibujar(self):
        if self.img_fondo:
            self.pantalla.blit(self.img_fondo, (0, 0))
        else:
            self.pantalla.fill(COLOR_FONDO)

        # Renders con False para máximo estilo Pixel Art
        titulo_sombra = FUENTE_TITULO.render("Zombie IA - Dijkstra", False, (0, 0, 0))
        titulo = FUENTE_TITULO.render("Zombie IA - Dijkstra", False, COLOR_TEXTO)

        # Título centrado y reposicionado proporcionalmente en vertical
        self.pantalla.blit(titulo_sombra, titulo_sombra.get_rect(center=(ANCHO//2 + 3, 183)))
        self.pantalla.blit(titulo, titulo.get_rect(center=(ANCHO//2, 180)))

        self.boton_jugar.dibujar(self.pantalla)
        self.boton_salir.dibujar(self.pantalla)

        # El texto informativo se adapta dinámicamente al nuevo ALTO de 850 (ya no queda flotando)
        texto = FUENTE_INFO.render("Proyecto de Inteligencia Artificial", False, COLOR_TEXTO)
        self.pantalla.blit(texto, (20, ALTO - 40))
        pygame.display.flip()

    def ejecutar(self):
        while True:
            self.dibujar()
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if self.boton_jugar.clic(evento):
                    return True
                if self.boton_salir.clic(evento):
                    pygame.quit()
                    sys.exit()