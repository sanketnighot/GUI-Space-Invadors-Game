import pygame
import random
import math
from pygame import mixer

# Initialize the pygame
pygame.init()

mixer.music.load('background.wav')
mixer.music.play(-1)

# Create the Screen
screen = pygame.display.set_mode((800, 600))

# Title and Icon and Background
pygame.display.set_caption("Space Invadors by @SanketNighot")
icon = pygame.image.load("spaceship.png")
background = pygame.image.load("background.png")

pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load("player.png")
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 10
choice = [3, -3]

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(random.choice(choice))
    enemyY_change.append(20)

# Bullet
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bulletState = "ready"

score_value = 0
font = pygame.font.Font('Cyberpunks.ttf', 40)
overfont = pygame.font.Font('Cyberpunks.ttf', 60)

textX = 10
textY = 10


def showScore(x, y):
    score = font.render(f"Score: {score_value}", True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_txt = overfont.render("GAME OVER", True, (255, 255, 255))
    over_txt2 = overfont.render(f"Your Score is {score_value}", True, (255, 255, 255))
    screen.blit(over_txt2, (210, 245))
    screen.blit(over_txt, (275, 180))


def fire_bullet(x, y):
    global bulletState
    bulletState = "fire"
    screen.blit(bulletImg, (x + 20, y + 10))


def player(x, y):
    screen.blit(playerImg, (playerX, playerY))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (enemyX[i], enemyY[i]))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))

    if distance < 28:
        return True
    else:
        return False


# Game Loop
running = True
while running:

    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    showScore(textX, textY)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Key Strokes
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -3

            if event.key == pygame.K_RIGHT:
                playerX_change = 3

            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                if bulletState == "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    fire_bullet(playerX, bulletY)
                    bulletX = playerX

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                playerX_change = 0

    playerX += playerX_change

    if playerX < 0:
        playerX = 0
    elif playerX > 736:
        playerX = 736

    for i in range(num_of_enemies):

        if enemyY[i] > 460:
            for j in range(num_of_enemies):
                enemyY[j] = 2000

            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] < 0:
            enemyX_change[i] = 3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] > 736:
            enemyX_change[i] = -3
            enemyY[i] += enemyY_change[i]

        if isCollision(enemyX[i], enemyY[i], bulletX, bulletY):
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            score_value += 5

            bulletState = "ready"
            bulletX = 0
            bulletY = 480
            enemyX_change[i] = random.choice(choice)
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    if bulletState == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    if bulletY < 0:
        bulletState = "ready"
        bulletX = 0
        bulletY = 480

    player(playerX, playerY)
    showScore(textX, textY)
    pygame.display.update()
