import pygame as pg
from os.path import join
import sys , os , random , json
from random import randint
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
sound_on = pg.transform.scale(pg.image.load(join('Assets/sound_on.png')) , (60 , 50))
sound_off = pg.transform.scale(pg.image.load(join('Assets/sound_off.png')) , (60 ,50))
music_off = pg.transform.scale(pg.image.load(join('Assets/music_off.png')) , (50 , 50))
music_on = pg.transform.scale(pg.image.load(join('Assets/music_on.png')) , (50 , 50))

YELLOW = (230 , 230 , 30)
BLACK = (0 , 0 , 0)
GREEN = (10 , 150 , 60)
WHITE = (255 , 255 , 255)
GREY = (128 , 128 , 128 , 4 )
DARK_GREY = (70 ,70 ,70)
MID_GREY = (100 , 100 , 100)
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
preset_texts = pg.sprite.Group()
pause_texts = pg.sprite.Group()
info_texts = pg.sprite.Group()

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

change_text = options_font1.render('SWITCH', 1, BLACK)
waiting_text = gameover_text_font.render('Press a key...' , 1 , BLACK)
waiting_text_rect = waiting_text.get_rect(center = (WIDTH//2 , 440))

rebinding = None
controls = {
    "up" : pg.K_w,
    "down" : pg.K_s,
    "fire" : pg.K_SPACE,
    "action" : pg.K_r,
}

with open('default_preset.json' , 'w') as f:
    json.dump(controls , f)

try:
    with open('preset.json' , 'r') as f:
        controls = json.load(f)
        custom_preset = True
except:
    pass

sound = True
music = True
sound_image = sound_on
music_image = music_on

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
        if keys[controls['up']] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[controls['down']] and self.rect.bottom < HEIGHT:
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
        if keys[controls["up"]] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[controls['down']] and self.rect.bottom < HEIGHT:
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

class PresetText(pg.sprite.Sprite):
    def __init__(self , move , cords , groups):
        super().__init__(groups)
        self.move = move
        self.cords = cords
        self.key_text = pg.key.name(controls[self.move]).upper()

        self.text = options_font1.render(f'{self.move.upper()} -->  {self.key_text}', 1, "green")
        self.text_rect = self.text.get_rect(center=self.cords)
        self.text_back = options_font1_back.render(f'{self.move.upper()} -->  {self.key_text}', 1, BLACK)
        self.text_back_rect = self.text_back.get_rect(center=self.cords)

        self.colour_active = YELLOW
        self.colour_passive = 'green'
        self.colour = self.colour_passive

    def update(self):
        self.key_text = pg.key.name(controls[self.move]).upper()
        self.text = options_font1.render(f'{self.move.upper()} -->  {self.key_text}', 1, "green")
        self.text_back = options_font1_back.render(f'{self.move.upper()} -->  {self.key_text}', 1, BLACK)
        self.text_back_rect = self.text_back.get_rect(center= self.cords)
        self.text_rect = self.text.get_rect(center = self.cords)

        screen.blit(self.text_back, self.text_back_rect)
        screen.blit(self.text, self.text_rect)

        self.change_rect = change_text.get_rect(midleft=(self.text_back_rect.midright))
        self.change_rect.x += 20
        pg.draw.rect(screen, self.colour , self.change_rect, 0, 4)
        screen.blit(change_text, self.change_rect)

class Text(pg.sprite.Sprite):
    def __init__(self , text , x , y , size , font_style , colour , underline , bold , surf , groups):
        super().__init__(groups)
        self.text = text
        self.x = x
        self.y = y
        self.cords = (x,y)
        self.size = size
        self.colour = colour
        self.underline = underline
        self.bold = bold
        self.surf = surf
        self.font_style = font_style
        self.font = pg.font.SysFont(self.font_style , self.size)
        if self.bold:
            self.font_back = pg.font.SysFont(self.font_style , self.size)
            self.font_back.set_bold(True)
            self.text_surf_back = self.font_back.render(self.text, 1, BLACK)
        self.text_surf = self.font.render(self.text , 1 , self.colour)
        self.rect = self.text_surf.get_rect(midleft = self.cords)

    def update(self):
        if self.bold:
            self.surf.blit(self.text_surf_back, self.rect)
        self.surf.blit(self.text_surf , self.rect)
        if self.underline:
            pg.draw.line(self.surf, BLACK , (self.x - 8, self.y + self.rect.height // 2 + 5), (self.rect.width + self.x + 2, self.y + self.rect.height // 2 + 5), 5)
            pg.draw.line(self.surf , self.colour , (self.x - 5 , self.y + self.rect.height//2 + 3) , (self.rect.width + self.x + 5 , self.y + self.rect.height//2 + 3) , 5)

class PauseText(pg.sprite.Sprite):
    def __init__(self , move , cords , groups):
        super().__init__(groups)
        self.move = move
        self.cords = cords
        self.key_text = pg.key.name(controls[self.move]).upper()

        self.text = options_font1.render(f'{self.move.upper()} -->  {self.key_text}', 1, WHITE)
        self.text_rect = self.text.get_rect(center=self.cords)
        self.text_back = options_font1_back.render(f'{self.move.upper()} -->  {self.key_text}', 1, BLACK)
        self.text_back_rect = self.text_back.get_rect(center=self.cords)

    def update(self):
        self.key_text = pg.key.name(controls[self.move]).upper()
        self.text = options_font1.render(f'{self.move.upper()} -->  {self.key_text}', 1, WHITE)
        self.text_back = options_font1_back.render(f'{self.move.upper()} -->  {self.key_text}', 1, BLACK)
        self.text_back_rect = self.text_back.get_rect(center= self.cords)
        self.text_rect = self.text.get_rect(center = self.cords)

        surface.blit(self.text_back, self.text_back_rect)
        surface.blit(self.text, self.text_rect)

class Rectangle(pg.sprite.Sprite):
    def __init__(self , width , height , center , colour , side , eccentry , write , text , surf , font_style , size ,text_colour , groups):
        super().__init__(groups)
        self.width = width
        self.height = height
        self.center = center
        self.colour = colour
        self.text_colour = text_colour
        self.side = side
        self.eccentry = eccentry
        self.write = write
        self.text = text
        self.font_style = font_style
        self.size = size
        self.font = pg.font.SysFont(self.font_style , self.size)
        self.surface = surf
        self.rect = pg.Rect(0 , 0 , self.width , self.height)
        self.rect.center = self.center

        if self.write:
            self.text_surf = self.font.render(self.text , 1 , self.text_colour)
            self.text_rect = self.text_surf.get_rect(center = self.center)
            self.rect2 = self.text_rect.inflate(20 , 10)

    def update(self):
        if self.write:
            pg.draw.rect(self.surface , self.colour , self.rect2 , self.side , self.eccentry)
            self.surface.blit(self.text_surf , self.text_rect)
        else:
            pg.draw.rect(self.surface, self.colour, self.rect, self.side, self.eccentry)


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
            options_button = Button(200, 60, WIDTH // 2, 360, 'OPTIONS')
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
                if event.button == 1:
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
    global mouse_count, highscore , high_score_notification , music , sound , pause_texts
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


    continue_button = Pause_Button(200, 50, 240, 580, 'CONTINUE')
    menu_button = Pause_Button(210, 50, 730, 580, 'MAIN MENU')

    pause_rect = Rectangle(800 , 600 , (WIDTH//2 , HEIGHT//2) , DARK_GREY , 0 , 0 , False , '' , surface , '' , 0 , BLACK , pause_texts)
    pause_text = Rectangle(400 , 80, (WIDTH // 2, 110), 'dark grey', 0, 4 , True, 'Game Paused', surface, 'Impact', 60 , BLACK, pause_texts)
    pause_text1 = PauseText('up' , (WIDTH//2 , 250) , pause_texts)
    pause_text2 = PauseText('down' , (WIDTH//2 , 300) , pause_texts)
    pause_text3 = PauseText('fire' , (WIDTH//2 , 350) , pause_texts)
    pause_text4 = PauseText('action' , (WIDTH//2 ,400) , pause_texts)

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
            pause_texts.update()
            continue_button.changecolour(mouse)
            continue_button.update('dark grey')
            menu_button.changecolour(mouse)
            menu_button.update('dark grey')

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
                if event.key == controls['fire'] and player.can_shoot:
                    laser_sound.play()
                    laser = Laser(player.rect.midright, (all_entities, laser_entities))
                    player.can_shoot = False

                if event.key == controls['action'] and player.bomb and len(trap_entities) < player.trap_limit and total_score > 200:
                    trap = Trap(player.rect.center , (trap_entities , all_entities))
                    player.bomb = False


            if event.type == pg.MOUSEBUTTONDOWN and pause:
                if event.button == 1:
                    if mouse[0] in range(continue_button.rect.left , continue_button.rect.right) and mouse[1] in range(continue_button.rect.top , continue_button.rect.bottom) and pause:
                        pause = False
                        click_sound.play()
                        if music:
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
    global sound_image , music_image , sound, music, sound_off, sound_on, music_on, music_off
    screen.blit(floor , (-20 , -20))

    while True:
        clock = pg.time.Clock()
        mouse = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()[0]

        info_button = Button(150, 60, WIDTH // 2, 290, 'INFO')
        info_button.changecolour(mouse)
        info_button.update(BLACK)
        controls_button = Button(220, 60, WIDTH // 2, 360, 'CONTROLS')
        controls_button.changecolour(mouse)
        controls_button.update(BLACK)
        back_button = Button(150, 60, WIDTH // 2, 430, 'BACK')
        back_button.changecolour(mouse)
        back_button.update(BLACK)

        sound_rect = pg.Rect(450 , 550 , 60 , 50)
        pg.draw.rect(screen , WHITE , sound_rect , 0 , 5)
        screen.blit(sound_image , (450 , 550))

        music_rect = pg.Rect(520 , 550 , 60 , 50)
        pg.draw.rect(screen , WHITE , music_rect , 0 , 5)
        screen.blit(music_image , (525 , 552))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if mouse[0] in range(info_button.rect.left, info_button.rect.right) and mouse[1] in range(info_button.rect.top, info_button.rect.bottom):
                        click_sound.play()
                        info()
                    if mouse[0] in range(controls_button.rect.left, controls_button.rect.right) and mouse[1] in range(controls_button.rect.top, controls_button.rect.bottom):
                        click_sound.play()
                        keybinds()
                    if mouse[0] in range(back_button.rect.left, back_button.rect.right) and mouse[1] in range(back_button.rect.top, back_button.rect.bottom):
                        click_sound.play()
                        menu()
                    if mouse[0] in range(sound_rect.left, sound_rect.right) and mouse[1] in range(sound_rect.top, sound_rect.bottom):
                        click_sound.play()
                        if sound:
                            sound = False
                        else:
                            sound = True
                    if mouse[0] in range(music_rect.left, music_rect.right) and mouse[1] in range(music_rect.top, music_rect.bottom):
                        click_sound.play()
                        if music:
                            music = False
                        else:
                            music = True

        if music:
            music_image = music_on
            menu_music.set_volume(0.4)
            pg.mixer.music.set_volume(1)
        else:
            music_image = music_off
            menu_music.set_volume(0)
            pg.mixer.music.set_volume(0)
        if sound:
            sound_image = sound_on
            mouse_spawn.set_volume(1)
            mouse_death.set_volume(0.7)
            laser_sound.set_volume(0.3)
            trap_sound.set_volume(1)
            highscore_sound.set_volume(1)
        else:
            sound_image = sound_off
            mouse_spawn.set_volume(0)
            mouse_death.set_volume(0)
            laser_sound.set_volume(0)
            trap_sound.set_volume(0)
            highscore_sound.set_volume(0)

        clock.tick(60)
        pg.display.flip()

def info():
    screen.blit(floor , (-20 , -20))
    back_button = Button(150, 60, WIDTH // 2, 650, 'BACK')

    stage1 = Text('STAGE 1 :' , 20 , 50 , 35 , 'Impact' , YELLOW , True , True , screen , info_texts)
    text1_1 = Text('- Mice Numbers :  Very Low' , 30 , 100 , 25 , 'Impact' , WHITE , False , True , screen , info_texts)
    text1_2 = Text('- Mice Speed :  Very Slow' , 350 , 100 , 25 , 'Impact' , WHITE , False , True ,screen , info_texts)

    stage2 = Text('STAGE 2 :' , 20 , 150 , 35 , 'Impact' , YELLOW , True ,True , screen , info_texts)
    text2_1 = Text('- Mice Numbers :  Low', 30, 200, 25, 'Impact', WHITE, False, True ,screen , info_texts)
    text2_2 = Text('- Mice Speed :  Slow', 350, 200, 25, 'Impact', WHITE, False, True ,screen , info_texts)

    stage3 = Text('STAGE 3 :', 20, 250, 35, 'Impact', YELLOW, True, True ,screen , info_texts)
    text3_1 = Text('- Mice Numbers :  Normal', 30, 300, 25, 'Impact', WHITE, False, True ,screen , info_texts)
    text3_2 = Text('- Mice Speed :  Medium', 350, 300, 25, 'Impact', WHITE, False, True ,screen , info_texts)

    stage4 = Text('STAGE 4 :', 20, 350, 35, 'Impact', YELLOW, True, True ,screen , info_texts)
    text4_1 = Text('- Mice Numbers :  High', 30, 400, 25, 'Impact', WHITE, False, True ,screen , info_texts)
    text4_2 = Text('- Mice Speed :  Fast', 350, 400, 25, 'Impact', WHITE, False, True ,screen , info_texts)

    stage5 = Text('STAGE 5 :', 20, 450, 35, 'Impact', YELLOW, True, True ,screen , info_texts)
    text5_1 = Text('- Mice Numbers :  High', 30, 500, 25, 'Impact', WHITE, False, True ,screen , info_texts)
    text5_2 = Text('- Mice Speed :  Very Fast', 350, 500, 25, 'Impact', WHITE, False, True ,screen , info_texts)

    while True:
        clock = pg.time.Clock()
        mouse = pg.mouse.get_pos()
        back_button.changecolour(mouse)
        back_button.update(BLACK)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if mouse[0] in range(back_button.rect.left , back_button.rect.right) and mouse[1] in range(back_button.rect.top , back_button.rect.bottom):
                        click_sound.play()
                        options()

        clock.tick(60)
        info_texts.update()
        pg.display.flip()

def keybinds():
    global rebinding , controls
    preset_texts.empty()
    screen.blit(floor, (-20, -20))

    up_text = PresetText('up', (WIDTH//2, 220), preset_texts)
    down_text = PresetText('down' , (WIDTH//2 , 260) , preset_texts)
    fire_text = PresetText('fire' , (WIDTH//2 , 300) , preset_texts)
    action_text = PresetText('action' , (WIDTH//2 , 340) , preset_texts)

    back_button = Button(150, 60, WIDTH // 2, 650, 'BACK')
    reset_button = Button(300, 60, WIDTH // 2, 580, 'RESET BINDS')

    while True:
        clock = pg.time.Clock()
        mouse = pg.mouse.get_pos()
        screen.blit(floor, (-20, -20))

        back_button.changecolour(mouse)
        back_button.update(BLACK)
        reset_button.changecolour(mouse)
        reset_button.update(BLACK)

        title = gameover_text_font.render('KEY CONTROLS', 1, BLACK)
        title_rect = pg.Rect(100 , 100 , 300 , 70)
        title_rect.center = (WIDTH // 2 , 100)

        text2b = options_font1_back.render('Press ESC to pause', 1, BLACK)
        text2b_rect = text2b.get_rect(center=(WIDTH // 2, 380))
        text2 = options_font1.render('Press ESC to pause', 1, 'green')
        text2_rect = text2.get_rect(center=(WIDTH // 2, 380))

        rect_big = pg.Rect(250 , 140 , 500 , 380)
        pg.draw.rect(screen , MID_GREY , rect_big , 0 , 4)
        pg.draw.rect(screen, BLACK, rect_big, 4, 4)
        pg.draw.rect(screen, 'green', title_rect , 0 , 4)
        pg.draw.rect(screen, BLACK, title_rect, 3, 4)

        screen.blit(title , (title_rect.x + 35 , title_rect.y + 10))
        screen.blit(text2b, text2b_rect)
        screen.blit(text2, text2_rect)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if mouse[0] in range(back_button.rect.left, back_button.rect.right) and mouse[1] in range(back_button.rect.top, back_button.rect.bottom):
                        click_sound.play()
                        rebinding = None
                        options()
                    if mouse[0] in range(reset_button.rect.left, reset_button.rect.right) and mouse[1] in range(reset_button.rect.top, reset_button.rect.bottom):
                        click_sound.play()
                        with open('default_preset.json' , 'r') as f:
                            controls = json.load(f)
                        try:
                            os.remove('preset.json')
                        except:
                            pass
                    if mouse[0] in range(up_text.change_rect.left, up_text.change_rect.right) and mouse[1] in range(up_text.change_rect.top, up_text.change_rect.bottom):
                        click_sound.play()
                        rebinding = 'up'
                    if mouse[0] in range(down_text.change_rect.left, down_text.change_rect.right) and mouse[1] in range(down_text.change_rect.top, down_text.change_rect.bottom):
                        click_sound.play()
                        rebinding = 'down'
                    if mouse[0] in range(fire_text.change_rect.left, fire_text.change_rect.right) and mouse[1] in range(fire_text.change_rect.top, fire_text.change_rect.bottom):
                        click_sound.play()
                        rebinding = 'fire'
                    if mouse[0] in range(action_text.change_rect.left, action_text.change_rect.right) and mouse[1] in range(action_text.change_rect.top, action_text.change_rect.bottom):
                        click_sound.play()
                        rebinding = 'action'

            if event.type == pg.KEYDOWN and rebinding:
                    if event.key == pg.K_ESCAPE:
                        rebinding = None
                    elif event.key in controls.values():
                        rebinding = None
                    else:
                        controls[rebinding] = event.key
                        rebinding = None

                        with open('preset.json', 'w') as f:
                            json.dump(controls , f)

        if rebinding:
            screen.blit(waiting_text , waiting_text_rect)
        else:
            for button in preset_texts:
                button.colour = button.colour_passive
        if rebinding == 'up':
            up_text.colour = up_text.colour_active
        if rebinding == 'down':
            down_text.colour = down_text.colour_active
        if rebinding == 'fire':
            fire_text.colour = fire_text.colour_active
        if rebinding == 'action':
            action_text.colour = action_text.colour_active

        preset_texts.update()
        clock.tick(60)
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
                if event.button == 1:
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