import pygame
import sys
import random

# --- CONFIGURACIÓN ---
ANCHO, ALTO = 960, 540
FPS = 60

# Colores
AZUL = (30, 30, 60)
AZUL_CLARO = (50, 50, 80)
VERDE = (100, 200, 120)
VERDE_OSCURO = (70, 160, 90)
ROJO = (255, 80, 80)
AMARILLO = (255, 215, 80)
NEGRO = (0, 0, 0)
MARRON = (139, 69, 19)
CAFE = (160, 120, 80)
CAFE_CLARO = (200, 160, 100)
BLANCO = (255, 255, 255)

# Físicas
GRAVEDAD = 0.5
FUERZA_SALTO = -14
VELOCIDAD = 7

# Posición inicial
INICIO_X = 100
INICIO_Y = 400


class Jugador:
    def __init__(self):
        self.x = INICIO_X
        self.y = INICIO_Y
        self.w = 30
        self.h = 40
        self.vx = 0
        self.vy = 0
        self.en_suelo = False

    def mover(self, teclas):
        if (teclas[pygame.K_SPACE] or teclas[pygame.K_UP] or teclas[pygame.K_w]) and self.en_suelo:
            self.vy = FUERZA_SALTO
            self.en_suelo = False

        self.vx = 0
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.vx = -VELOCIDAD
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.vx = VELOCIDAD

    def actualizar(self, plataformas):
        self.vy += GRAVEDAD
        if self.vy > 15:
            self.vy = 15

        self.x += self.vx
        rect = pygame.Rect(self.x, self.y, self.w, self.h)
        for p in plataformas:
            if rect.colliderect(p):
                if self.vx > 0:
                    self.x = p.left - self.w
                elif self.vx < 0:
                    self.x = p.right

        self.y += self.vy
        self.en_suelo = False
        rect = pygame.Rect(self.x, self.y, self.w, self.h)
        for p in plataformas:
            if rect.colliderect(p):
                if self.vy > 0:
                    self.y = p.top - self.h
                    self.vy = 0
                    self.en_suelo = True
                elif self.vy < 0:
                    self.y = p.bottom
                    self.vy = 0

        if self.y > ALTO + 100:
            return True
        return False

    def reiniciar(self):
        self.x = INICIO_X
        self.y = INICIO_Y
        self.vx = 0
        self.vy = 0
        self.en_suelo = False

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)

    def dibujar(self, pantalla):
        pygame.draw.rect(pantalla, ROJO, (self.x, self.y, self.w, self.h))


class HoyoFalso:
    def __init__(self, x, y, ancho, alto):
        self.x_inicial = x
        self.x = x
        self.y = y
        self.ancho = ancho
        self.alto = alto
        self.moviendo = False
        self.objetivo_x = 0
        self.velocidad = 20

    def activar(self, objetivo_x):
        if not self.moviendo:
            self.moviendo = True
            self.objetivo_x = objetivo_x

    def mover(self):
        if self.moviendo:
            if self.x < self.objetivo_x:
                self.x += self.velocidad
                if self.x >= self.objetivo_x:
                    self.x = self.objetivo_x
                    self.moviendo = False
            elif self.x > self.objetivo_x:
                self.x -= self.velocidad
                if self.x <= self.objetivo_x:
                    self.x = self.objetivo_x
                    self.moviendo = False

    def reiniciar(self):
        self.x = self.x_inicial
        self.moviendo = False
        self.objetivo_x = 0

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.ancho, self.alto)

    def dibujar(self, pantalla):
        rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        pygame.draw.rect(pantalla, AZUL, rect)
        pygame.draw.rect(pantalla, AZUL_CLARO, rect, 2)


class HoyoVerdadero:
    def __init__(self, x, y, ancho, alto):
        self.x = x
        self.y = y
        self.ancho = ancho
        self.alto = alto
        self.activo = True

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.ancho, self.alto)

    def dibujar(self, pantalla):
        pygame.draw.rect(pantalla, VERDE, (self.x, self.y, self.ancho, self.alto))


class ParticulaDerrumbe:
    def __init__(self, x, y):
        self.x = x + random.randint(-20, 20)
        self.y = y
        self.tamano = random.randint(3, 8)
        self.vel_x = random.uniform(-2, 2)
        self.vel_y = random.uniform(1, 4)
        self.gravedad = 0.1
        self.color = random.choice([MARRON, CAFE, CAFE_CLARO, VERDE_OSCURO])
        self.vida = 60

    def actualizar(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.vel_y += self.gravedad
        self.vida -= 1
        return self.vida > 0

    def dibujar(self, pantalla):
        if self.vida > 0:
            pygame.draw.circle(pantalla, self.color, (int(self.x), int(self.y)), self.tamano)


def dibujar_derrumbe(pantalla, x, y, ancho, alto, progreso):
    ancho_actual = int(ancho * (0.2 + 0.8 * progreso))
    alto_actual = int(alto * (0.2 + 0.8 * progreso))
    offset_x = (ancho - ancho_actual) // 2
    offset_y = (alto - alto_actual) // 2
    
    oscuridad = int(50 + 150 * progreso)
    color_hoyo = (oscuridad, oscuridad, oscuridad + 20)
    
    pygame.draw.rect(pantalla, color_hoyo, (x + offset_x, y + offset_y, ancho_actual, alto_actual))
    
    if progreso > 0.1:
        for i in range(int(5 + 10 * progreso)):
            bx = x + random.randint(0, ancho)
            by = y + random.randint(0, alto)
            size = random.randint(2, 5)
            color_tierra = random.choice([MARRON, CAFE, CAFE_CLARO])
            pygame.draw.rect(pantalla, color_tierra, (bx, by, size, size))


def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    reloj = pygame.time.Clock()
    fuente = pygame.font.Font(None, 36)
    fuente_peq = pygame.font.Font(None, 24)
    fuente_grande = pygame.font.Font(None, 72)

    jugador = Jugador()
    
    nivel_actual = 1
    transicionando = False
    tiempo_transicion = 0
    
    mostrar_felicidades = False
    tiempo_felicidades = 0
    
    # --- NIVEL 1 ---
    suelo_izq_n1 = pygame.Rect(0, ALTO - 40, 550, 40)
    suelo_der_n1 = pygame.Rect(710, ALTO - 40, 250, 40)
    trampa_x = 550
    trampa_y = ALTO - 40
    trampa_w = 160
    trampa_h = 40
    trampa_visible = True
    trampa_abierta = False
    tiempo_apertura = 0
    animacion_progreso = 0.0
    animacion_duracion = 270
    particulas_n1 = []
    generar_particulas = False
    posicion_activacion = trampa_x - 10
    
    # --- NIVEL 2 ---
    suelo_izq_n2 = pygame.Rect(0, ALTO - 40, 430, 40)
    suelo_der_n2 = pygame.Rect(590, ALTO - 40, 370, 40)
    
    hoyo_verdadero = HoyoVerdadero(430, ALTO - 40, 160, 40)
    hoyo_falso = HoyoFalso(680, ALTO - 40, 160, 40)
    hoyo_falso_activado = False
    posicion_centro = 430
    
    puerta = pygame.Rect(850, ALTO - 140, 80, 100)

    def reiniciar_nivel_1():
        nonlocal trampa_visible, trampa_abierta, tiempo_apertura, animacion_progreso, particulas_n1, generar_particulas
        jugador.reiniciar()
        trampa_visible = True
        trampa_abierta = False
        tiempo_apertura = 0
        animacion_progreso = 0.0
        particulas_n1 = []
        generar_particulas = False

    def reiniciar_nivel_2():
        nonlocal hoyo_falso_activado, mostrar_felicidades
        jugador.reiniciar()
        hoyo_falso.reiniciar()
        hoyo_falso_activado = False
        mostrar_felicidades = False

    def reiniciar_nivel():
        if nivel_actual == 1:
            reiniciar_nivel_1()
        else:
            reiniciar_nivel_2()

    def cambiar_nivel(nuevo_nivel):
        nonlocal nivel_actual, transicionando, tiempo_transicion, hoyo_falso_activado, mostrar_felicidades
        nivel_actual = nuevo_nivel
        transicionando = True
        tiempo_transicion = pygame.time.get_ticks()
        mostrar_felicidades = False
        
        if nivel_actual == 1:
            pygame.display.set_caption("Trollus - Nivel 1: Confianza")
            reiniciar_nivel_1()
        else:
            pygame.display.set_caption("Trollus - Nivel 2: Hoyo Persecutor")
            reiniciar_nivel_2()
            hoyo_falso_activado = False

    pygame.display.set_caption("Trollus - Nivel 1: Confianza")

    corriendo = True
    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    corriendo = False
                if evento.key == pygame.K_r:
                    reiniciar_nivel()
                    mostrar_felicidades = False
                if evento.key == pygame.K_1:
                    cambiar_nivel(1)
                if evento.key == pygame.K_2:
                    cambiar_nivel(2)

        if transicionando:
            if pygame.time.get_ticks() - tiempo_transicion > 300:
                transicionando = False
            pygame.display.flip()
            reloj.tick(FPS)
            continue

        teclas = pygame.key.get_pressed()
        jugador.mover(teclas)

        if nivel_actual == 1:
            # --- NIVEL 1 ---
            plataformas = [suelo_izq_n1, suelo_der_n1]
            if trampa_visible:
                plataformas.append(pygame.Rect(trampa_x, trampa_y, trampa_w, trampa_h))
            
            if jugador.actualizar(plataformas):
                reiniciar_nivel_1()
            
            tiempo = pygame.time.get_ticks()
            centro_x = jugador.x + jugador.w / 2
            
            if trampa_visible and not trampa_abierta:
                if centro_x >= posicion_activacion:
                    trampa_abierta = True
                    tiempo_apertura = tiempo
                    generar_particulas = True
            
            if trampa_abierta and trampa_visible:
                tiempo_transcurrido = tiempo - tiempo_apertura
                animacion_progreso = min(1.0, tiempo_transcurrido / animacion_duracion)
                
                if generar_particulas and animacion_progreso < 0.8:
                    for _ in range(3):
                        px = trampa_x + random.randint(0, trampa_w)
                        py = trampa_y + random.randint(-10, 5)
                        particulas_n1.append(ParticulaDerrumbe(px, py))
                
                if animacion_progreso >= 1.0:
                    trampa_visible = False
                    generar_particulas = False
            
            particulas_n1 = [p for p in particulas_n1 if p.actualizar()]

        else:
            # --- NIVEL 2 ---
            centro_jugador = jugador.x + jugador.w / 2
            
            if not hoyo_falso_activado and centro_jugador >= posicion_centro:
                hoyo_falso_activado = True
                hoyo_falso.activar(hoyo_verdadero.x)
            
            if hoyo_falso_activado:
                hoyo_falso.mover()
            
            plataformas = []
            
            if suelo_izq_n2.right <= hoyo_verdadero.x:
                plataformas.append(suelo_izq_n2)
            else:
                if suelo_izq_n2.left < hoyo_verdadero.x:
                    plataformas.append(pygame.Rect(suelo_izq_n2.left, suelo_izq_n2.top, hoyo_verdadero.x - suelo_izq_n2.left, suelo_izq_n2.height))
            
            if suelo_der_n2.left >= hoyo_verdadero.x + hoyo_verdadero.ancho:
                plataformas.append(suelo_der_n2)
            else:
                if suelo_der_n2.right > hoyo_verdadero.x + hoyo_verdadero.ancho:
                    plataformas.append(pygame.Rect(hoyo_verdadero.x + hoyo_verdadero.ancho, suelo_der_n2.top, suelo_der_n2.right - (hoyo_verdadero.x + hoyo_verdadero.ancho), suelo_der_n2.height))
            
            if jugador.actualizar(plataformas):
                reiniciar_nivel_2()
            
            rect_jugador = jugador.get_rect()
            rect_hoyo_verdadero = hoyo_verdadero.get_rect()
            
            if rect_jugador.colliderect(rect_hoyo_verdadero) and jugador.en_suelo:
                reiniciar_nivel_2()
                pygame.display.flip()
                reloj.tick(FPS)
                continue

        # --- Verificar puerta ---
        if jugador.get_rect().colliderect(puerta):
            if nivel_actual == 1:
                cambiar_nivel(2)
            else:
                if not mostrar_felicidades:
                    mostrar_felicidades = True
                    tiempo_felicidades = pygame.time.get_ticks()

        # --- Actualizar tiempo de felicitaciones ---
        if mostrar_felicidades:
            if pygame.time.get_ticks() - tiempo_felicidades > 2000:
                mostrar_felicidades = False

        # --- DIBUJAR ---
        pantalla.fill(AZUL)

        if nivel_actual == 1:
            pygame.draw.rect(pantalla, VERDE, suelo_izq_n1)
            pygame.draw.rect(pantalla, VERDE, suelo_der_n1)
            
            if trampa_visible:
                if trampa_abierta:
                    dibujar_derrumbe(pantalla, trampa_x, trampa_y, trampa_w, trampa_h, animacion_progreso)
                else:
                    pygame.draw.rect(pantalla, VERDE, (trampa_x, trampa_y, trampa_w, trampa_h))
            
            for p in particulas_n1:
                p.dibujar(pantalla)
            
            titulo = fuente.render("Nivel 1: Confianza", True, BLANCO)

        else:
            pygame.draw.rect(pantalla, VERDE, suelo_izq_n2)
            pygame.draw.rect(pantalla, VERDE, suelo_der_n2)
            hoyo_verdadero.dibujar(pantalla)
            hoyo_falso.dibujar(pantalla)
            titulo = fuente.render("Nivel 2: Hoyo Persecutor", True, BLANCO)

        # --- ELEMENTOS COMUNES ---
        pygame.draw.rect(pantalla, AMARILLO, puerta)
        jugador.dibujar(pantalla)

        pantalla.blit(titulo, (20, 16))
        ayuda = fuente_peq.render("A/D mover | Espacio saltar | R reiniciar | 1/2 cambiar nivel", True, (200, 200, 200))
        pantalla.blit(ayuda, (20, 50))

        texto_nivel = fuente_peq.render(f"Nivel: {nivel_actual}", True, (200, 200, 200))
        pantalla.blit(texto_nivel, (ANCHO - 120, 20))

        # --- MOSTRAR FELICIDADES ---
        if mostrar_felicidades:
            overlay = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 100))
            pantalla.blit(overlay, (0, 0))
            
            feliz_text = fuente_grande.render("FELICIDADES", True, (255, 215, 0))
            feliz_rect = feliz_text.get_rect(center=(ANCHO//2, ALTO//2))
            pantalla.blit(feliz_text, feliz_rect)

        if transicionando:
            trans_text = fuente.render(f"NIVEL {nivel_actual}", True, (255, 215, 0))
            pantalla.blit(trans_text, (ANCHO//2 - 100, ALTO//2 - 50))

        pygame.display.flip()
        reloj.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()