# Shooting Game using pygame
#install pygame: pip install pygame 
import pygame
import random
import sys
#initialize pygame
pygame.init()
#set up display
width, height = 800, 600
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Shooting game")
#Difine colors
WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)
BLACK = (0,0,0)

#font
font = pygame.font.SysFont("Arial",24)
#Game variables
player_size = 50
player_pos = [width // 2, height-2 * player_size]
player_speed = .1

bullet_width = 5
bullet_height=10
bullets =[]
bullet_speed = 5

enemy_size = 20
enemy_speed = .01
enemies = [[random.randint(0,width-enemy_size), 0 ] for _ in range(3)]

score = 0
game_over = False
game_started = False

#Main game loop
running = True
while running:
    screen.fill(BLACK)

    if not game_started:
        title_text = font.render("Press Enter to start",True,WHITE)
        screen.blit(title_text,( width // 2 -100, height // 2 - 20))
        pygame.display.flip()

        #Check for Enter key to start the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_started = True
                    score = 0
                    player_pos = [ width // 2, height - 2 * player_size]
                    enemies = [[random.randint(0, width - enemy_size),0] for _ in range(3)]
                    bullets = []
        continue
    if game_over: 
        #display GameOver screen 
        game_over_text = font.render("Game Over! Press R to Restart",True,RED)
        screen.blit(game_over_text, (width // 2 - 100, height // 2 -20))
        pygame.display.flip()

        #waiting for the player to press R 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    #reset the game state
                    game_over = False
                    score = 0
                    player_pos = [ width // 2, height -2 * player_size]
                    enemies = [[random.randint(0, width - enemy_size),0] for _ in range(3)]
                    bullets = []
        pygame.time.wait(100)
        continue
    
    #Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            #space 
            if event.key == pygame.K_SPACE:
                bullet_pos = [player_pos[0] + player_size // 2, player_pos[1]]
                bullets.append(bullet_pos)
    #player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT] and player_pos[0] < width - player_size:
        player_pos[0] += player_speed
    
    #update bullets
    bullets = [[x,y -bullet_speed] for [x,y] in bullets if y > 0]

    #update enimies 
    for enemy in enemies:
        enemy[1] += enemy_speed
        if enemy[1] >= height:
            game_over = True
            break
        for bullet in bullets[:]:
            bullet_rect = pygame.Rect(bullet[0],bullet[1],bullet_width,bullet_height)
            enemy_rect = pygame.Rect(enemy[0],enemy[1],enemy_size,enemy_size)
            if bullet_rect.colliderect(enemy_rect):
                bullets.remove(bullet)
                enemies.remove(enemy)
                enemies.append([random.randint(0,width-enemy_size),0])
                score += 10
                break
    
    #Increase difficulty by adding more enemies over time 
    if score > 0 and score % 50 == 0 and len(enemies) < score // 50 + 3:
        enemies.append([random.randint(0, width - enemy_size),0])
    
    #Draw player
    pygame.draw.rect(screen,GREEN,(*player_pos,player_size,player_size))
    #Draw bullets
    for bullet in bullets:
        pygame.draw.rect(screen,WHITE,(bullet[0],bullet[1],bullet_width,bullet_height))
    #Draw enemies
    for enemy in enemies:
        pygame.draw.rect(screen,RED,(*enemy, enemy_size,enemy_size))
    #Draw score:
    score_text = font.render("Score: "+str(score),True,WHITE)
    screen.blit(score_text,(10, 10))
    #Refresh display
    pygame.display.flip()
#Quit Game 
pygame.quit()
sys.exit()
