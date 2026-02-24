import pygame
import random

# ---------------- INITIAL SETUP ----------------
pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1000, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch Peppa")

clock = pygame.time.Clock()

# colors
WHITE = (255, 255, 255)
RED = (220, 20, 60)
BROWN = (139, 69, 19)
BLACK = (30, 30, 30)

# ---------------- ASSETS ----------------
bg_img = pygame.image.load("background.jpg").convert()
bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))


apple_img = pygame.image.load("apple.png").convert_alpha()
APPLE_SIZE = 100
apple_img = pygame.transform.scale(apple_img, (APPLE_SIZE, APPLE_SIZE))

# ---------------- GAME VARIABLES ----------------
APPLE_RADIUS = 25
APPLE_SPEED = 4

BOWL_WIDTH = 100
BOWL_HEIGHT = 35
bowl_img = pygame.image.load("bowl.png").convert_alpha()
bowl_img = pygame.transform.scale(bowl_img, (BOWL_WIDTH, BOWL_HEIGHT))

BOWL_SPEED = 6

LIVES = 3
lives = LIVES
score = 0
game_over = False

# apple position
apple_x = random.randint(20, WIDTH - 20)
apple_y = 0

# bowl position
bowl_x = WIDTH // 2
bowl_y = HEIGHT - 40

# font
font = pygame.font.SysFont(None, 36)

# sounds (make sure these files exist in the same folder)
catch_sound = pygame.mixer.Sound("catch.wav")
miss_sound = pygame.mixer.Sound("miss.wav")
gameover_sound = pygame.mixer.Sound("missed.wav")

# background music (uses mixer.music for continuous playback)
pygame.mixer.music.load("background-music.wav")
pygame.mixer.music.set_volume(0.5)  # adjust volume if needed (0.0 to 1.0)
pygame.mixer.music.play(-1)  # -1 means loop forever

# ---------------- FUNCTIONS ----------------
def reset_apple():
    global apple_x, apple_y
    apple_x = random.randint(20, WIDTH - 20)
    apple_y = 0

def draw_score():
    text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(text, (10, 10))

def draw_lives():
    text = font.render(f"Lives: {lives}", True, BLACK)
    screen.blit(text, (WIDTH - 140, 10))

def draw_game_over():
    over_text = font.render("GAME OVER", True, (200, 0, 0))
    info_text = font.render("Press R to Restart", True, BLACK)
    screen.blit(over_text, (WIDTH // 2 - 90, HEIGHT // 2 - 20))
    screen.blit(info_text, (WIDTH // 2 - 120, HEIGHT // 2 + 20))

# ---------------- GAME LOOP ----------------
running = True
while running:
    clock.tick(60)
    screen.blit(bg_img, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # -------- RESTART GAME --------
    if game_over:
        if keys[pygame.K_r]:
            score = 0
            lives = LIVES
            game_over = False
            reset_apple()
            pygame.mixer.music.set_volume(0.5)  # restore normal volume
    else:
        # -------- BOWL MOVEMENT --------
        if keys[pygame.K_LEFT]:
            bowl_x -= BOWL_SPEED
        if keys[pygame.K_RIGHT]:
            bowl_x += BOWL_SPEED

        bowl_x = max(0, min(WIDTH - BOWL_WIDTH, bowl_x))

       
        apple_y += APPLE_SPEED

        
        apple_rect = pygame.Rect(
            apple_x - APPLE_SIZE // 2,
            apple_y - APPLE_SIZE // 2,
            APPLE_SIZE,
            APPLE_SIZE
        )
        bowl_rect = pygame.Rect(bowl_x, bowl_y, BOWL_WIDTH, BOWL_HEIGHT)

        if apple_rect.colliderect(bowl_rect):
            score += 1
            catch_sound.play()
            reset_apple()

      
        if apple_y > HEIGHT:
            lives -= 1
            miss_sound.play()
            reset_apple()
            if lives == 0:
                game_over = True
                pygame.mixer.music.set_volume(0.05)  # instantly lower volume
                gameover_sound.play()

 
    screen.blit(apple_img, (apple_x - APPLE_SIZE // 2, apple_y - APPLE_SIZE // 2))
    screen.blit(bowl_img, (bowl_x, bowl_y))

    draw_score()
    draw_lives()

    if game_over:
        draw_game_over()

    pygame.display.flip()

pygame.quit()