import pygame as pg
from os.path import join
import sys
from random import randint
import random
import os
pg.init()

WIDTH , HEIGHT = 1000 , 700
screen = pg.display.set_mode((WIDTH , HEIGHT))
surface = pg.Surface((WIDTH , HEIGHT), pg.SRCALPHA)
surface2 = pg.Surface((WIDTH , HEIGHT), pg.SRCALPHA)
pg.display.set_caption('Cheesy Situation')
icon = pg.image.load(join('Assets/cheese.png'))
pg.display.set_icon(icon)
floor = pg.transform.scale(pg.image.load(join('Assets/floor.jpg')), (1050 , 800))
player_image = pg.image.load(join('Assets/cheese.png'))


YELLOW = (230 , 230 , 30)
BLACK = (0 , 0 , 0)
GREEN = (10 , 150 , 60)
WHITE = (255 , 255 , 255)
GREY = (128 , 128 , 128 , 4 )
DARK_GREY = (70 ,70 ,70)
LIGHT_BLUE = (12 , 175 , 170)


button_font = pg.font.SysFont('Impact' , 50)
pause_button_font = pg.font.SysFont('Impact' , 40)
menu_font = pg.font.SysFont('Ink Free' , 70)
menu_font2 = pg.font.SysFont('Ink Free' , 40)
menu_font2_back = pg.font.SysFont('Ink Free' , 40)
menu_font2_back.set_bold(True)

pause_font = pg.font.SysFont('Impact' , 60)
pause_text_font = pg.font.SysFont('Impact' , 30)
pause_text = pause_font.render('Game Paused' , 1 , BLACK)
pause_text1 = pause_text_font.render('W , S   --->   MOVE' , 1 , WHITE)
pause_text2 = pause_text_font.render('SPACE   --->   FIRE RAT POISON' , 1 , WHITE)
pause_text3 = pause_text_font.render('R   --->   THROW POISON TRAP' , 1 , WHITE)

score_font = pg.font.SysFont('Times New Roman' , 40)
stage_text_font = pg.font.SysFont('Times New Roman'  , 20)

gameover_text_font = pg.font.SysFont('Impact' , 40)
gameover_text_font_back = pg.font.SysFont('Impact' , 40)
gameover_text_font_back.set_bold(True)
gameover_text_font2 = pg.font.SysFont('Times New Roman' , 40)
options_font1 = pg.font.SysFont('Impact' , 30)
options_font1_back = pg.font.SysFont('Impact' , 30)
options_font1_back.set_bold(True)
options_font2 = pg.font.SysFont('Impact' , 29)
options_font2_back = pg.font.SysFont('Impact' , 29)
options_font2_back.set_bold(True)

mouse_event1 = pg.event.custom_type()
mouse_event2 = pg.event.custom_type()
mouse_event3 = pg.event.custom_type()
mouse_event4 = pg.event.custom_type()
pg.time.set_timer(mouse_event1 , 2500)
pg.time.set_timer(mouse_event2 , 2000)
pg.time.set_timer(mouse_event3 , 1000)
pg.time.set_timer(mouse_event4 , 800)

laser_entities = pg.sprite.Group()
mouse_entities = pg.sprite.Group()
all_entities = pg.sprite.Group()
player_group = pg.sprite.Group()
explosion_entities = pg.sprite.Group()
trap_entities = pg.sprite.Group()

explosion = pg.image.load(join('Assets/explosion.png'))
mouse_width , mouse_height = 200 , 60
mouse_image = 'Assets/mouse.png'

mouse_count = 0
game_over = False
high_score_notification = False
if os.path.exists('highscore.txt'):
    with open('highscore.txt' , 'r') as file:
        highscore = int(file.read())
else:
    highscore = 0


game_music = pg.mixer.music.load(join('Assets/Game Music.mp3'))
menu_music = pg.mixer.Sound(join('Assets/Menu Music.mp3'))
menu_music.set_volume(0.4)
mouse_spawn = pg.mixer.Sound(join('Assets/mouse_squeak.mp3'))
mouse_death = pg.mixer.Sound(join('Assets/splash.mp3'))
mouse_death.set_volume(0.7)
laser_sound = pg.mixer.Sound(join('Assets/spray.mp3'))
laser_sound.set_volume(0.3)
trap_sound = pg.mixer.Sound(join('Assets/poison.mp3'))
player_death = pg.mixer.Sound(join('Assets/munch.mp3'))
highscore_sound = pg.mixer.Sound(join('Assets/highscore.mp3'))
click_sound = pg.mixer.Sound(join('Assets/click.mp3'))
menu_music.play(-1)


class Button():
    def __init__(self , width , height , x_pos , y_pos , text_input):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height
        self.text_input = text_input
        self.text = button_font.render(text_input , 1 , 'orange')
        self.rect = pg.Rect(100 , 100 , width , height)
        self.text_rect = self.text.get_rect(center = (self.x_pos , self.y_pos))
        self.rect.center = self.text_rect.center


    def update(self , rect_colour):
        pg.draw.rect(screen , rect_colour , self.rect , 0 , 5)
        screen.blit(self.text , self.text_rect)


    def changecolour(self , mouse):
        if mouse[0] in range(self.rect.left , self.rect.right) and mouse[1] in range(self.rect.top , self.rect.bottom):
            self.text = button_font.render(self.text_input, 1, 'green')
        else:
            self.text = button_font.render(self.text_input, 1, 'orange')

class Pause_Button():
    def __init__(self , width , height , x_pos , y_pos , text_input):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height
        self.text_input = text_input
        self.text = pause_button_font.render(text_input , 1 , BLACK)
        self.rect = pg.Rect(100 , 100 , width , height)
        self.text_rect = self.text.get_rect(center = (self.x_pos , self.y_pos))
        self.rect.center = self.text_rect.center


    def update(self , rect_colour):
        pg.draw.rect(surface , rect_colour , self.rect , 0 , 5)
        surface.blit(self.text , self.text_rect)

    def changecolour(self , mouse):
        if mouse[0] in range(self.rect.left , self.rect.right) and mouse[1] in range(self.rect.top , self.rect.bottom):
            self.text = pause_button_font.render(self.text_input, 1, YELLOW)
        else:
            self.text = pause_button_font.render(self.text_input, 1, BLACK)

class Gameover_Button():
    def __init__(self , width , height , x_pos , y_pos , text_input):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height
        self.text_input = text_input
        self.text = pause_button_font.render(text_input , 1 , BLACK)
        self.rect = pg.Rect(100 , 100 , width , height)
        self.text_rect = self.text.get_rect(center = (self.x_pos , self.y_pos))
        self.rect.center = self.text_rect.center


    def update(self , rect_colour):
        pg.draw.rect(surface2 , rect_colour , self.rect , 0 , 5)
        surface2.blit(self.text , self.text_rect)

    def changecolour(self , mouse):
        if mouse[0] in range(self.rect.left , self.rect.right) and mouse[1] in range(self.rect.top , self.rect.bottom):
            self.text = pause_button_font.render(self.text_input, 1, YELLOW)
        else:
            self.text = pause_button_font.render(self.text_input, 1, BLACK)

class Gun(pg.sprite.Sprite):
    def __init__(self , x  ,y , image , groups):
        super().__init__(groups)
        self.x = x
        self.y = y
        self.image = pg.transform.rotate(pg.transform.scale(pg.image.load(image) , (100 , 85)) , 10)
        self.rect = self.image.get_rect(center = (x , y))
        self.speed = 5

    def update(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_w] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pg.K_s] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed

    def draw(self):
        screen.blit(self.image , self.rect)

class Player(pg.sprite.Sprite):
    def __init__(self, pos , image, can_shoot, bomb , groups):
        super().__init__(groups)
        self.image = pg.transform.rotate(pg.transform.scale(pg.image.load(image), (100, 85)), 10)
        self.rect = self.image.get_rect(center=(pos))
        self.speed = 5
        self.timer = 0
        self.can_shoot = can_shoot
        self.bomb = bomb
        self.bomb_timer = 0
        self.total_time_laser = 60
        self.total_time_trap = 240
        self.trap_limit = 1

    def update(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_w] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pg.K_s] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed

    def draw(self):
        screen.blit(self.image, self.rect)

    def fire_timer(self):
        if self.can_shoot == False:
            self.timer += 1
            if self.timer > self.total_time_laser:
                self.can_shoot = True
                self.timer = 0

        if self.bomb == False:
            self.bomb_timer += 1
            if self.bomb_timer > self.total_time_trap:
                self.bomb = True
                self.bomb_timer = 0

class Laser(pg.sprite.Sprite):
    def __init__(self , pos , groups):
        super().__init__(groups)
        self.image = pg.image.load(join('Assets/laser.png'))
        self.rect = self.image.get_rect(midleft = (pos))
        self.speed = 14

    def update(self):
        self.rect.centerx += self.speed
        if self.rect.left > WIDTH:
            self.kill()

    def draw(self):
        screen.blit(self.image , self.rect)

class Mouse(pg.sprite.Sprite):
    def __init__(self , x , y , width , height , speed , image , groups):
        super().__init__(groups)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pg.transform.scale(pg.image.load(join(image)) , (self.width , self.height))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.speed = speed


    def update(self):
        for player in player_group:
            if self.rect.left > 50:
                self.rect.x -= self.speed

            else:
                if self.y < player.rect.y:
                    self.image = pg.transform.rotate(pg.transform.scale(pg.image.load(join('Assets/mousetop.png')), (150 , 60)), 90)
                    self.rect.y += 2
                else:
                    self.image = pg.transform.rotate(pg.transform.scale(pg.image.load(join('Assets/mousetop.png')), (150, 60)), -90)
                    self.rect.y -= 2
        if self.rect.bottom < 0 or self.rect.top > HEIGHT:
            self.kill()

    def draw(self):
        screen.blit(self.image , self.rect)

class Explosion(pg.sprite.Sprite):
    def __init__(self , pos , groups):
        super().__init__(groups)
        self.image = pg.image.load(join('Assets/explosion2.png'))
        self.rect = self.image.get_rect(center = pos)
        self.timer = 0

    def update(self):
        self.timer += 1
        if self.timer > 28:
            self.kill()

class Trap(pg.sprite.Sprite):
    def __init__(self , pos , groups):
        super().__init__(groups)
        self.image = pg.transform.scale(pg.image.load(join('Assets/poison_trap.webp')), (50 , 50))
        self.rect = self.image.get_rect(center = pos)

    def draw(self):
        screen.blit(self.image , self.rect)


def collisions():
    global mouse_count
    for player in player_group:
        pl_collide = pg.sprite.spritecollide(player , mouse_entities , True)
        if pl_collide:
            player_death.play(1)
            game_over = True
            gameover()


    for laser in laser_entities:
        collides = pg.sprite.spritecollide(laser , mouse_entities , True)
        if collides:
            mouse_death.play()
            laser.kill()
            mouse_count += 1

    for trap in trap_entities:
        coll = pg.sprite.spritecollide(trap , mouse_entities , False)
        if coll:
            trap_sound.play()
            trap.kill()
            Explosion(trap.rect.center , (explosion_entities , all_entities))

    for mouse in mouse_entities:
        collisisons = pg.sprite.spritecollide(mouse , explosion_entities , False)
        if collisisons:
            mouse.kill()
            mouse_count += 1

def menu():
    pg.mixer.music.stop()
    screen.blit(floor , (-20 , -20))
    game_over = False

    screen.blit(pg.transform.scale(pg.image.load(join('Assets/rat_poisonleft.png')), (400 , 400)), (740 , 350))
    screen.blit(pg.transform.rotate(pg.transform.scale(pg.image.load(join('Assets/cheeseleft.png')), (220 , 220)), -8), (700 , 520))
    screen.blit(pg.transform.scale(pg.image.load(join('Assets/mouseright.png')), (400, 200)), (-120, 510))
    screen.blit(pg.transform.scale(pg.image.load(join('Assets/mouseright.png')), (400 , 200)), (-20 , 565))
    screen.blit(pg.transform.scale(pg.image.load(join('Assets/mouseright.png')), (400, 200)), (-140, 565))
    screen.blit(pg.transform.scale(pg.image.load(join('Assets/mouseright.png')), (400, 200)), (-260, 565))

    menu_text = menu_font.render('Cheesy Situation' , 1 , BLACK)
    menu_rect1 = menu_text.get_rect(center = (WIDTH//2 , 130))
    rect1 = pg.Rect(100 , 100 , 560 , 84)
    rect1.center = menu_rect1.center
    pg.draw.rect(screen , YELLOW , rect1 , 0 , 4)
    pg.draw.rect(screen , BLACK , rect1 , 5 , 4)
    screen.blit(menu_text , menu_rect1)
    high_score_text = menu_font2.render('HIGHSCORE:  ' + str(highscore) , 1  , 'orange')
    high_score_textb = menu_font2_back.render('HIGHSCORE:  ' + str(highscore), 1, BLACK)
    # rect3 = pg.Rect(2, 8, 370, 50)
    # pg.draw.rect(screen, BLACK , rect3 , 0 , 5)
    rect2b = pg.Rect(5 , 11 , 400 , 50)
    pg.draw.rect(screen, BLACK, rect2b, 3, 5)
    rect2 = pg.Rect(2 , 8 , 400 , 50)
    pg.draw.rect(screen , 'orange' , rect2 , 3 , 5)
    screen.blit(high_score_textb, (10, 10))
    screen.blit(high_score_text , (10 , 10))


    while True:
        clock = pg.time.Clock()
        mouse = pg.mouse.get_pos()

        if not game_over:
            play_button = Button(150, 60, WIDTH // 2, 290, 'PLAY')
            play_button.changecolour(mouse)
            play_button.update(BLACK)
            options_button = Button(150, 60, WIDTH // 2, 360, 'INFO')
            options_button.changecolour(mouse)
            options_button.update(BLACK)
            quit_button = Button(150, 60, WIDTH // 2, 430, 'EXIT')
            quit_button.changecolour(mouse)
            quit_button.update(BLACK)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if event.type == pg.MOUSEBUTTONDOWN:
                if mouse[0] in range(play_button.rect.left , play_button.rect.right) and mouse[1] in range(play_button.rect.top , play_button.rect.bottom):
                    click_sound.play()
                    play()
                if mouse[0] in range(options_button.rect.left , options_button.rect.right) and mouse[1] in range(options_button.rect.top , options_button.rect.bottom):
                    click_sound.play()
                    options()
                if mouse[0] in range(quit_button.rect.left , quit_button.rect.right) and mouse[1] in range(quit_button.rect.top , quit_button.rect.bottom):
                    click_sound.play()
                    pg.quit()
                    sys.exit()

        clock.tick(60)
        pg.display.flip()

def play():
    global mouse_count, highscore , high_score_notification
    music_delay = 0
    menu_music.stop()
    screen.blit(floor , (-20 , -20))
    clock = pg.time.Clock()
    pause = False
    player = Player((75 , HEIGHT//2) , 'Assets/cheese.png' , True , True , (all_entities , player_group))
    gun = Gun(125 , HEIGHT//2 , 'Assets/rat_poison.png' , all_entities)
    gun.image = pg.transform.rotate(gun.image , -10).convert_alpha()
    total_score = 0
    highscore_num = 0
    play_num = 0
    game_over = False
    mouse_count = 0
    with open('score.txt' , 'w') as file:
        file.write('0')

    stage1 = score_font.render('STAGE 1' , 1 , BLACK)
    stage1_rect = pg.Rect(100 , 40 , 0 , 0)
    stage1_text = stage_text_font.render('Slow movement , reload & enemies' , 1 , BLACK)
    stage1_rect.center = (WIDTH//2 - 70 , 20)
    stage1_text_rect = pg.Rect(100 , 40 , 0 , 0)
    stage1_text_rect.center = (WIDTH//2 - 140 , 60)

    stage2 = score_font.render('STAGE 2' , 1 , BLACK)
    stage2_rect = pg.Rect(100, 40, 0, 0)
    stage2_text = stage_text_font.render('Faster reload & enemies / More enemies / Traps Unlocked', 1, BLACK)
    stage2_rect.center = (WIDTH // 2 - 70, 20)
    stage2_text_rect = pg.Rect(100, 40, 0, 0)
    stage2_text_rect.center = (WIDTH // 2 - 210, 60)

    stage3 = score_font.render('STAGE 3', 1, BLACK)
    stage3_rect = pg.Rect(100, 40, 0, 0)
    stage3_text = stage_text_font.render('Faster movement , reload & enemies / More enemies / +1 Trap', 1, BLACK)
    stage3_rect.center = (WIDTH // 2 - 70, 20)
    stage3_text_rect = pg.Rect(100, 40, 0, 0)
    stage3_text_rect.center = (WIDTH // 2 - 240, 60)

    stage4 = score_font.render('STAGE 4', 1, BLACK)
    stage4_rect = pg.Rect(100, 40, 0, 0)
    stage4_text = stage_text_font.render('More & faster enemies / +2 Traps', 1, BLACK)
    stage4_rect.center = (WIDTH // 2 - 70, 20)
    stage4_text_rect = pg.Rect(100, 40, 0, 0)
    stage4_text_rect.center = (WIDTH // 2 - 120, 60)

    stage5 = score_font.render('STAGE 5', 1, BLACK)
    stage5_rect = pg.Rect(100, 40, 0, 0)
    stage5_text = stage_text_font.render('Faster Enemies', 1, BLACK)
    stage5_rect.center = (WIDTH // 2 - 70, 20)
    stage5_text_rect = pg.Rect(100, 40, 0, 0)
    stage5_text_rect.center = (WIDTH // 2 - 50, 60)


    while True:
        mouse = pg.mouse.get_pos()
        music_delay += 1
        high_score = False
        score = play_num // 6
        score_text = score_font.render('SCORE:  ' + str(score), 1, BLACK)
        total_score = score
        highscore_text = score_font.render('!!NEW HIGHSCORE!!' , 1 , BLACK)
        with open('score.txt' , 'w') as file:
            file.write(str(score))

        if music_delay == 300:
            pg.mixer.music.play()

        if score > highscore:
            highscore = total_score
            high_score = True
            high_score_notification = True
            with open('highscore.txt' , 'w') as file:
                file.write(str(highscore))
            highscore_num += 1

        if 200 <= total_score <= 600:
            player.total_time_laser = 40
            player.total_time_trap = 200
        elif 600 <= total_score <= 1300:
            player.speed = 7
            gun.speed = 7
            player.total_time_laser = 25
            player.total_time_trap = 150
            player.trap_limit = 2
        elif 1300 <= total_score:
            player.total_time_laser = 20
            player.total_time_trap = 100
            player.trap_limit = 4


        if pause:
            pg.draw.rect(surface, GREY , (0, 0, WIDTH, HEIGHT))
            pg.draw.rect(surface , DARK_GREY , (100, 50 , 800 , 600))
            pg.draw.rect(surface , 'dark grey' , (280 , 65 , 400 , 80) , 0 , 4)
            surface.blit(pause_text , (320 , 65))

            continue_button = Pause_Button(200 , 50 , 240 , 580 , 'CONTINUE')
            continue_button.changecolour(mouse)
            continue_button.update('dark grey')

            menu_button = Pause_Button(210 , 50 , 730 , 580 , 'MAIN MENU')
            menu_button.changecolour(mouse)
            menu_button.update('dark grey')

            surface.blit(pause_text1 , (380 , 170))
            surface.blit(pause_text2 , (320 , 230))
            surface.blit(pause_text3, (320, 290))
            screen.blit(surface, (0, 0))

            pg.display.flip()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE and not game_over:
                    if pause:
                        pause = False
                        pg.mixer.music.unpause()
                    else:
                        pause = True
                        pg.mixer.music.pause()
                if event.key == pg.K_SPACE and player.can_shoot:
                    laser_sound.play()
                    laser = Laser(player.rect.midright, (all_entities, laser_entities))
                    player.can_shoot = False

                if event.key == pg.K_r and player.bomb and len(trap_entities) < player.trap_limit and total_score > 200:
                    trap = Trap(player.rect.center , (trap_entities , all_entities))
                    player.bomb = False


            if event.type == pg.MOUSEBUTTONDOWN and pause:
                if mouse[0] in range(continue_button.rect.left , continue_button.rect.right) and mouse[1] in range(continue_button.rect.top , continue_button.rect.bottom) and pause:
                    pause = False
                    click_sound.play()
                    pg.mixer.music.unpause()
                if mouse[0] in range(menu_button.rect.left , menu_button.rect.right) and mouse[1] in range(menu_button.rect.top , menu_button.rect.bottom) and pause:
                    for entity in all_entities:
                        entity.kill()
                    menu_music.play(-1)
                    click_sound.play()
                    high_score_notification = False
                    menu()

            if event.type == mouse_event1 and total_score < 200:
                if not pause:
                    mouse_y = randint(30, 640)
                    mouse_speed = randint(2 , 5)
                    enemy = Mouse(900 , mouse_y , mouse_width , mouse_height , mouse_speed , mouse_image , (all_entities , mouse_entities))
                    mouse_spawn.play()

            if event.type == mouse_event2 and 200 < total_score < 600:
                if not pause:
                    mouse_y = randint(30, 640)
                    mouse_speed = randint(3, 6)
                    enemy = Mouse(900 , mouse_y , mouse_width , mouse_height , mouse_speed , mouse_image , (all_entities , mouse_entities))
                    mouse_spawn.play()

            if event.type == mouse_event3 and 600 < total_score < 1300:
                if not pause:
                    mouse_y = randint(30, 640)
                    mouse_speed = randint(4, 7)
                    enemy = Mouse(900, mouse_y, mouse_width, mouse_height, mouse_speed, mouse_image, (all_entities, mouse_entities))
                    mouse_spawn.play()

            if event.type == mouse_event4 and 1300 < total_score < 2000:
                if not pause:
                    mouse_y = randint(30, 640)
                    mouse_speed = randint(6, 9)
                    enemy = Mouse(900, mouse_y, mouse_width, mouse_height, mouse_speed, mouse_image, (all_entities, mouse_entities))
                    mouse_spawn.play()

            if event.type == mouse_event4 and 2000 < total_score:
                if not pause:
                    mouse_y = randint(30, 640)
                    mouse_speed = randint(8, 12)
                    enemy = Mouse(900, mouse_y, mouse_width, mouse_height, mouse_speed, mouse_image, (all_entities, mouse_entities))
                    mouse_spawn.play()

        if not pause and not game_over:
            screen.blit(floor, (-20, -20))
            if total_score < 50:
                screen.blit(stage1, stage1_rect)
                screen.blit(stage1_text , stage1_text_rect)
            if 200 < total_score < 250:
                screen.blit(stage2, stage2_rect)
                screen.blit(stage2_text , stage2_text_rect)
            if 600 < total_score < 650:
                screen.blit(stage3 , stage3_rect)
                screen.blit(stage3_text , stage3_text_rect)
            if 1300 < total_score < 1350:
                screen.blit(stage4, stage4_rect)
                screen.blit(stage4_text, stage4_text_rect)
            if 2000 < total_score < 2050:
                screen.blit(stage5, stage5_rect)
                screen.blit(stage5_text, stage5_text_rect)

            play_num += 1
            all_entities.update()
            all_entities.draw(screen)
            collisions()
            player.fire_timer()
            screen.blit(score_text, (0, 0))
            if highscore_num < 50 and high_score:
                screen.blit(highscore_text, (300, 100))
            else:
                high_score = False
            if highscore_num == 1 and high_score:
                highscore_sound.play()
            clock.tick(60)
            pg.display.flip()

def options():
    screen.blit(floor , (-20 , -20))

    while True:
        clock = pg.time.Clock()
        mouse = pg.mouse.get_pos()
        back_button = Button(150, 60, WIDTH // 2, 650, 'BACK')
        back_button.changecolour(mouse)
        back_button.update(BLACK)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if event.type == pg.MOUSEBUTTONDOWN:
                if mouse[0] in range(back_button.rect.left , back_button.rect.right) and mouse[1] in range(back_button.rect.top , back_button.rect.bottom):
                    click_sound.play()
                    menu()

        clock.tick(60)

        text1b = gameover_text_font_back.render('Key Controls:' , 1 , BLACK)
        text1b_rect = text1b.get_rect(center = (120 , 30))
        screen.blit(text1b , text1b_rect)
        pg.draw.line(screen , 'orange' , (10 , 55) , (230 , 55) , 5)
        text2b = options_font1_back.render('W , S :  Player Movement' , 1  , BLACK)
        text2b_rect = text2b.get_rect(center = (170 , 80))
        screen.blit(text2b , text2b_rect)
        text3b = options_font1_back.render('SPACE :  Fire Rat Poison', 1, BLACK)
        text3b_rect = text3b.get_rect(center = (165, 120))
        screen.blit(text3b, text3b_rect)
        text4b = options_font1_back.render('R :  Place Poison Traps', 1, BLACK)
        text4b_rect = text4b.get_rect(center = (160, 160))
        screen.blit(text4b, text4b_rect)
        text5b = options_font1_back.render('Press ESC to pause', 1, BLACK)
        text5b_rect = text5b.get_rect(center=(140 , 200))
        screen.blit(text5b, text5b_rect)


        text1 = gameover_text_font.render('Key Controls:' , 1 , 'green')
        text1_rect = text1.get_rect(center = (120 , 30))
        screen.blit(text1 , text1_rect)
        pg.draw.line(screen , 'green' , (10 , 55) , (230 , 55) , 5)
        text2 = options_font1.render('W , S :  Player Movement' , 1  , 'green')
        text2_rect = text2.get_rect(center = (170 , 80))
        screen.blit(text2 , text2_rect)
        text3 = options_font1.render('SPACE :  Fire Rat Poison', 1, 'green')
        text3_rect = text3.get_rect(center = (165, 120))
        screen.blit(text3, text3_rect)
        text4 = options_font1.render('R :  Place Poison Traps', 1, 'green')
        text4_rect = text4.get_rect(center = (160, 160))
        screen.blit(text4, text4_rect)
        text5 = options_font1.render('Press ESC to pause', 1, 'green')
        text5_rect = text5.get_rect(center=(140 , 200))
        screen.blit(text5, text5_rect)

        stage1b = gameover_text_font_back.render('Stage 1 (0-200):', 1, BLACK)
        stage1b_rect = stage1b.get_rect(center=(135, 300))
        screen.blit(stage1b, stage1b_rect)
        pg.draw.line(screen, 'green', (10, 325), (260, 325), 5)
        stage1_text1b = options_font2_back.render('- Player moves slow', 1, BLACK)
        screen.blit(stage1_text1b, (10, 330))
        stage1_text2b = options_font2_back.render('- Slow reload', 1, BLACK)
        screen.blit(stage1_text2b, (10, 360))
        stage1_text3b = options_font2_back.render('- No poison traps(be careful)', 1, BLACK)
        screen.blit(stage1_text3b, (10, 390))
        stage1_text4b = options_font2_back.render('- Slow & Few enemies', 1, BLACK)
        screen.blit(stage1_text4b, (10, 420))

        stage1 = gameover_text_font.render('Stage 1 (0-200):' , 1 , YELLOW)
        stage1_rect = stage1.get_rect(center = (135 , 300))
        screen.blit(stage1 , stage1_rect)
        pg.draw.line(screen , YELLOW , (10 , 325) , (260 , 325) , 5)
        stage1_text1 = options_font2.render('- Player moves slow' , 1 , YELLOW)
        screen.blit(stage1_text1 , (10 , 330))
        stage1_text2 = options_font2.render('- Slow reload', 1, YELLOW)
        screen.blit(stage1_text2 , (10 , 360))
        stage1_text3 = options_font2.render('- No poison traps(be careful)', 1, YELLOW)
        screen.blit(stage1_text3, (10, 390))
        stage1_text4 = options_font2.render('- Slow & Few enemies', 1, YELLOW)
        screen.blit(stage1_text4, (10, 420))

        stage2b = gameover_text_font_back.render('Stage 2 (200-600):', 1, BLACK)
        stage2b_rect = stage2b.get_rect(center=(505, 300))
        screen.blit(stage2b, stage2b_rect)
        pg.draw.line(screen, BLACK, (360, 325), (660, 325), 5)
        stage2_text1b = options_font2_back.render('- Faster laser & trap reload', 1, BLACK)
        screen.blit(stage2_text1b, (360, 330))
        stage2_text2b = options_font2_back.render('- More & Faster enemies', 1, BLACK)
        screen.blit(stage2_text2b, (360, 360))
        stage2_text3b = options_font2_back.render('- Unlocks poison traps(1)', 1, BLACK)
        screen.blit(stage2_text3b, (360, 390))

        stage2 = gameover_text_font.render('Stage 2 (200-600):' , 1 , YELLOW)
        stage2_rect = stage2.get_rect(center = (505 , 300))
        screen.blit(stage2, stage2_rect)
        pg.draw.line(screen , YELLOW , (360 , 325) , (660 , 325) , 5)
        stage2_text1 = options_font2.render('- Faster laser & trap reload', 1, YELLOW)
        screen.blit(stage2_text1, (360, 330))
        stage2_text2 = options_font2.render('- More & Faster enemies', 1, YELLOW)
        screen.blit(stage2_text2, (360, 360))
        stage2_text3 = options_font2.render('- Unlocks poison traps(1)', 1, YELLOW)
        screen.blit(stage2_text3, (360, 390))

        stage3b = gameover_text_font_back.render('Stage 3 (600-1300):', 1, BLACK)
        stage3b_rect = stage3b.get_rect(center=(840, 300))
        screen.blit(stage3b, stage3b_rect)
        pg.draw.line(screen, BLACK, (690, 325), (998, 325), 5)
        stage3_text1b = options_font2_back.render('- Player moves faster', 1, BLACK)
        screen.blit(stage3_text1b, (690, 330))
        stage3_text2b = options_font2_back.render('- Even faster reload', 1, BLACK)
        screen.blit(stage3_text2b, (690, 360))
        stage3_text3b = options_font2_back.render('- +1 Poison trap(2)', 1, BLACK)
        screen.blit(stage3_text3b, (690, 390))
        stage3_text4b = options_font2_back.render('- Even more & faster', 1, BLACK)
        screen.blit(stage3_text4b, (690, 420))
        stage3_text5b = options_font2_back.render('enemies', 1, BLACK)
        screen.blit(stage3_text5b, (690, 450))

        stage3 = gameover_text_font.render('Stage 3 (600-1300):', 1, YELLOW)
        stage3_rect = stage3.get_rect(center=(840, 300))
        screen.blit(stage3 , stage3_rect)
        pg.draw.line(screen, YELLOW, (690 , 325), (998, 325), 5)
        stage3_text1 = options_font2.render('- Player moves faster', 1, YELLOW)
        screen.blit(stage3_text1, (690, 330))
        stage3_text2 = options_font2.render('- Even faster reload', 1, YELLOW)
        screen.blit(stage3_text2, (690, 360))
        stage3_text3 = options_font2.render('- +1 Poison trap(2)', 1, YELLOW)
        screen.blit(stage3_text3, (690, 390))
        stage3_text4 = options_font2.render('- Even more & faster', 1, YELLOW)
        screen.blit(stage3_text4, (690, 420))
        stage3_text5 = options_font2.render('enemies', 1, YELLOW)
        screen.blit(stage3_text5, (690, 450))

        stage4b = gameover_text_font_back.render('Stage 4 (1300-2000):', 1, BLACK)
        stage4b_rect = stage4b.get_rect(center=(175, 530))
        screen.blit(stage4b, stage4b_rect)
        pg.draw.line(screen, BLACK, (10, 555), (345, 555), 5)
        stage4_text1b = options_font2_back.render('- Even MORE & FASTER enemies', 1, BLACK)
        screen.blit(stage4_text1b, (10, 560))
        stage4_text2b = options_font2_back.render('- +2 Poison traps (4)', 1, BLACK)
        screen.blit(stage4_text2b, (10, 590))

        stage4 = gameover_text_font.render('Stage 4 (1300-2000):', 1, YELLOW)
        stage4_rect = stage4.get_rect(center=(175 , 530))
        screen.blit(stage4, stage4_rect)
        pg.draw.line(screen, YELLOW, (10 , 555) , (345 , 555), 5)
        stage4_text1 = options_font2.render('- Even MORE & FASTER enemies', 1, YELLOW)
        screen.blit(stage4_text1, (10 , 560))
        stage4_text2 = options_font2.render('- +2 Poison traps (4)', 1, YELLOW)
        screen.blit(stage4_text2, (10, 590))

        stage5b = gameover_text_font_back.render('Stage 5 (2000 +):', 1, BLACK)
        stage5b_rect = stage5b.get_rect(center=(830, 530))
        screen.blit(stage5b, stage5b_rect)
        pg.draw.line(screen, BLACK, (695, 555), (970, 555), 5)
        stage5_text1b = options_font2_back.render('- CRAZY FAST enemies', 1, BLACK)
        screen.blit(stage5_text1b, (700, 560))

        stage5 = gameover_text_font.render('Stage 5 (2000 +):', 1, YELLOW)
        stage5_rect = stage5.get_rect(center=(830 , 530))
        screen.blit(stage5, stage5_rect)
        pg.draw.line(screen, YELLOW, (695, 555), (970, 555), 5)
        stage5_text1 = options_font2.render('- CRAZY FAST enemies', 1, YELLOW)
        screen.blit(stage5_text1, (700 , 560))

        pg.display.flip()

def gameover():
    global highscore , mouse_count , high_score_notification
    game_over = True
    pg.mixer.music.stop()
    while game_over:
        clock = pg.time.Clock()
        mouse = pg.mouse.get_pos()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if event.type == pg.MOUSEBUTTONDOWN:
                if mouse[0] in range(restart.rect.left, restart.rect.right) and mouse[1] in range(restart.rect.top,restart.rect.bottom):
                    for entitity in all_entities:
                        entitity.kill()
                    score = 0
                    click_sound.play()
                    high_score_notification = False
                    play()
                if mouse[0] in range(menu_button.rect.left, menu_button.rect.right) and mouse[1] in range(menu_button.rect.top,menu_button.rect.bottom):
                    for entitity in all_entities:
                        entitity.kill()
                    menu_music.play(-1)
                    click_sound.play()
                    high_score_notification = False
                    menu()

        clock.tick(60)
        pg.draw.rect(surface2 , DARK_GREY , (200 , 100 , 600 , 500))
        pg.draw.rect(surface2 , 'dark grey' , (280 , 120 , 440 , 100) , 0 , 3)
        game_over_text = pause_font.render('Game Over!' , 1 , BLACK)
        surface2.blit(game_over_text , (350 , 130))
        restart = Gameover_Button(200 , 40 , 330 , 550 , 'RESTART')
        restart.changecolour(mouse)
        restart.update('dark gray')
        menu_button = Gameover_Button(200, 40, 670, 550, 'MENU')
        menu_button.changecolour(mouse)
        menu_button.update('dark gray')
        with open('score.txt' , 'r') as file:
            score = int(file.read())
        score_text = gameover_text_font.render('Score :   ' + str(score) , 1 , WHITE)
        kills_text = gameover_text_font.render('Mice Killed :   ' + str(mouse_count) , 1 , WHITE)
        highscore_text = gameover_text_font2.render('! NEW BEST !   ' , 1 , LIGHT_BLUE)
        if not high_score_notification:
            surface2.blit(kills_text , (370 , 300))
            surface2.blit(score_text , (410 , 240))
        else:
            surface2.blit(kills_text, (370, 300))
            surface2.blit(score_text, (250, 240))
            surface2.blit(highscore_text, (480, 240))

        screen.blit(surface2 , (0 , 0))
        pg.display.flip()

menu()