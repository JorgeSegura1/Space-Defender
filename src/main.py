
import pygame
import random
import sys
from pygame.locals import (
    QUIT, KEYDOWN, MOUSEMOTION, MOUSEBUTTONDOWN,
    K_UP, K_DOWN, K_LEFT, K_RIGHT,
    K_RETURN, K_SPACE, K_p
)

# -----------------------------------
# CONFIGURACIÓN DE NIVELES, PUNTOS Y VIDAS
# -----------------------------------
POINTS_PER_LEVEL = 50
INITIAL_LIVES   = 3

# Inicialización de Pygame
def init_pygame(width=800, height=600, title="Space Defender"):
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(title)
    return screen

# Menú principal (teclado + ratón)
def show_main_menu(screen):
    font     = pygame.font.SysFont(None, 48)
    options  = ["Jugar", "Instrucciones", "Salir"]
    selected = 0
    clock    = pygame.time.Clock()

    while True:
        screen.fill((0, 0, 0))
        labels = []
        # dibujar opciones y guardar rects
        for i, text in enumerate(options):
            color = (255,255,0) if i==selected else (255,255,255)
            label = font.render(text, True, color)
            rect  = label.get_rect(center=(400, 200 + i*60))
            screen.blit(label, rect)
            labels.append(rect)
        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                sys.exit()

            # teclado
            if e.type == KEYDOWN:
                if e.key == K_UP:
                    selected = (selected - 1) % len(options)
                elif e.key == K_DOWN:
                    selected = (selected + 1) % len(options)
                elif e.key in (K_RETURN, pygame.K_KP_ENTER):
                    return options[selected]

            # ratón: hover
            if e.type == MOUSEMOTION:
                mx, my = e.pos
                for i, rect in enumerate(labels):
                    if rect.collidepoint(mx, my):
                        selected = i
            # ratón: click
            if e.type == MOUSEBUTTONDOWN and e.button == 1:
                mx, my = e.pos
                for i, rect in enumerate(labels):
                    if rect.collidepoint(mx, my):
                        return options[i]

        clock.tick(30)

# Pantalla de instrucciones
def show_instructions(screen):
    font_title = pygame.font.SysFont(None, 56)
    font_text  = pygame.font.SysFont(None, 32)
    title_surf = font_title.render("Instrucciones", True, (255,255,0))
    lines = [
        "Cómo jugar",
        "Mueve la nave con las flechas del teclado ← →",
        "Dispara con ESPACIO",
        "Pausa con P",
        "Elimina enemigos antes de que lleguen abajo",
        "Pierdes una vida por cada enemigo que escape",
        "Presiona cualquier tecla o click para volver"
    ]
    text_surfs = [font_text.render(line, True, (255,255,255)) for line in lines]
    clock = pygame.time.Clock()

    while True:
        screen.fill((0,0,0))
        screen.blit(title_surf, (300, 100))
        for i, surf in enumerate(text_surfs):
            screen.blit(surf, (200, 180 + i*40))
        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                sys.exit()
            # vuelve con cualquier tecla o click
            if e.type == KEYDOWN or (e.type == MOUSEBUTTONDOWN and e.button == 1):
                return
        clock.tick(30)

# Clase para enemigos
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        self.image = pygame.Surface((40,30))
        self.image.fill((255,0,0))
        self.rect  = self.image.get_rect(topleft=(x,y))
        self.speed = speed

    def update(self):
        self.rect.y += self.speed

# Generar enemigos
def spawn_enemies(group, num, speed):
    for _ in range(num):
        x = random.randint(0, 760)
        y = random.randint(-150, -40)
        group.add(Enemy(x, y, speed))

# Menú de pausa
def show_pause_menu(screen):
    font      = pygame.font.SysFont(None, 48)
    label     = font.render("Pausa - Presiona P para continuar", True, (255,255,255))
    clock     = pygame.time.Clock()

    while True:
        screen.fill((0,0,0))
        screen.blit(label, (100,300))
        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                sys.exit()
            if e.type == KEYDOWN and e.key == K_p:
                return
        clock.tick(30)

# Pantalla de Game Over
def game_over(screen, score):
    font1 = pygame.font.SysFont(None, 64)
    font2 = pygame.font.SysFont(None, 36)
    over_surf = font1.render("¡Game Over!", True, (255,0,0))
    score_surf= font2.render(f"Puntuación final: {score}", True, (255,255,255))
    clock = pygame.time.Clock()

    while True:
        screen.fill((0,0,0))
        screen.blit(over_surf,  (250,200))
        screen.blit(score_surf, (250,300))
        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                sys.exit()
            if e.type == KEYDOWN or (e.type==MOUSEBUTTONDOWN and e.button==1):
                return
        clock.tick(30)

# Lógica principal de juego
def play_game(screen):
    clock   = pygame.time.Clock()
    player  = pygame.Rect(370,500,60,40)
    bullets = []
    enemies = pygame.sprite.Group()
    score   = 0
    level   = 1
    lives   = INITIAL_LIVES

    spawn_enemies(enemies, level*5, 1 + 0.2*level)
    running = True

    while running:
        # eventos
        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                sys.exit()
            if e.type == KEYDOWN and e.key == K_p:
                show_pause_menu(screen)

        # movimiento jugador
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]   and player.left > 0:
            player.x -= 5
        if keys[K_RIGHT]  and player.right < 800:
            player.x += 5
        if keys[K_SPACE]:
            bullets.append(pygame.Rect(player.centerx-2, player.top, 4,10))

        # actualizar balas
        for b in bullets[:]:
            b.y -= 7
            if b.y < 0:
                if b in bullets: bullets.remove(b)
            else:
                for en in enemies:
                    if en.rect.colliderect(b):
                        en.kill()
                        score += 10
                        if b in bullets: bullets.remove(b)
                        break

        # mover enemigos y quitar vidas si escapan
        for en in enemies.copy():
            en.update()
            if en.rect.top > 600:
                en.kill()
                lives -= 1
                if lives <= 0:
                    running = False

        # subir nivel por puntos
        if score >= level * POINTS_PER_LEVEL:
            level += 1
            spawn_enemies(enemies, level*5, 1 + 0.2*level)

        # subir nivel por oleada vacía
        if len(enemies)==0 and running:
            level += 1
            spawn_enemies(enemies, level*5, 1 + 0.2*level)

        # dibujado
        screen.fill((0,0,20))
        pygame.draw.rect(screen, (0,255,0), player)
        for b in bullets:
            pygame.draw.rect(screen, (255,255,0), b)
        enemies.draw(screen)

        font = pygame.font.SysFont(None,36)
        screen.blit(font.render(f"Puntos: {score}", True, (255,255,255)), (10,10))
        screen.blit(font.render(f"Nivel:  {level}", True, (255,255,255)), (10,50))
        screen.blit(font.render(f"Vidas:  {lives}", True, (255,255,255)), (10,90))

        pygame.display.flip()
        clock.tick(60)

    game_over(screen, score)

# Punto de entrada
def main():
    screen = init_pygame()
    while True:
        opcion = show_main_menu(screen)
        if opcion == "Jugar":
            play_game(screen)
        elif opcion == "Instrucciones":
            show_instructions(screen)
        else:  # Salir
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    main()
