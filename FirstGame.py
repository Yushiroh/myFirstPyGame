import os
import random
import pygame
import sys

# Essentials Parameters
win_W, win_H = 300, 600
gameWindow = pygame.display.set_mode((win_W, win_H))
pygame.display.set_caption("DodgyBalls")
gameFPS = 60
pygame.init()

# Color Lists
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLACK = (0,0,0)


# Game Assets
gameFont = pygame.font.SysFont('arial', 40)
playerSpeed = 5
debrisSpeed = 5
debrisAllowed = 20
bulletSpeed= 20
playerHit = pygame.USEREVENT + 1

# Extra Functions
def draw_window(playerBox, debrisSpawner, playerAmmo, playerHealth, playerScore):
    gameWindow.fill(YELLOW)
    pygame.draw.rect(gameWindow, BLACK, (playerBox.x, playerBox.y, 20, 20))
    playerHealth_display = gameFont.render("HP: " + str(playerHealth), 1, BLACK)
    gameWindow.blit(playerHealth_display,(0,0, 20, 20))

    for debris in debrisSpawner:
        pygame.draw.rect(gameWindow, RED, (debris.x, debris.y, 20, 20))

    for bullet in playerAmmo:
        pygame.draw.rect(gameWindow, BLACK, (bullet.x, bullet.y, 10,10))

    if playerHealth <= 0:
        pygame.draw.rect(gameWindow, BLACK, (0, 0, win_W, win_H))
        gameOverDisplay = gameFont.render("GAME OVER", 1, YELLOW)
        restartText = gameFont.render("Press R to Restart", 1, YELLOW)
        scoreText = gameFont.render("Score: " + str(playerScore), 1, YELLOW)
        gameWindow.blit(gameOverDisplay, (60, win_H/2, 20, 20))
        gameWindow.blit(restartText, (25, win_H/2 + 40, 20, 20))
        gameWindow.blit(scoreText, (60, win_H / 2 + 80, 20, 20))



    pygame.display.update()


def playerMovement(keyInput, playerBox, playerSpeed):
    if keyInput[pygame.K_a] and playerBox.x > 0:  # Left
        playerBox.x -= playerSpeed
    if keyInput[pygame.K_d] and playerBox.x < win_W - 20:  # Right
        playerBox.x += playerSpeed

def debrisBehaviour(debrisSpawner):
    for debris in debrisSpawner:
        debris.y += debrisSpeed
        if debris.y > win_H:
            debrisSpawner.remove(debris)

def playerGun(playerAmmo):
    for bullet in playerAmmo:
        bullet.y -= bulletSpeed


def collisionManager(playerAmmo, debrisSpawner):
    for bullet in playerAmmo:
        for debris in debrisSpawner:
            if debris.colliderect(bullet):
                debrisSpawner.remove(debris)
    for debris in debrisSpawner:
        for bullet in playerAmmo:
            if bullet.colliderect(debris):
                playerAmmo.remove(bullet)



def playerHealthManager(playerBox, debrisSpawner, playerHealth):
    for debris in debrisSpawner:
        if debris.colliderect(playerBox):
            debrisSpawner.remove(debris)
            pygame.event.post(pygame.event.Event(playerHit))


# Main Function
def main():
    playerBox = pygame.Rect(150, 550, 20, 20)
    debrisSpawner = []
    playerAmmo = []
    playerHealth = 10
    playerScore = 0

    clock = pygame.time.Clock()
    run = True
    while run:
        tick = pygame.time.get_ticks()
        clock.tick(gameFPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet = pygame.Rect(playerBox.x, playerBox.y, 10, 20)
                    playerAmmo.append(bullet)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    python = sys.executable
                    os.execl(python, python, * sys.argv)

            if event.type == playerHit:
                playerHealth -= 1

        if len(debrisSpawner) < debrisAllowed:
            debris = pygame.Rect(random.randint(0, 300), 0, 20, 20)
            debrisSpawner.append(debris)
        if playerHealth > 0:
            playerScore += 10

        keyInput = pygame.key.get_pressed()
        debrisBehaviour(debrisSpawner)
        playerGun(playerAmmo)
        collisionManager(playerAmmo, debrisSpawner)
        playerMovement(keyInput, playerBox, playerSpeed)
        playerHealthManager(playerBox, debrisSpawner, playerHealth)
        draw_window(playerBox, debrisSpawner, playerAmmo, playerHealth, playerScore)


    main()


# Essential Command
if __name__ == "__main__":
    main()
