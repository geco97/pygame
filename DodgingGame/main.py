#Today we will build dodging game using pygame
# To install pygame : pip install pygame
import pygame
import random
import sys
#init pygame 
pygame.init()

#screen settings 
screen_width = 300
screen_height = 600
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Dodging Game")

#Colors
WHITE = (255,255,255)
BLACK = (0,0,0)
GRAY = (169,169,169)

#Clock for controlling the frame rate
clock = pygame.time.Clock()

#load images 
player_car_image = pygame.image.load("./images/player_car.png")
enemy_car_image = pygame.image.load("./images/enemy_car.png")
power_up_image = pygame.image.load("./images/power_up.png")
background_image = pygame.image.load("./images/road_background.png")

#Resize images to fit the desired dimensions
car_width , car_height = 80,100
player_car_image = pygame.transform.scale(player_car_image,(car_width,car_height))
enemy_car_image = pygame.transform.scale(enemy_car_image,(car_width,car_height))
power_up_image = pygame.transform.scale(power_up_image,(50,50))
background_image = pygame.transform.scale(background_image,(screen_width,screen_height))

#player car settings 
player_x = screen_width // 2 - car_width // 2
player_y = screen_height - car_height - 20
player_speed = 10

#lane settings 
lane_width = screen_width // 3
lanes = [lane_width // 2 - car_width // 2, 3* lane_width //2 - car_width//2, 5 * lane_width // 2 - lane_width //2]

#enemy cars settings 
enemy_cars = []
for _ in range(3):
    enemy_x = random.choice(lanes)
    enemy_y = random.randint(-600,-100)
    enemy_speed = random.randint(5,10)
    enemy_cars.append([enemy_x,enemy_y,enemy_speed])

#power-up settings
power_up_x = random.choice(lanes)
power_up_y = random.randint(-600,-100)
power_up_active = False

#Scrolling background settings
background_y = 0
background_speed = 5

#score and high score 
score = 0 
high_score = 0
font = pygame.font.SysFont(None,35)
game_over_font = pygame.font.SysFont(None,60)

#paise variable 
paused = False

#Function to display the High score
def display_high_score():
    text = font.render(f"High score: {high_score}",True,BLACK)
    screen.blit(text,(10,40))
#Function to display the score:
def display_score():
    text = font.render(f"Score: {score}",True,BLACK)
    screen.blit(text,(10,10))
#Function to draw lanes
def draw_lanes():
    for i in range(1,3):
        pygame.draw.line(screen,GRAY,(i*lane_width,0),(i*lane_width,screen_height),5)

#Funtion to toggle pause
def toggle_pause():
    global paused
    paused = not paused

#Function to the game over screen 
def game_over():
    global high_score
    if score > high_score:
        high_score = score
    
    screen.fill(WHITE)
    text = game_over_font.render("Game Over!",True,BLACK)
    screen.blit(text,(screen_width //2 - text.get_width()//2, 150))
    play_again_text = font.render("Press",True,BLACK)
    screen.blit(play_again_text,(screen_width // 2 - play_again_text.get_width() // 2, 300))
    play_again_text = font.render("R to play again",True,BLACK)
    screen.blit(play_again_text,(screen_width // 2 - play_again_text.get_width() // 2, 330))
    play_again_text = font.render("Q to Quit",True,BLACK)
    screen.blit(play_again_text,(screen_width // 2 - play_again_text.get_width() // 2, 360))
    display_high_score()
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                if event.key == pygame.K_q:
                    pygame.QUIT()
                    sys.exit()
#function to show the main menu
def main_menu():
    menu_running = True
    while menu_running:
        screen.fill(WHITE)
        title_text = font.render("Dodging Game",True,BLACK)
        screen.blit(title_text,(screen_width //2 - title_text.get_width() //2,150))
        title_text = font.render("Press ENTER to Start",True,BLACK)
        screen.blit(title_text,(screen_width //2 - title_text.get_width() //2,300))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                menu_running = False
main_menu()

#Main game loop 
running = True
while running:
    screen.fill(WHITE)
    background_y +=background_speed
    if background_y >=screen_height:
        background_y = 0
    screen.blit(background_image,(0,background_y))
    screen.blit(background_image,(0,background_y - screen_height))

    draw_lanes()

    #pause
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                toggle_pause()
    if paused: 
        continue

    #player movment 
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > lanes[0]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < lanes[-1]:
        player_x += player_speed
    
    # Move the enemy cars and check collisions
    for car in enemy_cars:
        car[1] += car[2]

        if car[1] > screen_height:
            car[1] = random.randint(-600 , -100)
            car[0] = random.choice(lanes)
            car[2] = random.randint(5,10)
            score +=1
        #check for collision
        if (player_x < car[0] < player_x + car_width or player_x < car[0] + car_width < player_x + car_width) and \
        (player_y < car[1] < player_y + car_height or player_y < car[1] + car_height < player_y + car_height):
            game_over()
            player_x = screen_height //2 - car_width //2 
            player_y = screen_height - car_height - 20
            enemy_cars = [[random.choice(lanes), random.randint(-600,-100),random.randint(5,10)] for _ in range(3)]
            score = 0
            break
    #Move the power_up and check collection
    power_up_y += background_speed
    if power_up_y > screen_height:
        power_up_y = random.randint(-600,-100)
        power_up_x = random.choice(lanes)
        
        if (player_x < power_up_x< player_x + car_width or player_x < power_up_x + 50 < player_x + car_width) and \
        (player_y < power_up_y < player_y + car_height or player_y < power_up_y + 50 < player_y + car_height):
            power_up_active = True
            power_up_y = random.randint(-600,-100)
    #Draw the player car 
    screen.blit(player_car_image,(player_x,player_y))
    #Draw the enemy cars
    for car in enemy_cars:
        screen.blit(enemy_car_image,(car[0],car[1]))
    #Draw the power_up
    screen.blit(power_up_image,(power_up_x,power_up_y))
    #Display the score and high score
    display_score()
    display_high_score()

    #update the display
    pygame.display.flip()
    #cap the frame rate at 30 frames per sec
    clock.tick(30)

#Quit pygame
pygame.quit()
sys.exit()
#DONE