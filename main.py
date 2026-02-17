import pygame
import sys
import random


pygame.init()
# CONFIGURACIÓN DEL JUEGO.
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SALVA LA PELOTA")

background = pygame.image.load("assets/fondo_juego.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))


clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)

# VARIABLES DEL JUEGO.
ball_pos = [400, 300]
ball_speed = [5, -5]
ball_radius = 12

paddle = pygame.Rect(350, 560, 120, 15)

blocks = []
score = 0
game_state = "menu"

# FUNCIONES DEL JUEGO 

def create_blocks():
    blocks.clear()
    for row in range(4):
        for col in range(8):
            blocks.append(
                pygame.Rect(80*col+60, 60*row+40, 70, 25)
            )


def draw_text(text, x, y):
    img = font.render(text, True, (0,0,0))
    screen.blit(img, (x, y))


def move_ball():
    global game_state

    ball_pos[0] += ball_speed[0]
    ball_pos[1] += ball_speed[1]

    # Rebote de las paredes laterales
    if ball_pos[0] <= 0 or ball_pos[0] >= WIDTH:
        ball_speed[0] *= -1

    # Rebote del techo
    if ball_pos[1] <= 0:
        ball_speed[1] *= -1

    # condicional de si Pierde o toca abajo
    if ball_pos[1] >= HEIGHT:
        game_state = "game_over"


def paddle_collision():
    ball_rect = pygame.Rect(
        ball_pos[0]-ball_radius,
        ball_pos[1]-ball_radius,
        ball_radius*2,
        ball_radius*2
    )

    if ball_rect.colliderect(paddle):
        ball_speed[1] *= -1


def block_collision():
    global score
    ball_rect = pygame.Rect(
        ball_pos[0]-ball_radius,
        ball_pos[1]-ball_radius,
        ball_radius*2,
        ball_radius*2
    )

    for block in blocks[:]:
        if ball_rect.colliderect(block):
            blocks.remove(block)
            ball_speed[1] *= -1
            score += 10
            break


def draw_objects():
    pygame.draw.circle(screen, (84, 59, 227),
                       ball_pos, ball_radius)

    pygame.draw.rect(screen, (0,0,0), paddle)

    for block in blocks:
        pygame.draw.rect(screen, (193, 154, 107), block)


def reset_game():
    global ball_pos, ball_speed, score, game_state
    ball_pos = [400, 300]
    ball_speed = [random.choice([-5,5]), -5]
    score = 0
    create_blocks()
    game_state = "playing"


def menu():
    screen.fill((0,0,0))
    screen.blit(background, (0, 0))
    draw_text("SALVA LA PELOTA", 300, 220)
    draw_text("Presiona ENTER para JUGAR", 220, 300)


def game_over():
    screen.fill((0,0,0))
    screen.blit(background, (0, 0))
    draw_text("GAME OVER", 320, 240)
    draw_text(f"Puntaje: {score}", 330, 290)
    draw_text("Presiona R para reiniciar", 220, 340)


# -------- LOOP PRINCIPAL --------

create_blocks()

while True:
    screen.fill((0,0,0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if game_state == "menu" and event.key == pygame.K_RETURN:
                reset_game()

            if game_state == "game_over" and event.key == pygame.K_r:
                reset_game()

    keys = pygame.key.get_pressed()

    # -------- ESTADOS --------
    if game_state == "menu":
        menu()

    elif game_state == "playing":

        if keys[pygame.K_LEFT]:
            paddle.x -= 7
        if keys[pygame.K_RIGHT]:
            paddle.x += 7

        screen.blit(background, (0, 0))

        move_ball()
        paddle_collision()
        block_collision()

        draw_objects()
        draw_text(f"Puntos: {score}", 10, 10)

    elif game_state == "game_over":
        game_over()

    pygame.display.update()
    clock.tick(60)