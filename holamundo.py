import pygame
import random
import math

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
ANCHO = 800
ALTO = 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption('Ping Pong')

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (128, 128, 128)

# Fuentes
fuente = pygame.font.Font(None, 36)
fuente_grande = pygame.font.Font(None, 74)

# Reloj para controlar la velocidad del juego
reloj = pygame.time.Clock()

# Configuración del juego
PALETA_ANCHO = 15
PALETA_ALTO = 90
PUNTOS_VICTORIA = 5
modo_juego = None  # 1 = un jugador, 2 = dos jugadores

# Agregar estas variables globales al inicio del código, junto con las otras configuraciones
VELOCIDAD_IA_BASE = 6
VELOCIDAD_PELOTA_BASE = 7
INCREMENTO_VELOCIDAD = 1.1  # Factor de incremento de velocidad

def mostrar_menu():
    while True:
        pantalla.fill(NEGRO)
        titulo = fuente_grande.render('PING PONG', True, BLANCO)
        un_jugador = fuente.render('1 - Un Jugador', True, BLANCO)
        dos_jugadores = fuente.render('2 - Dos Jugadores', True, BLANCO)
        salir = fuente.render('ESC - Salir', True, BLANCO)

        pantalla.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 100))
        pantalla.blit(un_jugador, (ANCHO//2 - un_jugador.get_width()//2, 300))
        pantalla.blit(dos_jugadores, (ANCHO//2 - dos_jugadores.get_width()//2, 350))
        pantalla.blit(salir, (ANCHO//2 - salir.get_width()//2, 450))

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return None
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_1:
                    return 1
                if evento.key == pygame.K_2:
                    return 2
                if evento.key == pygame.K_ESCAPE:
                    return None

def mover_ia(paleta, pelota):
    # Predicción de la posición de la pelota
    prediccion_y = pelota.centery
    
    # La IA solo reacciona cuando la pelota va hacia ella
    if velocidad_x > 0:
        # Calcular punto de intercepción
        distancia_x = paleta.centerx - pelota.centerx
        tiempo = distancia_x / velocidad_x
        prediccion_y += velocidad_y * tiempo
        
        # Mantener la predicción dentro de los límites de la pantalla
        prediccion_y = max(min(prediccion_y, ALTO - PALETA_ALTO//2), PALETA_ALTO//2)
        
        # Añadir un pequeño error aleatorio para hacer la IA más realista
        error = random.randint(-20, 20)
        prediccion_y += error
    
    # Mover la paleta hacia la predicción
    if paleta.centery < prediccion_y and paleta.bottom < ALTO:
        paleta.y += VELOCIDAD_IA_BASE
    if paleta.centery > prediccion_y and paleta.top > 0:
        paleta.y -= VELOCIDAD_IA_BASE

def mostrar_ganador(ganador):
    pantalla.fill(NEGRO)
    texto = fuente_grande.render(f'¡{ganador} GANA!', True, BLANCO)
    continuar = fuente.render('Presiona ESPACIO para continuar', True, GRIS)
    pantalla.blit(texto, (ANCHO//2 - texto.get_width()//2, ALTO//2 - texto.get_height()//2))
    pantalla.blit(continuar, (ANCHO//2 - continuar.get_width()//2, ALTO//2 + 100))
    pygame.display.flip()
    
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                return True
    return False

def reiniciar_pelota(ultima_puntuacion):
    """
    Reinicia la pelota en el centro con una dirección controlada
    ultima_puntuacion: 'izq' o 'der' para indicar quién puntuó
    """
    pelota.center = (ANCHO//2, ALTO//2)
    
    # Velocidad base
    velocidad_x = VELOCIDAD_PELOTA_BASE
    
    # Dirección hacia el jugador que perdió el punto
    if ultima_puntuacion == 'der':
        velocidad_x = -velocidad_x
    
    # Ángulo aleatorio controlado (entre -45 y 45 grados)
    angulo = random.uniform(-0.785, 0.785)  # radianes
    velocidad_y = velocidad_x * math.tan(angulo)
    
    # Asegurar que la velocidad vertical no sea muy alta
    velocidad_y = max(min(velocidad_y, VELOCIDAD_PELOTA_BASE), -VELOCIDAD_PELOTA_BASE)
    
    return velocidad_x, velocidad_y

def mostrar_menu_post_partida(ganador):
    """
    Muestra el menú después de cada partida con opciones para jugar de nuevo o volver al menú principal
    """
    while True:
        pantalla.fill(NEGRO)
        texto_ganador = fuente_grande.render(f'¡{ganador} GANA!', True, BLANCO)
        jugar_otra = fuente.render('1 - Jugar otra vez', True, BLANCO)
        menu_principal = fuente.render('2 - Menú Principal', True, BLANCO)
        salir = fuente.render('ESC - Salir', True, BLANCO)

        pantalla.blit(texto_ganador, (ANCHO//2 - texto_ganador.get_width()//2, 100))
        pantalla.blit(jugar_otra, (ANCHO//2 - jugar_otra.get_width()//2, 300))
        pantalla.blit(menu_principal, (ANCHO//2 - menu_principal.get_width()//2, 350))
        pantalla.blit(salir, (ANCHO//2 - salir.get_width()//2, 400))

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "salir"
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_1:
                    return "jugar_otra"
                if evento.key == pygame.K_2:
                    return "menu"
                if evento.key == pygame.K_ESCAPE:
                    return "salir"

# Bucle principal
ejecutando = True
while ejecutando:
    # Mostrar menú y obtener modo de juego
    modo_juego = mostrar_menu()
    if modo_juego is None:
        break

    # Inicializar elementos del juego
    paleta_izq = pygame.Rect(50, ALTO//2 - PALETA_ALTO//2, PALETA_ANCHO, PALETA_ALTO)
    paleta_der = pygame.Rect(ANCHO - 50 - PALETA_ANCHO, ALTO//2 - PALETA_ALTO//2, PALETA_ANCHO, PALETA_ALTO)
    pelota = pygame.Rect(ANCHO//2 - 15//2, ALTO//2 - 15//2, 15, 15)
    
    # En la sección donde se inicializan las variables del juego:
    velocidad_paleta = 5
    velocidad_x, velocidad_y = reiniciar_pelota('izq')  # Primer saque hacia la izquierda
    
    puntos_izq = 0
    puntos_der = 0

    # Bucle del juego
    jugando = True
    while jugando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
                jugando = False

        teclas = pygame.key.get_pressed()
        
        # Movimiento paleta izquierda
        if teclas[pygame.K_w] and paleta_izq.top > 0:
            paleta_izq.y -= velocidad_paleta
        if teclas[pygame.K_s] and paleta_izq.bottom < ALTO:
            paleta_izq.y += velocidad_paleta

        # Movimiento paleta derecha
        if modo_juego == 2:  # Dos jugadores
            if teclas[pygame.K_UP] and paleta_der.top > 0:
                paleta_der.y -= velocidad_paleta
            if teclas[pygame.K_DOWN] and paleta_der.bottom < ALTO:
                paleta_der.y += velocidad_paleta
        else:  # Un jugador (IA)
            mover_ia(paleta_der, pelota)

        # Movimiento de la pelota
        pelota.x += velocidad_x
        pelota.y += velocidad_y

        # Colisiones
        if pelota.top <= 0 or pelota.bottom >= ALTO:
            velocidad_y *= -1
        # Colisiones con las paletas
        if pelota.colliderect(paleta_izq) or pelota.colliderect(paleta_der):
            velocidad_x *= -1
            
            # Aumentar la velocidad gradualmente en modo un jugador
            if modo_juego == 1:
                velocidad_x *= INCREMENTO_VELOCIDAD
                velocidad_y *= INCREMENTO_VELOCIDAD
                
            # Variar el ángulo según donde golpee la pelota en la paleta
            if pelota.colliderect(paleta_izq):
                relativo_y = (pelota.centery - paleta_izq.centery) / (PALETA_ALTO/2)
                velocidad_y = relativo_y * abs(velocidad_x)
            else:
                relativo_y = (pelota.centery - paleta_der.centery) / (PALETA_ALTO/2)
                velocidad_y = relativo_y * abs(velocidad_x)

        # Sistema de puntuación
        if pelota.left <= 0:
            puntos_der += 1
            velocidad_x, velocidad_y = reiniciar_pelota('der')
            # Pausa breve antes del siguiente saque
            pygame.time.wait(1000)
        elif pelota.right >= ANCHO:
            puntos_izq += 1
            velocidad_x, velocidad_y = reiniciar_pelota('izq')
            # Pausa breve antes del siguiente saque
            pygame.time.wait(1000)

        # Verificar victoria
        if puntos_izq >= PUNTOS_VICTORIA or puntos_der >= PUNTOS_VICTORIA:
            ganador = "JUGADOR 1" if puntos_izq >= PUNTOS_VICTORIA else "JUGADOR 2"
            if modo_juego == 1 and ganador == "JUGADOR 2":
                ganador = "CPU"
            
            # Mostrar menú post-partida y procesar la elección
            eleccion = mostrar_menu_post_partida(ganador)
            if eleccion == "jugar_otra":
                # Reiniciar el juego con el mismo modo
                puntos_izq = 0
                puntos_der = 0
                velocidad_x, velocidad_y = reiniciar_pelota('izq')
                paleta_izq.centery = ALTO//2
                paleta_der.centery = ALTO//2
            elif eleccion == "menu":
                jugando = False  # Volver al menú principal
            else:  # "salir"
                jugando = False
                ejecutando = False

        # Dibujar elementos
        pantalla.fill(NEGRO)
        pygame.draw.rect(pantalla, BLANCO, paleta_izq)
        pygame.draw.rect(pantalla, BLANCO, paleta_der)
        pygame.draw.ellipse(pantalla, BLANCO, pelota)
        pygame.draw.aaline(pantalla, BLANCO, (ANCHO//2, 0), (ANCHO//2, ALTO))

        # Mostrar puntuación
        texto_izq = fuente.render(str(puntos_izq), True, BLANCO)
        texto_der = fuente.render(str(puntos_der), True, BLANCO)
        pantalla.blit(texto_izq, (ANCHO//4, 20))
        pantalla.blit(texto_der, (3*ANCHO//4, 20))

        pygame.display.flip()
        reloj.tick(60)

pygame.quit()