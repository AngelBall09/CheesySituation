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
icon = pg.image.load(join('Assets/cheeses/cheese.png'))
pg.display.set_icon(icon)
floor = pg.transform.scale(pg.image.load(join('Assets/floor.jpg')), (1050 , 800))
player_image = pg.image.load(join('Assets/cheeses/cheese.png'))
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
m1_timer = 2500
m2_timer = 2000
m3_timer = 1000
m4_timer = 800
pg.time.set_timer(mouse_event1 , m1_timer)
pg.time.set_timer(mouse_event2 , m2_timer)
pg.time.set_timer(mouse_event3 , m3_timer)
pg.time.set_timer(mouse_event4 , m4_timer)

laser_entities = pg.sprite.Group()
normal_bullets = pg.sprite.Group()
shotgun_shells = pg.sprite.Group()
sniper_bullets = pg.sprite.Group()
missile_entities = pg.sprite.Group()
missile_explosions = pg.sprite.Group()
air_entities_up = pg.sprite.Group()
air_entities_down = pg.sprite.Group()
planks = pg.sprite.Group()
smokes = pg.sprite.Group()
smokes_up = pg.sprite.Group()
smokes_down = pg.sprite.Group()
blue_area_group = pg.sprite.GroupSingle()
oil_drops = pg.sprite.Group()
cream_drops = pg.sprite.Group()
creams = pg.sprite.Group()
rolling_cheeses = pg.sprite.Group()
mouse_entities = pg.sprite.Group()
all_entities = pg.sprite.Group()
player_group = pg.sprite.Group()
gun_group = pg.sprite.GroupSingle()
explosion_entities = pg.sprite.Group()
trap_entities = pg.sprite.Group()


preset_texts = pg.sprite.Group()
pause_texts = pg.sprite.Group()
info_texts = pg.sprite.Group()

explosion = pg.image.load(join('Assets/bullets_effects/explosion.png'))
mouse_width , mouse_height = 200 , 60
mouse_image = 'Assets/mice/mouse.png'

mouse_kills = 0
game_over = False
high_score_notification = False
if os.path.exists('highscore.txt'):
    with open('highscore.txt' , 'r') as file:
        highscore = int(file.read())
else:
    highscore = 0


game_music = pg.mixer.music.load(join('Assets/sound_effects/Game Music.mp3'))
menu_music = pg.mixer.Sound(join('Assets/sound_effects/Menu Music.mp3'))
menu_music.set_volume(0.4)

mouse_spawn = pg.mixer.Sound(join('Assets/sound_effects/mouse_squeak.mp3'))
mouse_death = pg.mixer.Sound(join('Assets/sound_effects/splash.mp3'))
mouse_death.set_volume(0.7)

laser_sound = pg.mixer.Sound(join('Assets/sound_effects/spray.mp3'))
laser_sound.set_volume(0.3)
bullet_sound = pg.mixer.Sound(join('Assets/sound_effects/bullet.mp3'))
bullet_sound.set_volume(0.3)
shotgun_sound = pg.mixer.Sound(join('Assets/sound_effects/shotgun.mp3'))
shotgun_sound.set_volume(0.7)
rat_slayer_sound = pg.mixer.Sound(join('Assets/sound_effects/rat_slayer.mp3'))
ratzooka_sound1 = pg.mixer.Sound(join('Assets/sound_effects/ratzooka1.mp3'))
ratzooka_sound2 = pg.mixer.Sound(join('Assets/sound_effects/ratzooka2.mp3'))

trap_sound = pg.mixer.Sound(join('Assets/sound_effects/poison.mp3'))

player_death = pg.mixer.Sound(join('Assets/sound_effects/munch.mp3'))
barrel_sound = pg.mixer.Sound(join('Assets/sound_effects/barrel_smash.mp3'))
cheddar_sound = pg.mixer.Sound(join('Assets/sound_effects/cheddar_upgrade.mp3'))
cream_drop_sound = pg.mixer.Sound(join('Assets/sound_effects/cream_drop.mp3'))
cream_sound = pg.mixer.Sound(join('Assets/sound_effects/cream.mp3'))
slip_sound = pg.mixer.Sound(join('Assets/sound_effects/slip.mp3'))
rolling_cheese_sound = pg.mixer.Sound(join('Assets/sound_effects/rolling_cheese.mp3'))
oil_drop_sound = pg.mixer.Sound(join('Assets/sound_effects/oil.mp3'))
burn_sound = pg.mixer.Sound(join('Assets/sound_effects/burn.mp3'))
smoke_sound = pg.mixer.Sound(join('Assets/sound_effects/smoke.mp3'))

highscore_sound = pg.mixer.Sound(join('Assets/sound_effects/highscore.mp3'))
click_sound = pg.mixer.Sound(join('Assets/sound_effects/click.mp3'))
menu_music.play(-1)

change_text = options_font1.render('SWITCH', 1, BLACK)
waiting_text = gameover_text_font.render('Press a key...' , 1 , BLACK)
waiting_text_rect = waiting_text.get_rect(center = (WIDTH//2 , 470))

rebinding = None
controls = {
    "up" : pg.K_w,
    "down" : pg.K_s,
    "fire" : pg.K_SPACE,
    "action" : pg.K_r,
    "reload" : pg.K_f
}

inventory = {}

with open('default_preset.json' , 'w') as f:
    json.dump(controls , f)

try:
    with open('preset.json' , 'r') as f:
        controls = json.load(f)
        custom_preset = True
except:
    pass

try:
    with open('inventory.json' , 'r') as f:
        inventory = json.load(f)
except:
    pass

sound = True
music = True
sound_image = sound_on
music_image = music_on

last_press = {}

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
    def __init__(self , x  ,y , gun , speed , can_shoot , groups):
        super().__init__(groups)
        self.gun = gun
        self.cooldown = False
        if self.gun == 'rat_poison':
            self.image = pg.transform.scale(pg.image.load('Assets/guns/rat_poison_right.png') , (35 , 85))
            self.reload_sound = pg.mixer.Sound(join('Assets/sound_effects/rat_poison_reload2.mp3'))
            self.magazine = 15
            self.fire_cooldown = 30
            self.reload_time = 60
            self.damage = 25
        elif self.gun == 'rat_killers':
            self.image = pg.transform.scale(pg.image.load('Assets/guns/rat_killers.png') , (100 , 75))
            self.reload_sound = pg.mixer.Sound(join('Assets/sound_effects/rat_killers_reload.mp3'))
            self.magazine = 12
            self.fire_cooldown = 20
            self.reload_time = 120
            self.damage = 40
        elif self.gun == 'rat_buster':
            self.image = pg.transform.scale(pg.image.load('Assets/guns/shotgun_right.png') , (150 , 60))
            self.reload_sound = pg.mixer.Sound(join('Assets/sound_effects/shotgun_reload.mp3'))
            self.load_sound = pg.mixer.Sound(join('Assets/sound_effects/shotgun_load.mp3'))
            self.magazine = 5
            self.fire_cooldown = 45
            self.reload_time = 180
            self.damage = 80
        elif self.gun == 'ratata':
            self.image = pg.transform.scale(pg.image.load('Assets/guns/ratata_right.png') , (175 , 60))
            self.reload_sound = pg.mixer.Sound(join('Assets/sound_effects/ratata_reload.mp3'))
            self.magazine = 30
            self.fire_cooldown = 10
            self.reload_time = 150
            self.damage = 45
        elif self.gun == 'rat_slayer':
            self.image = pg.transform.scale(pg.image.load('Assets/guns/bayonet_right.png') , (190 , 70))
            self.reload_sound = pg.mixer.Sound(join('Assets/sound_effects/rat_slayer_reload.mp3'))
            self.load_sound = pg.mixer.Sound(join('Assets/sound_effects/rat_slayer_load.mp3'))
            self.magazine = 6
            self.fire_cooldown = 120
            self.reload_time = 120
            self.melee = False
            self.damage = 160
        elif self.gun == 'ratzooka':
            self.image = pg.transform.scale(pg.image.load('Assets/guns/ratzooka_right.png') , (200 , 65))
            self.magazine = 1
            self.fire_cooldown = 25
            self.reload_time = 100
            self.damage = 200

        self.x = x
        self.y = y
        self.rect = self.image.get_rect(center = (x , y))
        self.speed = speed
        self.can_shoot = can_shoot
        self.timer = 0

    def update(self):
        if self.gun == 'ratzooka':
            if self.can_shoot:
                self.image = pg.transform.scale(pg.image.load('Assets/guns/ratzooka_right.png') , (200 , 65))
            else:
                self. image = pg.transform.scale(pg.image.load('Assets/guns/ratzooka_empty.png'), (180, 65))
        keys = pg.key.get_pressed()
        if keys[controls['up']] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[controls['down']] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed

    def fire_timer(self):
        if self.cooldown:
            self.fire_cooldown -= 1
            if self.gun == 'rat_buster' and self.fire_cooldown == 44:
                self.load_sound.play()
            elif self.gun == 'rat_slayer' and self.fire_cooldown == 119:
                self.load_sound.play()
        if self.magazine <= 0:
            self.can_shoot = False

        if self.gun == 'rat_killers':
            if self.fire_cooldown <= 0:
                self.fire_cooldown = 20
                self.cooldown = False
            if self.can_shoot == False:
                self.timer += 1
                if self.timer == 1:
                    self.reload_sound.play()
                if self.timer > self.reload_time:
                    self.can_shoot = True
                    self.magazine = 12
                    self.timer = 0

        elif self.gun == 'rat_poison':
            if self.fire_cooldown <= 0:
                self.fire_cooldown = 30
                self.cooldown = False
            if self.can_shoot == False:
                self.image = pg.transform.scale(pg.image.load('Assets/guns/rat_poison_right_empty.png'), (40 , 20))
                self.timer += 1
                if self.timer == 1:
                    self.reload_sound.play()
                if self.timer > self.reload_time:
                    self.can_shoot = True
                    self.magazine = 15
                    self.timer = 0
            else:
                self.image = pg.transform.scale(pg.image.load('Assets/guns/rat_poison_right.png'), (35, 85))

        elif self.gun == 'rat_buster':
            if self.fire_cooldown <= 0:
                self.fire_cooldown = 45
                self.cooldown = False
            if self.can_shoot == False:
                self.timer += 1
                if self.timer == 1:
                    self.reload_sound.play()
                if self.timer > self.reload_time:
                    self.can_shoot = True
                    self.magazine = 5
                    self.timer = 0

        elif self.gun == 'ratata':
            if self.fire_cooldown <= 0:
                self.cooldown = False
                self.fire_cooldown = 10
            if self.can_shoot == False:
                self.timer += 1
                if self.timer == 1:
                    self.reload_sound.play()
                if self.timer > self.reload_time:
                    self.can_shoot = True
                    self.magazine = 30
                    self.timer = 0

        elif self.gun == 'rat_slayer':
            if self.fire_cooldown <= 0:
                self.fire_cooldown = 120
                self.cooldown = False
            if self.can_shoot == False:
                self.timer += 1
                if self.timer == 1:
                    self.reload_sound.play()
                if self.timer > self.reload_time:
                    self.can_shoot = True
                    self.magazine = 6
                    self.timer = 0

        elif self.gun == 'ratzooka':
            if self.fire_cooldown <= 0:
                self.fire_cooldown = 25
                self.cooldown = False
            if self.can_shoot == False:
                self.timer += 1
                if self.timer > self.reload_time:
                    self.can_shoot = True
                    self.magazine = 1
                    self.timer = 0

    def rotate(self , direction , playery):
        if self.gun == 'rat_slayer':
            if direction == 'up':
                self.image = pg.transform.rotate(pg.transform.scale(pg.image.load('Assets/guns/bayonet_right.png') , (190 , 70)) , 90)
                self.rect.y  -= 75
            elif direction == 'down':
                self.image = pg.transform.rotate(pg.transform.scale(pg.image.load('Assets/guns/bayonet_right.png') , (190 , 70)) , -90)
                self.rect.y -= 40
            elif direction == 'right':
                self.image = pg.transform.scale(pg.image.load('Assets/guns/bayonet_right.png') , (190 , 70))
                self.rect.centery = playery

    def draw(self):
        screen.blit(self.image , self.rect)

class Player(pg.sprite.Sprite):
    def __init__(self, pos , cheese, bomb , groups):
        super().__init__(groups)
        self.cheese = cheese
        if self.cheese == 'gruyere':
            self.image = pg.transform.rotate(pg.transform.scale(pg.image.load('Assets/cheeses/cheese.png'), (100, 85)), 10)
            self.rect = self.image.get_rect(center=(pos))
            self.speed = 5
        elif self.cheese == 'feta_barrel':
            self.image = pg.transform.scale(pg.image.load('Assets/cheeses/feta_barrel.png'), (120, 120))
            self.rect = self.image.get_rect(center=(pos))
            self.speed = 3
            self.plank_damage = 120
            self.plank_number = 2
        elif self.cheese == 'blue_cheese':
            self.image = pg.transform.rotate(pg.transform.scale(pg.image.load('Assets/cheeses/blue_cheese.png'), (100, 85)), 15)
            self.rect = self.image.get_rect(center=(pos))
            blue_area = BlueArea(self.rect.center , blue_area_group)
            self.speed = 4
            self.slow_x = 2
            self.slow_y = 0.5
        elif self.cheese == 'cream_cheese':
            self.image = pg.transform.scale(pg.image.load('Assets/cheeses/cream_cheese.png'), (80, 55))
            self.rect = self.image.get_rect(center=(pos))
            self.speed = 6
            self.cream_time = 420
            self.cream_timer = 0
        elif self.cheese == 'cheddar':
            self.image = pg.transform.scale(pg.image.load('Assets/cheeses/cheddar_cheese1.png'), (100, 75))
            self.rect = self.image.get_rect(center=(pos))
            self.speed = 3
            self.stage = 1
        elif self.cheese == 'parmesan':
            self.image = pg.transform.scale(pg.image.load('Assets/cheeses/parmesan.png'), (120, 90))
            self.rect = self.image.get_rect(center=(pos))
            self.speed = 4
            self.roll_time = 720
            self.roll_timer = 0
            self.roll_ready = False
            self.cheese_damage = 50
        elif self.cheese == 'smoked_cheese':
            self.image = pg.transform.scale(pg.image.load('Assets/cheeses/smoked_cheese1.png'), (100, 85))
            self.rect = self.image.get_rect(center=(pos))
            self.speed = 4
            self.stage = 2
        elif self.cheese == 'saganaki':
            self.image = pg.transform.scale(pg.image.load('Assets/cheeses/saganaki.png'), (100, 65))
            self.rect = self.image.get_rect(center=(pos))
            self.speed = 5
            self.oil_time = 600
            self.oil_timer = 0
            self.burn_damage = 0.5
        elif self.cheese == 'anthotyro':
            self.image = pg.transform.scale(pg.image.load('Assets/cheeses/anthotyro.png'), (100, 115))
            self.rect = self.image.get_rect(center=(pos))
            self.speed = 5
            self.time_addition = 20/100
        self.mask = pg.mask.from_surface(self.image)
        self.bomb = bomb
        self.bomb_timer = 0
        self.trap_limit = 1
        self.total_time_trap = 240

    def place_timer(self):
        if self.bomb == False:
            self.bomb_timer += 1
            if self.bomb_timer > self.total_time_trap:
                self.bomb = True
                self.bomb_timer = 0

    def update(self):
        keys = pg.key.get_pressed()
        if keys[controls["up"]] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[controls['down']] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed

    def change_form_cheddar(self , stage):
        if self.cheese == 'cheddar':
            if stage == 2:
                self.stage = stage
                self.speed = 5
                self.image = pg.transform.scale(pg.image.load('Assets/cheeses/cheddar_cheese2.png') , (100 , 75))
                self.mask = pg.mask.from_surface(self.image)
                cheddar_sound.play()

            elif stage == 3:
                self.stage = stage
                self.speed = 7
                self.image = pg.transform.scale(pg.image.load('Assets/cheeses/cheddar_cheese3.png') , (100 , 75))
                self.mask = pg.mask.from_surface(self.image)
                cheddar_sound.play()

    def change_form_smoked(self , stage):
        if self.cheese == 'smoked_cheese':
            if stage == 2:
                self.stage = stage
                self.image = pg.transform.scale(pg.image.load('Assets/cheeses/smoked_cheese2.png'), (100, 85))
                self.mask = pg.mask.from_surface(self.image)
                smoke_sound.play()
            elif stage == 3:
                self.stage = stage
                self.image = pg.transform.scale(pg.image.load('Assets/cheeses/smoked_cheese3.png'), (100, 85))
                self.mask = pg.mask.from_surface(self.image)
                smoke_sound.play()

            elif stage == 4:
                self.stage = stage
                self.image = pg.transform.scale(pg.image.load('Assets/cheeses/smoked_cheese4.png'), (100, 85))
                self.mask = pg.mask.from_surface(self.image)
                smoke_sound.play()

    def oil_drop(self , mice):
        if self.cheese == 'saganaki':
            self.oil_timer += 1
            if self.oil_timer >= self.oil_time and mice > 0:
                self.oil_timer = 0
                Oil(self.rect.midright , (all_entities , oil_drops))
                oil_drop_sound.play()

    def cream_drop(self , mice):
        if self.cheese == 'cream_cheese':
            self.cream_timer += 1
            if self.cream_timer >= self.cream_time and mice > 0:
                self.cream_timer = 0
                CreamDrop(self.rect.midright , (all_entities , cream_drops))
                cream_drop_sound.play()

    def rolling_cheese(self , mice , mouse1 , mouse2 , cheeses):
        if self.cheese == 'parmesan':
            if self.roll_ready:
                if mice > 3 and cheeses < 3:
                    RollingCheese((-100 , mouse1.rect.centery) , (all_entities , rolling_cheeses))
                    RollingCheese((-100 , mouse2.rect.centery) , (all_entities , rolling_cheeses))
                    rolling_cheese_sound.play()
                    self.roll_timer = 0
                    self.roll_ready = False

    def rolling_timer(self):
        self.roll_timer += 1
        if self.roll_timer >= self.roll_time:
            self.roll_ready = True

    def draw(self):
        screen.blit(self.image, self.rect)

class Laser(pg.sprite.Sprite):
    def __init__(self , pos , groups):
        super().__init__(groups)
        self.image = pg.image.load(join('Assets/bullets_effects/laser.png'))
        self.speed = 12
        self.rect = self.image.get_rect(midleft = (pos))

    def update(self):
        self.rect.centerx += self.speed
        if self.rect.left > WIDTH:
            self.kill()

    def draw(self):
        screen.blit(self.image , self.rect)

class NormalBullet(pg.sprite.Sprite):
    def __init__(self , pos , groups):
        super().__init__(groups)
        self.image = pg.transform.scale(pg.image.load(join('Assets/bullets_effects/bullet.png')) , (20 , 10))
        self.speed = 16
        self.rect = self.image.get_rect(midleft = (pos))

    def update(self):
        self.rect.centerx += self.speed
        if self.rect.left > WIDTH:
            self.kill()

    def draw(self):
        screen.blit(self.image , self.rect)

class ShotgunBulletMid(pg.sprite.Sprite):
    def __init__(self , pos , groups):
        super().__init__(groups)
        self.timer = 0
        self.image = pg.transform.scale(pg.image.load(join('Assets/bullets_effects/shotgun_bullet.png')) , (25 , 10))
        self.speed = 14
        self.rect = self.image.get_rect(midleft = (pos))

    def update(self):
        self.rect.centerx += self.speed
        self.timer += 1
        if self.rect.left > WIDTH or self.timer > 10:
            self.kill()

    def draw(self):
        screen.blit(self.image , self.rect)

class ShotgunBulletTop(pg.sprite.Sprite):
    def __init__(self , pos , groups):
        super().__init__(groups)
        self.timer = 0
        self.image = pg.transform.rotate(pg.transform.scale(pg.image.load(join('Assets/bullets_effects/shotgun_bullet.png')) , (25 , 10)) , 25)
        self.speed = 14
        self.rect = self.image.get_rect(midbottom = pos)

    def update(self):
        self.rect.centerx += self.speed
        self.rect.centery -= self.speed / 2
        self.timer += 1
        if self.rect.left > WIDTH or self.rect.bottom < 0 or self.timer > 10:
            self.kill()

    def draw(self):
        screen.blit(self.image , self.rect)

class ShotgunBulletBottom(pg.sprite.Sprite):
    def __init__(self , pos , groups):
        super().__init__(groups)
        self.timer = 0
        self.image = pg.transform.rotate(pg.transform.scale(pg.image.load(join('Assets/bullets_effects/shotgun_bullet.png')) , (25 , 10)) , -25)
        self.speed = 14
        self.rect = self.image.get_rect(midtop = pos)

    def update(self):
        self.rect.centerx += self.speed
        self.rect.centery += self.speed / 2
        self.timer += 1
        if self.rect.left > WIDTH or self.rect.bottom < 0 or self.timer > 10:
            self.kill()

    def draw(self):
        screen.blit(self.image , self.rect)

class SniperBullet(pg.sprite.Sprite):
    def __init__(self , pos , groups):
        super().__init__(groups)
        self.image = pg.transform.scale(pg.image.load(join('Assets/bullets_effects/rat_slayer_bullet.png')) , (40 , 10))
        self.speed = 35
        self.rect = self.image.get_rect(midleft = (pos))

    def update(self):
        self.rect.centerx += self.speed
        if self.rect.left > WIDTH:
            self.kill()

    def draw(self):
        screen.blit(self.image , self.rect)

class Missile(pg.sprite.Sprite):
    def __init__(self , pos , groups):
        super().__init__(groups)
        self.image = pg.transform.scale(pg.image.load(join('Assets/bullets_effects/ratzooka_missile.png')) , (112 , 28))
        self.speed = 20
        self.rect = self.image.get_rect(midleft = (pos))

    def update(self):
        self.rect.centerx += self.speed
        if self.rect.left > WIDTH:
            self.kill()

    def draw(self):
        screen.blit(self.image , self.rect)

class MissileExplosion(pg.sprite.Sprite):
    def __init__(self , pos , groups):
        super().__init__(groups)
        self.image = pg.transform.scale(pg.image.load(join('Assets/bullets_effects/fire.png')) , (200 , 60))
        self.rect = self.image.get_rect(center = pos)
        self.timer = 0
        self.mask = pg.mask.from_surface(self.image)

    def update(self):
        self.timer += 1
        if self.timer > 300:
            self.kill()

class AirWaveUp(pg.sprite.Sprite):
    def __init__(self , pos , groups):
        super().__init__(groups)
        self.timer = 0
        self.image = pg.transform.rotate(pg.transform.scale(pg.image.load(join('Assets/bullets_effects/air_wave.png')) , (120 , 90)) , 90)
        self.speed = 3
        self.rect = self.image.get_rect(midbottom = (pos))

    def update(self):
        self.rect.centery -= self.speed
        self.timer += 1
        if self.timer > 45:
            self.kill()

    def draw(self):
        screen.blit(self.image , self.rect)

class AirWaveDown(pg.sprite.Sprite):
    def __init__(self , pos , groups):
        super().__init__(groups)
        self.timer = 0
        self.image = pg.transform.rotate(pg.transform.scale(pg.image.load(join('Assets/bullets_effects/air_wave.png')) , (120 , 90)) , -90)
        self.speed = 3
        self.rect = self.image.get_rect(midtop = (pos))

    def update(self):
        self.rect.centery += self.speed
        self.timer += 1
        if self.timer > 45:
            self.kill()

    def draw(self):
        screen.blit(self.image , self.rect)

class Mouse(pg.sprite.Sprite):
    def __init__(self , x , y , width , height , mouse , groups):
        super().__init__(groups)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.mouse = mouse
        if self.mouse == 'mouse':
            self.original_image = pg.transform.scale(pg.image.load('Assets/mice/mouse.png') , (self.width , self.height))
            self.hp_max = 50
            self.speedx_original = 6
            self.speedy_original = 2
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)
        self.rect.x = self.x
        self.rect.y = self.y
        self.rotated = False
        self.cords = (self.x , self.y)
        self.speedx = self.speedx_original
        self.speedy = self.speedy_original
        self.burn = False
        self.creamed = False
        self.rotation = 0
        self.burn_timer = 0

        self.hp = self.hp_max
        self.hp_ratio = self.hp_max / 100

    def update(self):
        if self.creamed:
            self.speedy = 0
            self.rotation += 20
            if self.rect.centery >= HEIGHT/2:
                self.rect.y += 5
                self.image = pg.transform.rotate(self.original_image , self.rotation)
                self.rect = self.image.get_rect(center = self.rect.center)
            else:
                self.rect.y -= 5
                self.image = pg.transform.rotate(self.original_image , -self.rotation)
                self.rect = self.image.get_rect(center=self.rect.center)

        for player in player_group:
            if self.rect.bottom < 0 or self.rect.top > HEIGHT:
                self.kill()

            if self.rect.left > 45:
                self.cords = self.rect.midleft
                self.rect.x -= self.speedx

            else:
                if self.y < player.rect.y and not self.creamed:
                    if self.rotated == False:
                        self.image = pg.transform.rotate(pg.transform.scale(pg.image.load(join('Assets/mice/mousetop.png')), (150 , 60)), 90)
                        self.rect = self.image.get_rect(center = self.cords)
                        self.rect.centerx = 75
                        self.mask = pg.mask.from_surface(self.image)
                        self.rotated = True
                    self.y += self.speedy
                elif self.y > player.rect.y and not self.creamed:
                    if self.rotated == False:
                        self.image = pg.transform.rotate(pg.transform.scale(pg.image.load(join('Assets/mice/mousetop.png')), (150, 60)), -90)
                        self.rect = self.image.get_rect(center = self.cords)
                        self.rect.centerx = 75
                        self.mask = pg.mask.from_surface(self.image)
                        self.rotated = True
                    self.y -= self.speedy
        if not self.creamed: self.rect.y = self.y
        if self.rect.bottom < 0 or self.rect.top > HEIGHT:
            self.kill()

    def burn_damage(self , dmg):
        if self.burn:
            self.damage(dmg)
            self.burn_timer += 1
        if self.burn_timer == 1:
            burn_sound.play()

    def draw(self):
        screen.blit(self.image , self.rect)

    def health_bar(self):
        pg.draw.rect(screen , 'red' , (self.rect.left , self.rect.top - 8 , self.hp / self.hp_ratio , 10) , 0 , 4)
        pg.draw.rect(screen, BLACK, (self.rect.left , self.rect.top - 8 , 100 , 10), 2, 4)

        if self.hp <= 0:
            self.kill()
            mouse_death.play()
            if self.burn:
                burn_sound.stop()

    def damage(self , dmg):
        self.hp -= dmg
        if self.hp <= 0:
            self.hp = 0

class PoisonExplosion(pg.sprite.Sprite):
    def __init__(self , pos , groups):
        super().__init__(groups)
        self.image = pg.image.load(join('Assets/bullets_effects/explosion2.png'))
        self.rect = self.image.get_rect(center = pos)
        self.timer = 0

    def update(self):
        self.timer += 1
        if self.timer > 30:
            self.kill()

class Trap(pg.sprite.Sprite):
    def __init__(self , pos , trap , groups):
        super().__init__(groups)
        self.trap = trap
        if self.trap == 'poison_trap':
            self.image = pg.transform.scale(pg.image.load(join('Assets/traps/poison_trap.webp')), (50 , 50))
        elif self.trap == 'rat_trap':
            self.image = pg.transform.rotate(pg.transform.scale(pg.image.load(join('Assets/traps/trap_right.png')), (120 , 55)) , 10)
        elif self.trap == 'glue_trap':
            self.image = pg.transform.scale(pg.image.load(join('Assets/traps/glue_trap.png')), (125 , 60))
        elif self.trap == 'parasite_trap':
            self.image = pg.transform.scale(pg.image.load(join('Assets/traps/parasite_trap.png')), (50 , 50))
        elif self.trap == 'fall_trap':
            self.image = pg.transform.rotate(pg.transform.scale(pg.image.load(join('Assets/traps/fall_trap.png')), (120 , 90)) , 8)
        elif self.trap == 'shock_trap':
            self.image = pg.transform.scale(pg.image.load(join('Assets/traps/shock_trap.png')), (100 , 60))
        elif self.trap == 'spring_trap':
            self.image = pg.transform.scale(pg.image.load(join('Assets/traps/spring_trap_inactive.png')), (50 , 75))

        self.rect = self.image.get_rect(center = pos)


    def draw(self):
        screen.blit(self.image , self.rect)

class PlankUp(pg.sprite.Sprite):
    def __init__(self , pos , groups):
        super().__init__(groups)
        self.original_image = pg.transform.rotate(pg.transform.scale(pg.image.load(join('Assets/cheeses/plank.png')) , (90 , 50)) , 25)
        self.image = self.original_image
        self.speed = 4
        self.rect = self.image.get_rect(midbottom = (pos))
        self.rotation = 0

    def update(self):
        self.rotation += 5
        self.image = pg.transform.rotate(self.original_image , self.rotation)
        self.rect = self.image.get_rect(center = self.rect.center)
        self.rect.centery -= self.speed
        if self.rect.bottom < 0:
            self.kill()

class PlankDown(pg.sprite.Sprite):
    def __init__(self , pos , groups):
        super().__init__(groups)
        self.original_image = pg.transform.rotate(pg.transform.scale(pg.image.load(join('Assets/cheeses/plank.png')) , (90 , 50)) , -25)
        self.image = self.original_image
        self.speed = 4
        self.rect = self.image.get_rect(midbottom = (pos))
        self.rotation = 0

    def update(self):
        self.rotation -= 5
        self.image = pg.transform.rotate(self.original_image , self.rotation)
        self.rect = self.image.get_rect(center = self.rect.center)
        self.rect.centery += self.speed
        if self.rect.bottom < 0:
            self.kill()

class PlankRandom(pg.sprite.Sprite):
    def __init__(self , pos , groups):
        super().__init__(groups)
        self.original_image = pg.transform.scale(pg.image.load(join('Assets/cheeses/plank.png')) , (90 , 50))
        self.image = self.original_image
        self.speedx = randint(3 , 8)
        self.speedy = random.choice((3 , -3))
        self.rect = self.image.get_rect(midbottom = (pos))
        self.rotation = 0

    def update(self):
        self.rotation += 5
        self.image = pg.transform.rotate(self.original_image , self.rotation)
        self.rect = self.image.get_rect(center = self.rect.center)
        self.rect.centery -= self.speedy
        self.rect.centerx += self.speedx
        if self.rect.bottom < 0:
            self.kill()

class BlueArea(pg.sprite.Sprite):
    def __init__(self , pos , groups):
        super().__init__(groups)
        self.image = pg.transform.scale(pg.image.load('Assets/cheeses/blue_area.png') , (350 , 340))
        self.rect = self.image.get_rect(center = pos)
        self.mask = pg.mask.from_surface(self.image)

    def move(self , pl_center):
        self.rect.center = pl_center

class SmokeUp(pg.sprite.Sprite):
    def __init__(self , pos , groups):
        super().__init__(groups)
        self.image = pg.transform.rotate(pg.transform.scale(pg.image.load(join('Assets/bullets_effects/smoke.png')) , (120 , 90)) , 90)
        self.speed = 8
        self.rect = self.image.get_rect(midbottom = (pos))

    def update(self):
        self.rect.centery -= self.speed
        if self.rect.bottom < 0:
            self.kill()

    def draw(self):
        screen.blit(self.image , self.rect)

class SmokeDown(pg.sprite.Sprite):
    def __init__(self , pos , groups):
        super().__init__(groups)
        self.image = pg.transform.rotate(pg.transform.scale(pg.image.load(join('Assets/bullets_effects/smoke.png')) , (120 , 90)) , -90)
        self.speed = 8
        self.rect = self.image.get_rect(midtop = (pos))

    def update(self):
        self.rect.centery += self.speed
        if self.rect.top > HEIGHT:
            self.kill()

    def draw(self):
        screen.blit(self.image , self.rect)

class Smoke(pg.sprite.Sprite):
    def __init__(self , pos , groups):
        super().__init__(groups)
        self.image = pg.transform.scale(pg.image.load(join('Assets/bullets_effects/smoke.png')) , (120 , 90))
        self.speed = 8
        self.rect = self.image.get_rect(midleft = (pos))

    def update(self):
        self.rect.centerx += self.speed
        if self.rect.left > WIDTH:
            self.kill()

    def draw(self):
        screen.blit(self.image , self.rect)

class Oil(pg.sprite.Sprite):
    def __init__(self , pos , groups):
        super().__init__(groups)
        self.original_image = pg.transform.rotate(pg.transform.scale(pg.image.load(join('Assets/bullets_effects/oil_drop.png')) , (30 , 40)) , 90)
        self.image = self.original_image
        self.speed = 20
        self.rect = self.image.get_rect(midleft = (pos))
        self.rotation = 0

    def rotate(self):
        self.rotation += 20
        self.image = pg.transform.rotate(self.original_image, self.rotation)
        self.rect = self.image.get_rect(center=self.rect.center)

    def move(self , mouse):
        distancex = mouse.rect.centerx - self.rect.centerx
        distancey = mouse.rect.centery - self.rect.centery
        if distancex > 0:
            if distancex > 600:
                self.rect.x += distancex / 50
            elif distancex > 400:
                self.rect.x += distancex / 25
            elif distancex > 200:
                self.rect.x += distancex / 15
            else:
                self.rect.x += distancex / 5
        elif distancex < 0:
            if distancex < -600:
                self.rect.x += abs(distancex / 50)
            elif distancex < -400:
                self.rect.x -= abs(distancex / 25)
            elif distancex < -200:
                self.rect.x -= abs(distancex / 15)
            else:
                self.rect.x -= abs(distancex / 5)


        if distancey > 0:
            if distancey > 400:
                self.rect.y += distancey / 30
            if distancey > 200:
                self.rect.y += distancey / 15
            else:
                self.rect.y += distancey / 7
        elif distancey < 0:
            if distancey < -400:
                self.rect.y -= abs(distancey / 30)
            if distancey < -200:
                self.rect.y -= abs(distancey / 15)
            else:
                self.rect.y -= abs(distancey / 7)

    def draw(self):
        screen.blit(self.image , self.rect)

class CreamDrop(pg.sprite.Sprite):
    def __init__(self , pos , groups):
        super().__init__(groups)
        self.original_image = pg.transform.rotate(pg.transform.scale(pg.image.load(join('Assets/bullets_effects/cream_drop.png')) , (30 , 40)) , 90)
        self.image = self.original_image
        self.speed = 15
        self.rect = self.image.get_rect(midleft = (pos))
        self.rotation = 0

    def rotate(self):
        self.rotation += 15
        self.image = pg.transform.rotate(self.original_image, self.rotation)
        self.rect = self.image.get_rect(center=self.rect.center)

    def move(self , mouse):
        distancex = mouse.rect.centerx - self.rect.centerx
        distancey = mouse.rect.centery - self.rect.centery
        if distancex > 0:
            if distancex > 600:
                self.rect.x += distancex / 60
            elif distancex > 400:
                self.rect.x += distancex / 35
            elif distancex > 200:
                self.rect.x += distancex / 25
            else:
                self.rect.x += distancex / 10
        elif distancex < 0:
            if distancex < -600:
                self.rect.x += abs(distancex / 60)
            elif distancex < -400:
                self.rect.x -= abs(distancex / 35)
            elif distancex < -200:
                self.rect.x -= abs(distancex / 25)
            else:
                self.rect.x -= abs(distancex / 10)


        if distancey > 0:
            if distancey > 400:
                self.rect.y += distancey / 35
            if distancey > 200:
                self.rect.y += distancey / 20
            else:
                self.rect.y += distancey / 8
        elif distancey < 0:
            if distancey < -400:
                self.rect.y -= abs(distancey / 35)
            if distancey < -200:
                self.rect.y -= abs(distancey / 20)
            else:
                self.rect.y -= abs(distancey / 8)

    def draw(self):
        screen.blit(self.image , self.rect)

class Cream(pg.sprite.Sprite):
    def __init__(self , pos , groups):
        super().__init__(groups)
        self.image = pg.transform.scale(pg.image.load(join('Assets/bullets_effects/cream_puddle.png')) , (150 , 120))
        self.rect = self.image.get_rect(center = pos)
        self.timer = 0

    def update(self):
        self.timer += 1
        if self.timer > 600:
            self.kill()

class RollingCheese(pg.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pg.transform.scale(pg.image.load(join('Assets/cheeses/rolling_cheese.png')), (60, 45))
        self.speed = 8
        self.rect = self.image.get_rect(midleft=(pos))

    def update(self):
        self.rect.centerx += self.speed
        if self.rect.left > WIDTH:
            self.kill()

    def draw(self):
        screen.blit(self.image, self.rect)

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

class Timer():
    def __init__(self , frames):
        self.frames = frames
        self.done = True
        self.count = 0

    def timer(self):
        if not self.done:
            self.count += 1
            if self.count >= self.frames:
                self.done = True
                self.count = 0

    def start(self):
        self.done = False

    def set_frames(self , frames):
        self.frames = frames


def double_click(key):
    current_time = pg.time.get_ticks()

    if key in last_press:
        if current_time - last_press[key] <= 500:
            last_press.pop(key)
            print('Double')
            return True

    last_press[key] = current_time
    return False

def collisions(bullet_damage):
    for player in player_group:
        pl_collide = pg.sprite.spritecollide(player, mouse_entities , False)
        if pl_collide:
            pl_collide_mask = pg.sprite.spritecollide(player , mouse_entities , False , pg.sprite.collide_mask)
            if pl_collide_mask:
                if player.cheese == 'feta_barrel':
                    PlankUp(player.rect.midtop , (all_entities , planks))
                    PlankDown(player.rect.midbottom , (all_entities , planks))
                    for i in range(0 , player.plank_number):
                        PlankRandom(player.rect.midright , (all_entities , planks))
                    player.image = pg.transform.scale(pg.image.load('Assets/cheeses/feta.png'), (90, 75))
                    player.rect = player.image.get_rect(center = player.rect.center)
                    player.mask = pg.mask.from_surface(player.image)
                    player.cheese = 'feta'
                    player.speed = 5
                    barrel_sound.play()
                    for gun in gun_group:
                        gun.speed = player.speed

                elif player.cheese == 'smoked_cheese':
                    SmokeUp(player.rect.midtop , (all_entities , smokes_up))
                    SmokeDown(player.rect.midbottom, (all_entities, smokes_down))
                    Smoke(player.rect.midright, (all_entities, smokes))
                    if player.stage == 1:
                        player.change_form_smoked(2)
                    elif player.stage == 2:
                        player.change_form_smoked(3)
                    elif player.stage == 3:
                        player.change_form_smoked(4)
                    else:
                        player_death.play(1)
                        game_over = True
                        gameover()

                else:
                    player_death.play(1)
                    game_over = True
                    gameover()

    for trap in trap_entities:
        coll = pg.sprite.spritecollide(trap , mouse_entities , False)
        if coll:
            trap_sound.play()
            trap.kill()
            PoisonExplosion(trap.rect.center , (explosion_entities , all_entities))

    for mouse in mouse_entities:
        collisisons = pg.sprite.spritecollide(mouse , explosion_entities , False)
        if collisisons:
            mouse.kill()

        fire_collision = pg.sprite.spritecollide(mouse, missile_explosions, False)
        if fire_collision:
            fire_collision_mask = pg.sprite.spritecollide(mouse, missile_explosions, False, pg.sprite.collide_mask)
            if fire_collision_mask:
                mouse.damage(0.2)

        laser_collision = pg.sprite.spritecollide(mouse, laser_entities, True)
        if laser_collision:
            mouse.damage(bullet_damage)

        bullet_collision = pg.sprite.spritecollide(mouse, normal_bullets, True)
        if bullet_collision:
            mouse.damage(bullet_damage)

        shotgun_collision = pg.sprite.spritecollide(mouse, shotgun_shells, True)
        if shotgun_collision:
            mouse.damage(bullet_damage)

        sniper_collision = pg.sprite.spritecollide(mouse, sniper_bullets, True)
        if sniper_collision:
            mouse.damage(bullet_damage)

        missile_collision = pg.sprite.spritecollide(mouse, missile_entities, True)
        if missile_collision:
            MissileExplosion(mouse.rect.center, (missile_explosions, all_entities))
            ratzooka_sound2.play()
            mouse.damage(bullet_damage)

        air_collision = pg.sprite.spritecollide(mouse , air_entities_up , False)
        if air_collision:
            mouse.y -= 4

        air_collision = pg.sprite.spritecollide(mouse, air_entities_down, False)
        if air_collision:
            mouse.y += 4

        plank_collision = pg.sprite.spritecollide(mouse, planks, False)
        if plank_collision:
            mouse.damage(player.plank_damage)

        blue_collision = pg.sprite.spritecollide(mouse , blue_area_group , False)
        if blue_collision:
            blue_collision_mask = pg.sprite.spritecollide(mouse , blue_area_group , False , pg.sprite.collide_mask)
            if blue_collision_mask:
                mouse.speedx = player.slow_x
                mouse.speedy = player.slow_y
        else:
            mouse.speedx = mouse.speedx_original
            mouse.speedy = mouse.speedy_original

        smoke_collision = pg.sprite.spritecollide(mouse, smokes, False)
        if smoke_collision:
            mouse.rect.x += 14
        if smoke_collision and mouse.rect.left > WIDTH - 10:
            mouse.kill()

        smoke_collision_up = pg.sprite.spritecollide(mouse , smokes_up , False)
        if smoke_collision_up:
            mouse.y -= 14

        smoke_collision_down = pg.sprite.spritecollide(mouse, smokes_down, False)
        if smoke_collision_down:
            mouse.y += 14

        oil_collision = pg.sprite.spritecollide(mouse , oil_drops , True)
        if oil_collision:
            mouse.burn = True

        cream_drop_collision = pg.sprite.spritecollide(mouse , cream_drops , True)
        if cream_drop_collision:
            Cream(mouse.rect.center , creams)
            cream_sound.play()

        cream_collision = pg.sprite.spritecollide(mouse , creams , False)
        if cream_collision:
            mouse.creamed = True
            slip_sound.play()

        rolling_cheese_collision = pg.sprite.spritecollide(mouse , rolling_cheeses , False)
        if rolling_cheese_collision:
            mouse.damage(player.cheese_damage)

def menu():
    pg.mixer.music.stop()
    screen.blit(floor , (-20 , -20))
    game_over = False

    screen.blit(pg.transform.scale(pg.image.load(join('Assets/rat_poisonleft.png')), (400 , 400)), (740 , 350))
    screen.blit(pg.transform.rotate(pg.transform.scale(pg.image.load(join('Assets/cheeses/cheeseleft.png')), (220 , 220)), -8), (700 , 520))
    screen.blit(pg.transform.scale(pg.image.load(join('Assets/mice/mouseright.png')), (400, 200)), (-120, 510))
    screen.blit(pg.transform.scale(pg.image.load(join('Assets/mice/mouseright.png')), (400 , 200)), (-20 , 565))
    screen.blit(pg.transform.scale(pg.image.load(join('Assets/mice/mouseright.png')), (400, 200)), (-140, 565))
    screen.blit(pg.transform.scale(pg.image.load(join('Assets/mice/mouseright.png')), (400, 200)), (-260, 565))

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
    global mouse_kills, highscore , high_score_notification , music , sound , pause_texts , m1_timer , m2_timer , m3_timer , m4_timer
    music_delay = 0
    menu_music.stop()
    screen.blit(floor , (-20 , -20))
    clock = pg.time.Clock()
    pause = False
    player = Player((75 , HEIGHT//2) , 'smoked_cheese' , True , (all_entities , player_group))
    gun = Gun(125 , HEIGHT//2 , 'ratzooka' , player.speed , True , (all_entities , gun_group))
    if gun.gun == 'rat_slayer':
        sniper_melee_timer = Timer(gun.fire_cooldown)
        melee_mice = 0
        gun_original_image = pg.transform.scale(pg.image.load('Assets/guns/bayonet_right.png') , (190 , 70))
    if player.cheese == 'anthotyro':
        m1_timer = int(m1_timer + m1_timer * player.time_addition)
        m2_timer = int(m2_timer + m2_timer * player.time_addition)
        m3_timer = int(m3_timer + m3_timer * player.time_addition)
        m4_timer = int(m4_timer + m4_timer * player.time_addition)
        pg.time.set_timer(mouse_event1, m1_timer)
        pg.time.set_timer(mouse_event2, m2_timer)
        pg.time.set_timer(mouse_event3, m3_timer)
        pg.time.set_timer(mouse_event4, m4_timer)
    total_score = 0
    highscore_num = 0
    play_num = 0
    game_over = False
    mouse_kills = 0
    mouse_history = 0
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

        # if 200 <= total_score <= 600:
        #     player.reload_time = 40
        #     player.total_time_trap = 200
        # elif 600 <= total_score <= 1300:
        #     player.speed = 7
        #     gun.speed = 7
        #     player.reload_time = 25
        #     player.total_time_trap = 150
        #     player.trap_limit = 2
        # elif 1300 <= total_score:
        #     player.reload_time = 20
        #     player.total_time_trap = 100
        #     player.trap_limit = 4


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
                if event.key == controls['fire'] and gun.can_shoot and not gun.cooldown:
                    if gun.gun == 'rat_poison':
                        laser_sound.play()
                        laser = Laser(gun.rect.midright , (all_entities, laser_entities))
                        gun.magazine -= 1
                    elif gun.gun == 'rat_killers' or gun.gun == 'ratata':
                        bullet_sound.play()
                        bullet = NormalBullet(gun.rect.midright, (all_entities, normal_bullets))
                        gun.magazine -= 1
                    elif gun.gun == 'rat_buster':
                        shotgun_sound.play()
                        bullet = ShotgunBulletMid(gun.rect.midright, (all_entities, shotgun_shells))
                        bullet1 = ShotgunBulletTop(bullet.rect.midtop , (all_entities , shotgun_shells))
                        bullet2 = ShotgunBulletBottom(bullet.rect.midbottom, (all_entities, shotgun_shells))
                        gun.magazine -= 1
                    elif gun.gun == 'rat_slayer':
                        for mouse in mouse_entities:
                            distance = mouse.rect.centery - player.rect.centery
                            if abs(distance) < 250 and mouse.rect.centerx < 100:
                                mouse.kill()
                                mouse_death.play()
                                sniper_melee_timer.start()
                                gun.melee = True
                                if distance > 0:
                                    gun.rotate('down' , 67)
                                elif distance < 0:
                                    gun.rotate('up' , 67)
                                melee_mice = 1
                                break
                        if melee_mice == 0:
                            rat_slayer_sound.play()
                            bullet = SniperBullet(gun.rect.midright, (all_entities, sniper_bullets))
                            gun.magazine -= 1
                        melee_mice = 0
                    elif gun.gun == 'ratzooka':
                        ratzooka_sound1.play()
                        bullet = Missile(gun.rect.midright, (all_entities, missile_entities))
                        AirWaveUp(player.rect.midtop , (all_entities , air_entities_up))
                        AirWaveDown(player.rect.midbottom, (all_entities, air_entities_down))
                        gun.magazine -= 1
                    gun.cooldown = True


                if event.key == controls['action'] and player.bomb and len(trap_entities) < player.trap_limit:
                    trap = Trap(player.rect.center , 'poison_trap', trap_entities)
                    player.bomb = False

                if event.key == controls['reload'] and gun.can_shoot:
                    gun.can_shoot = False

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
                        for trap in trap_entities:
                            trap.kill()
                        for area in blue_area_group:
                            area.kill()
                        menu_music.play(-1)
                        click_sound.play()
                        high_score_notification = False
                        menu()

            if event.type == mouse_event1 and total_score < 200:
                if not pause:
                    mouse_y = randint(30, 640)
                    mouse_speed = randint(2 , 5)
                    enemy = Mouse(900 , mouse_y , mouse_width , mouse_height , 'mouse' , (all_entities , mouse_entities))
                    mouse_spawn.play()
                    mouse_history += 1

            if event.type == mouse_event2 and 200 < total_score < 600:
                if not pause:
                    mouse_y = randint(30, 640)
                    mouse_speed = randint(3, 6)
                    enemy = Mouse(900 , mouse_y , mouse_width , mouse_height , 'mouse' , (all_entities , mouse_entities))
                    mouse_spawn.play()
                    mouse_history += 1

            if event.type == mouse_event3 and 600 < total_score < 1300:
                if not pause:
                    mouse_y = randint(30, 640)
                    mouse_speed = randint(4, 7)
                    enemy = Mouse(900, mouse_y, mouse_width, mouse_height, 'mouse', (all_entities, mouse_entities))
                    mouse_spawn.play()
                    mouse_history += 1

            if event.type == mouse_event4 and 1300 < total_score < 2000:
                if not pause:
                    mouse_y = randint(30, 640)
                    mouse_speed = randint(6, 9)
                    enemy = Mouse(900, mouse_y, mouse_width, mouse_height, 'mouse', (all_entities, mouse_entities))
                    mouse_spawn.play()
                    mouse_history += 1

            if event.type == mouse_event4 and 2000 < total_score:
                if not pause:
                    mouse_y = randint(30, 640)
                    mouse_speed = randint(8, 12)
                    enemy = Mouse(900, mouse_y, mouse_width, mouse_height, 'mouse', (all_entities, mouse_entities))
                    mouse_spawn.play()
                    mouse_history += 1

        if not pause and not game_over:
            screen.blit(floor, (-20, -20))
            if player.cheese == 'cheddar':
                if total_score == 300:
                    player.change_form_cheddar(2)
                    gun.speed = player.speed
                if total_score == 750:
                    player.change_form_cheddar(3)
                    gun.speed = player.speed
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

            print(gun.magazine)
            if gun.gun == "rat_slayer":
                sniper_melee_timer.timer()
                if gun.melee and sniper_melee_timer.done:
                    gun.rotate('right' , player.rect.centery)
                    gun.melee = False

            if mouse_history > len(mouse_entities):
                mouse_kills += 1
                mouse_history -= 1
            play_num += 1

            if player.cheese == 'blue_cheese':
                blue_area_group.draw(screen)
                for area in blue_area_group:
                    area.move(player.rect.center)
            elif player.cheese == 'saganaki':
                player.oil_drop(len(mouse_entities))
                for oil in oil_drops:
                    oil.rotate()
                    try:
                        oil.move(mouse_entities.sprites()[0])
                    except:
                        oil.rect.x += oil.speed
            elif player.cheese == 'cream_cheese':
                player.cream_drop(len(mouse_entities))
                creams.draw(screen)
                creams.update()
                for cream in cream_drops:
                    cream.rotate()
                    try:
                        cream.move(mouse_entities.sprites()[0])
                    except:
                        cream.rect.x += cream.speed
            elif player.cheese == 'parmesan':
                player.rolling_timer()
                try:
                    player.rolling_cheese(len(mouse_entities) , mouse_entities.sprites()[2] , mouse_entities.sprites()[3] , len(rolling_cheeses))
                except:
                    pass

            trap_entities.draw(screen)
            all_entities.update()
            all_entities.draw(screen)
            collisions(gun.damage)
            for mouse in mouse_entities:
                mouse.health_bar()
                if player.cheese == 'saganaki':
                    mouse.burn_damage(player.burn_damage)
            gun.fire_timer()
            player.place_timer()
            screen.blit(score_text, (0, 0))
            # for mouse in mouse_entities:
            #     pg.draw.rect(screen , 'green' , mouse.rect)
            # pg.draw.rect(screen , 'blue' , player.rect)
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
    reload_text = PresetText('reload' , (WIDTH//2 , 380) , preset_texts)

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
        text2b_rect = text2b.get_rect(center=(WIDTH // 2, 420))
        text2 = options_font1.render('Press ESC to pause', 1, 'green')
        text2_rect = text2.get_rect(center=(WIDTH // 2, 420))

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
                    if mouse[0] in range(reload_text.change_rect.left, reload_text.change_rect.right) and mouse[1] in range(reload_text.change_rect.top, reload_text.change_rect.bottom):
                        click_sound.play()
                        rebinding = 'reload'

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
        if rebinding == 'reload':
            reload_text.colour = reload_text.colour_active

        preset_texts.update()
        clock.tick(60)
        pg.display.flip()

def gameover():
    global highscore , mouse_kills , high_score_notification
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
                        for entity in all_entities:
                            entity.kill()
                        for trap in trap_entities:
                            trap.kill()
                        for area in blue_area_group:
                            area.kill()
                        score = 0
                        click_sound.play()
                        high_score_notification = False
                        play()
                    if mouse[0] in range(menu_button.rect.left, menu_button.rect.right) and mouse[1] in range(menu_button.rect.top,menu_button.rect.bottom):
                        for entity in all_entities:
                            entity.kill()
                        for trap in trap_entities:
                            trap.kill()
                        for area in blue_area_group:
                            area.kill()
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
        kills_text = gameover_text_font.render('Mice Killed :   ' + str(mouse_kills) , 1 , WHITE)
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