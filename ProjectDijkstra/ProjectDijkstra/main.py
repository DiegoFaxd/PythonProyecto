import pygame
import sys
import os

from interfaz import MenuPrincipal, RUTA_FUENTE, Boton
from mapa import Mapa
from agente import Agente
from utils import resource_path
    
ANCHO = 1250
ALTO = 850
FPS = 120 # Fotogramas por segundo

RECURSOS_DIR = resource_path("recursos")

def main():
    # Inicialización del motor gráfico y de sonido
    pygame.init()
    pygame.mixer.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Agente inteligente - Algoritmo de Dijkstra")
    
    # Carga de icono y música ambiental
    ruta_icono = os.path.join(RECURSOS_DIR, "iconos", "icono.ico")
    if os.path.exists(ruta_icono):
        try:
            icono = pygame.image.load(ruta_icono)
            pygame.display.set_icon(icono)
        except: pass

    ruta_musica = os.path.join(RECURSOS_DIR, "sonidos", "musica.mp3")
    if os.path.exists(ruta_musica):
        try:
            pygame.mixer.music.load(ruta_musica)
            pygame.mixer.music.set_volume(0.5) 
            pygame.mixer.music.play(-1) # El -1 hace que se repita en bucle
        except: pass
        
    reloj = pygame.time.Clock()
    menu = MenuPrincipal(pantalla)

    # Control general del flujo (Menú -> Juego -> Menú)
    while True:
        if menu.ejecutar():
            while True:
                # Arrancamos la partida principal
                resultado = ejecutar_juego(pantalla, reloj)
                
                # Gestión de los resultados después de ganar/perder
                if resultado == "MENU":
                    if os.path.exists(ruta_musica):
                        pygame.mixer.music.play(-1)
                    break
                elif resultado == "REINTENTAR" or resultado == "JUGAR DENUEVO":
                    if os.path.exists(ruta_musica):
                        pygame.mixer.music.play(-1)
                    pass # Vuelve a iterar y reiniciar el nivel

def ejecutar_juego(pantalla, reloj):
    # Instanciamos los elementos principales de la partida
    mapa = Mapa()
    pos_jugador = [1, 1] 
    zombi = Agente(mapa, (7, 13))

    llaves = list(mapa.llaves)
    pos_salida = mapa.pos_salida
    llaves_totales = len(llaves)

    # Carga de sprites (Jugador y Llaves)
    ruta_jugador = os.path.join(RECURSOS_DIR, "sprites", "Jugador.png")
    img_jugador = None
    if os.path.exists(ruta_jugador):
        try:
            img_jugador = pygame.image.load(ruta_jugador).convert_alpha()
            img_jugador = pygame.transform.scale(img_jugador, (50, 50))
        except: pass

    ruta_llave = os.path.join(RECURSOS_DIR, "sprites", "llave.png")
    img_llave = None
    if os.path.exists(ruta_llave):
        try:
            img_llave = pygame.image.load(ruta_llave).convert_alpha()
            img_llave = pygame.transform.scale(img_llave, (30, 30))
        except: pass

    # Carga de los efectos de sonido de acción
    ruta_gamewin = os.path.join(RECURSOS_DIR, "sonidos", "victoria.wav")
    ruta_pasos = os.path.join(RECURSOS_DIR, "sonidos", "pasos2.mp3")
    ruta_gameover = os.path.join(RECURSOS_DIR, "sonidos", "gameover.wav")

    snd_pasos, snd_gameover, snd_gamewin = None, None, None
    try:
        if os.path.exists(ruta_pasos):
            snd_pasos = pygame.mixer.Sound(ruta_pasos)
            snd_pasos.set_volume(0.5)
        if os.path.exists(ruta_gameover):
            snd_gameover = pygame.mixer.Sound(ruta_gameover)
            snd_gameover.set_volume(1)
        if os.path.exists(ruta_gamewin):
            snd_gamewin = pygame.mixer.Sound(ruta_gamewin)
            snd_gamewin.set_volume(1)
    except: pass

    # Control de velocidad del zombi (para que no te atrape instantáneamente)
    ultimo_movimiento_zombi = pygame.time.get_ticks()
    COOLDOWN_ZOMBI = 250 # Milisegundos entre cada paso del zombi

    # Configuración de textos y botones de las pantallas de fin de juego
    if os.path.exists(RUTA_FUENTE):
        fuente_go = pygame.font.Font(RUTA_FUENTE, 48)
        fuente_exit = pygame.font.Font(RUTA_FUENTE, 10)
        fuente_hud = pygame.font.Font(RUTA_FUENTE, 24)
    else:
        fuente_go = pygame.font.SysFont("Arial", 64, bold=True)
        fuente_exit = pygame.font.SysFont("Arial", 20, bold=True)
        fuente_hud = pygame.font.SysFont("Arial", 64, bold=True)

    boton_reintentar = Boton(ANCHO//2 - 150, ALTO//2 + 30, 300, 60, "REINTENTAR")
    boton_menu = Boton(ANCHO//2 - 150, ALTO//2 + 110, 300, 60, "VOLVER AL MENU")
    boton_jugar_denuevo = Boton(ANCHO//2 - 150, ALTO//2 + 30, 300, 60, "JUGAR DENUEVO")

    ejecutando = True
    estado_gameover = False
    estado_victoria = False

    # --- BUCLE PRINCIPAL DE LA PARTIDA ---
    while ejecutando:
        reloj.tick(FPS)
        tiempo_actual = pygame.time.get_ticks()
        pos_tuple = tuple(pos_jugador)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Lógica de clicks cuando pierdes
            if estado_gameover:
                if boton_reintentar.clic(evento): return "REINTENTAR"
                if boton_menu.clic(evento): return "MENU"
            
            # Lógica de clicks cuando ganas
            if estado_victoria:
                if boton_jugar_denuevo.clic(evento): return "JUGAR DENUEVO"
                if boton_menu.clic(evento): return "MENU"

            # Movimiento del jugador con las flechas o letras WASD
            if not estado_gameover and evento.type == pygame.KEYDOWN:
                nueva_fila, nueva_columna = pos_jugador[0], pos_jugador[1]

                if evento.key in (pygame.K_UP, pygame.K_w): nueva_fila -= 1
                elif evento.key in (pygame.K_DOWN, pygame.K_s): nueva_fila += 1
                elif evento.key in (pygame.K_LEFT, pygame.K_a): nueva_columna -= 1
                elif evento.key in (pygame.K_RIGHT, pygame.K_d): nueva_columna += 1

                # Verifica en el mapa que no haya un muro para poder moverse
                if mapa.es_camino(nueva_fila, nueva_columna):
                    pos_jugador = [nueva_fila, nueva_columna]
                    if snd_pasos:
                        snd_pasos.play()

        # Actualizaciones automáticas solo si la partida sigue activa
        if not estado_gameover and not estado_victoria:
            # Movemos al zombi si ya pasó el tiempo de espera (cooldown)
            if tiempo_actual - ultimo_movimiento_zombi > COOLDOWN_ZOMBI:
                zombi.actualizar(pos_tuple)
                ultimo_movimiento_zombi = tiempo_actual

            # Condición de derrota: El zombi y el jugador están en la misma casilla
            if zombi.obtener_posicion() == pos_tuple:
                estado_gameover = True
                pygame.mixer.music.stop() 
                if snd_gameover: snd_gameover.play()

            # Recolección de llaves
            if pos_tuple in llaves:
                llaves.remove(pos_tuple)
            
            # Condición de victoria: Estás en la salida sin llaves pendientes
            if pos_tuple == pos_salida and len(llaves) == 0:
                estado_victoria = True 
                pygame.mixer.music.stop()
                if snd_gamewin: snd_gamewin.play()

        # DIBUJADO EN PANTALLA
        mapa.dibujar(pantalla)

        # Dibuja la casilla verde de salida
        sx = pos_salida[1] * 50
        sy = pos_salida[0] * 50
        pygame.draw.rect(pantalla, (0, 200, 0), (sx, sy, 50, 50))
        texto_salida = fuente_exit.render("EXIT", False, (255, 255, 255))
        pantalla.blit(texto_salida, (sx + 4, sy + 16))

        # Dibuja las llaves restantes
        for (lf, lc) in llaves:
            lx = lc * 50
            ly = lf * 50
            if img_llave:
                pantalla.blit(img_llave, (lx + 10, ly + 10))
            else:
                pygame.draw.circle(pantalla, (255, 215, 0), (lx + 25, ly + 25), 14)  
                pygame.draw.circle(pantalla, (180, 140, 0), (lx + 25, ly + 25), 14, 3)  
        
        # Interfaz de texto (HUD) con el contador
        texto_llaves = fuente_hud.render(f"Llaves: {llaves_totales - len(llaves)}/{llaves_totales}", False, (255, 215, 0))
        pantalla.blit(texto_llaves, (10, 10))

        # Aviso si intentas salir antes de tiempo
        if pos_tuple == pos_salida and len(llaves) > 0:
            aviso = fuente_hud.render("¡No recolectaste todas las llaves!", False, (255, 80, 80))
            pantalla.blit(aviso, (ANCHO//2 - 180, 20))

        # Dibujamos visualmente la ruta que calculó Dijkstra (cuadritos rojos)
        ruta_zombi = zombi.obtener_ruta()
        if len(ruta_zombi) > 1:
            superficie_ruta = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
            for f, c in ruta_zombi[1:-1]: 
                x = c * 50
                y = f * 50
                pygame.draw.rect(superficie_ruta, (255, 0, 0, 60), (x, y, 50, 50))
            pantalla.blit(superficie_ruta, (0, 0))

        # Dibujamos a los personajes
        zombi.dibujar(pantalla)
        
        if not estado_gameover:
            if img_jugador:
                pantalla.blit(img_jugador, (pos_jugador[1] * 50, pos_jugador[0] * 50))
            else:
                pygame.draw.circle(pantalla, (0, 255, 0), (pos_jugador[1] * 50 + 25, pos_jugador[0] * 50 + 25), 18)

        # Pantalla final al morir
        if estado_gameover:
            superficie_oscura = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
            superficie_oscura.fill((0, 0, 0, 160)) 
            pantalla.blit(superficie_oscura, (0, 0))

            texto_go = fuente_go.render("GAME OVER", False, (255, 0, 0))
            pantalla.blit(texto_go, texto_go.get_rect(center=(ANCHO//2, ALTO//2 - 50)))

            boton_reintentar.dibujar(pantalla)
            boton_menu.dibujar(pantalla)

        # Pantalla final al ganar
        if estado_victoria:
            superficie_oscura = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
            superficie_oscura.fill((0, 0, 0, 160))
            pantalla.blit(superficie_oscura, (0, 0))

            texto_win = fuente_go.render("¡SOBREVIVISTE!", False, (0, 255, 100))
            pantalla.blit(texto_win, texto_win.get_rect(center=(ANCHO//2, ALTO//2 - 50)))

            boton_jugar_denuevo.dibujar(pantalla)
            boton_menu.dibujar(pantalla)
        
        # Actualiza toda la pantalla al final del bucle
        pygame.display.flip()

if __name__ == "__main__":
    main()