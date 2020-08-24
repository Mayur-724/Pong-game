import pygame
import sys
import time
import random

pygame.mixer.pre_init()
pygame.init()
clock = pygame.time.Clock()
game_end = False
# colour
black = (0, 0, 0)
red = (255, 0, 0)
aqua = (0, 255, 255)
green = (0, 255, 0)
grey = (220, 220, 220)
dim_grey = (105, 105, 105)

# Main Window
screen_width = 800
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pong")
font = pygame.font.Font('freesansbold.ttf', 22)

# backgrouds
game_background = pygame.image.load("./backgrounds/background.jpg").convert()
menu_background = pygame.image.load("./backgrounds/menu.jpg")
winner_background = pygame.image.load("./backgrounds/winner.jpg").convert()
tutorial_background = pygame.image.load("./backgrounds/tutorial.png").convert()

# sounds
bounce_sound = pygame.mixer.Sound('./sounds/bounce.wav')
score_sound = pygame.mixer.Sound('./sounds/score.wav')
win_sound = pygame.mixer.Sound('./sounds/win.wav')
menu_music = pygame.mixer.Sound('./sounds/menu music.wav')
tutorial_music = pygame.mixer.Sound('./sounds/tutorial music.wav')

# ball positions and speed:

# position
ball_pos_x = 400
ball_pos_y = 200
# speed
ball_speed_x = 6 * random.choice((-1, 1))
ball_speed_y = 6 * random.choice((-1, 1))

# player speed and postion:

# speed
player1_speed = 0
player2_speed = 0
# position
player1_pos = [20, 200]
player2_pos = [775, 200]
player1 = pygame.draw.rect(screen, aqua, (player1_pos[0], player1_pos[1], 10, 80))

# score
player1_score = 0
player2_score = 0


def player():
    player1 = pygame.draw.rect(screen, aqua, (player1_pos[0], player1_pos[1], 10, 80))
    player2 = pygame.draw.rect(screen, green, (player2_pos[0], player2_pos[1], 10, 80))


def ball():
    global ball_pos_x, ball_pos_y
    radius = 10
    ball = pygame.draw.circle(screen, red, [ball_pos_x, ball_pos_y], radius)


def ball_movement():
    global ball_pos_x, ball_pos_y
    ball_pos_x += ball_speed_x
    ball_pos_y += ball_speed_y


def ball_border_check():
    global ball_speed_y, ball_speed_x
    if ball_pos_y <= 0 or ball_pos_y >= screen_height - 10:
        pygame.mixer.Sound.play(bounce_sound)
        ball_speed_y *= -1
    elif ball_pos_x <= 0 or ball_pos_x >= screen_width - 10:
        pygame.mixer.Sound.play(bounce_sound)
        ball_speed_x = ball_speed_x * -1


def players_border_check():
    if player1_pos[1] <= 0:
        player1_pos[1] = 0

    elif player1_pos[1] >= (screen_height - 80):
        player1_pos[1] = (screen_height - 80)

    elif player2_pos[1] <= 0:
        player2_pos[1] = 0

    elif player2_pos[1] >= (screen_height - 80):
        player2_pos[1] = (screen_height - 80)


def ball_players_collision():
    global ball_speed_x, ball_speed_y, ball_pos_x
    # ball and player1 collision
    if (ball_pos_y <= player1_pos[1] + 80) and ball_pos_y >= (player1_pos[1]):
        if ball_pos_x <= (player1_pos[0] + 20):
            pygame.mixer.Sound.play(bounce_sound)
            ball_speed_x *= -1

    if ball_pos_x <= player1_pos[0] and (ball_pos_x >= player1_pos[0] - 10):
        if (ball_pos_y <= player1_pos[1] + 80) and ball_pos_y >= (player1_pos[1]):
            pygame.mixer.Sound.play(bounce_sound)
            ball_speed_y *= -1

    # ball and player2 collision
    if (ball_pos_y <= player2_pos[1] + 80) and ball_pos_y >= (player2_pos[1]):
        if ball_pos_x >= (player2_pos[0] - 15):
            pygame.mixer.Sound.play(bounce_sound)
            ball_speed_x *= -1
    if ball_pos_x <= player2_pos[0] and (ball_pos_x >= player2_pos[0] - 10):
        if (ball_pos_y <= player2_pos[1] + 80) and ball_pos_y >= (player2_pos[1]):
            pygame.mixer.Sound.play(bounce_sound)
            ball_speed_y *= -1


def missed_ball():
    global ball_pos_x, ball_pos_y, ball_speed_y
    if ball_pos_x <= 5 or ball_pos_x >= 790:
        pygame.mixer.Sound.play(score_sound)
        time.sleep(0.7)
        player2_pos[1] = (200 - 20)
        player1_pos[1] = (200 - 20)
        ball_pos_y = random.randint(10, 390)
        ball_speed_y *= -1
        ball_pos_x = 395


def score_counter():
    global player1_score, player2_score
    if ball_pos_x <= 5:
        player2_score += 1
    elif ball_pos_x >= 790:
        player1_score += 1
    if player2_score == 10 or player1_score == 10:
        winner_declaration()


def winner_declaration():
    game_end = True
    pygame.mixer.Sound.play(win_sound)

    while game_end == True:
        screen.blit(winner_background, [0, 0])
        font1 = pygame.font.Font('freesansbold.ttf', 50)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if player1_score >= 10:
            win1 = font1.render('Player 1 won!', False, black)
            screen.blit(win1, (250, 100))
            close_button = pygame.image.load('./buttons/close.jpg').convert()
            screen.blit(close_button, (300, 180))

        elif player2_score >= 10:
            win1 = font1.render('Player 2 won!', False, black)
            screen.blit(win1, (250, 100))
            play_again_button = pygame.image.load('./buttons/close.jpg').convert()
            screen.blit(play_again_button, (300, 180))

        # button
        x, y = pygame.mouse.get_pos()
        left_click, scroll, right_click = pygame.mouse.get_pressed()
        if (y >= 180 and y <= 230) and (x >= 300 and x <= 528):
            button_glow = pygame.draw.rect(screen, green, (300, 180, 229, 50), 3)
            if left_click == 1:
                pygame.quit()
                sys.exit()
        pygame.display.update()


def tutorials():

    pygame.mixer.Sound.stop(menu_music)
    pygame.mixer.Sound.play(tutorial_music)
    screen.blit(tutorial_background, (0, 0))
    while game_end == False:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        time.sleep(6)
        game()


def game_intro():
    pygame.mixer.Sound.play(menu_music)
    pygame.mixer.Sound.stop(win_sound)
    while game_end == False:
        screen.blit(menu_background, [0, 0])
        play_button = pygame.image.load('./buttons/play.jpg').convert()
        left_click, scroll, right_click = pygame.mouse.get_pressed()
        screen.blit(play_button, (290, 280))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # button
        x, y = pygame.mouse.get_pos()
        left_click, scroll, right_click = pygame.mouse.get_pressed()
        if (y >= 280 and y <= 328) and (x >= 290 and x <= 506):
            button_glow = pygame.draw.rect(screen, green, (290, 280, 229, 50), 3)
            if left_click == 1:
                tutorials()

        pygame.display.update()


def game():

    pygame.mixer.Sound.stop(tutorial_music)
    pygame.mixer.Sound.stop(win_sound)
    global player1_pos, player2_pos
    while game_end == False:
        pygame.mixer.Sound.stop(menu_music)
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                # player 1 movement
                p1_y = player1_pos[1]
                p1_x = player1_pos[0]
                if event.key == pygame.K_s:
                    p1_y += 60
                elif event.key == pygame.K_w:
                    p1_y -= 60
                player1_pos = [p1_x, p1_y]
                # player 2 movement
                p2_x = player2_pos[0]
                p2_y = player2_pos[1]
                if event.key == pygame.K_DOWN:
                    p2_y += 80
                elif event.key == pygame.K_UP:
                    p2_y -= 80
                player2_pos = [p2_x, p2_y]

        screen.blit(game_background, [0, 0])
        player()
        ball()
        missed_ball()
        ball_border_check()
        players_border_check()
        ball_movement()
        score_counter()
        ball_players_collision()
        pygame.draw.line(screen, dim_grey, (400, 0), (400, screen_height))
        player1_s = font.render(f"{player1_score}", False, grey)
        screen.blit(player1_s, (373, 5))
        player2_s = font.render(f"{player2_score}", False, grey)
        screen.blit(player2_s, (413, 5))
        pygame.display.update()
        clock.tick(60)


game_intro()
