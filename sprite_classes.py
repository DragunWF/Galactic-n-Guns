import pygame
import random
import math

enemy_laser = pygame.sprite.Group()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(
            'Graphics/Player/playership.png').convert_alpha()
        self.rect = self.image.get_rect(center=(350, 550))
        self.effect, self.shield, self.pwr_name = False, 3, ''
        self.pwr_time_bolt, self.pwr_time_pills = 0, 0
        self.diagonal_movement, self.xy_axis_movement = 4.2, 6
        self.on_pills = False
        self.two_buffs = False
        self.laser_sound = pygame.mixer.Sound('Audio/laser1.ogg')
        self.damage_sound = pygame.mixer.Sound('Audio/Damage.wav')
        self.lose_sound = pygame.mixer.Sound('Audio/sfx_lose.ogg')
        self.laser_sound.set_volume(0.2)
        self.damage_sound.set_volume(0.5)
        self.lose_sound.set_volume(1.5)

    def shoot(self):
        self.laser_sound.play()

    def damaged(self):
        self.damage_sound.play()
        if self.shield <= 0:
            self.lose_sound.play()
            self.kill()
        self.shield -= 1

    def increase_shield(self):
        self.shield += 1

    def power_effect(self, effect):
        if not self.two_buffs:
            self.pwr_time_pills += 1 if effect == 'pill' else 0
            self.pwr_time_bolt += 1 if effect == 'bolt' else 0
        else:
            self.pwr_time_pills += 1
            self.pwr_time_bolt += 1
        self.pwr_name = effect
        seconds_passed_pills = math.floor(self.pwr_time_pills / 60)
        seconds_passed_bolt = math.floor(self.pwr_time_bolt / 60)
        time_limit_bolt, time_limit_pills = 20, 15
        if effect == 'bolt':
            self.xy_axis_movement = 10
            self.diagonal_movement = 7
        if effect == 'pill':
            self.on_pills = True
        if seconds_passed_pills >= time_limit_pills:
            self.on_pills = False
            self.pwr_time_pills = 0
            self.effect = True if self.two_buffs else False
            self.pwr_name = '' if not self.two_buffs else self.pwr_name
            if self.two_buffs:
                self.two_buffs = False
        if seconds_passed_bolt >= time_limit_bolt:
            self.xy_axis_movement, self.diagonal_movement = 6, 4.2
            self.pwr_time_bolt = 0
            self.effect = True if self.two_buffs else False
            self.pwr_name = '' if not self.two_buffs else self.pwr_name
            if self.two_buffs:
                self.two_buffs = False

    def powerup(self, type):
        pwr_types = ('bolt', 'pill', 'shield')
        for pwr in pwr_types:
            if pwr == type:
                if pwr != pwr_types[2]:
                    if not self.effect:
                        self.effect = True
                    else:
                        if type != self.pwr_name:
                            self.two_buffs = True
                    if pwr == pwr_types[0]:
                        self.pwr_time_bolt = 0
                    else:
                        self.pwr_time_pills = 0
                    self.pwr_name = type
                    self.power_effect(pwr)
                else:
                    self.increase_shield()

    def screen_limit(self):
        if self.rect.y >= 595:
            self.rect.y = 595
        if self.rect.y <= 330:
            self.rect.y = 330
        if self.rect.x <= 0:
            self.rect.x = 0
        if self.rect.x >= 596:
            self.rect.x = 596

    def player_input(self):
        key = pygame.key.get_pressed()
        if (key[pygame.K_w] or key[pygame.K_UP]) and (key[pygame.K_d] or key[pygame.K_RIGHT]):
            self.rect.x += self.diagonal_movement
            self.rect.y -= self.diagonal_movement
        elif (key[pygame.K_s] or key[pygame.K_DOWN]) and (key[pygame.K_a] or key[pygame.K_LEFT]):
            self.rect.x -= self.diagonal_movement
            self.rect.y += self.diagonal_movement
        elif (key[pygame.K_w] or key[pygame.K_UP]) and (key[pygame.K_a] or key[pygame.K_LEFT]):
            self.rect.x -= self.diagonal_movement
            self.rect.y -= self.diagonal_movement
        elif (key[pygame.K_s] or key[pygame.K_DOWN]) and (key[pygame.K_d] or key[pygame.K_RIGHT]):
            self.rect.x += self.diagonal_movement
            self.rect.y += self.diagonal_movement
        else:
            if key[pygame.K_w] or key[pygame.K_UP]:
                self.rect.y -= self.xy_axis_movement
            elif key[pygame.K_s] or key[pygame.K_DOWN]:
                self.rect.y += self.xy_axis_movement
            if key[pygame.K_a] or key[pygame.K_LEFT]:
                self.rect.x -= self.xy_axis_movement
            elif key[pygame.K_d] or key[pygame.K_RIGHT]:
                self.rect.x += self.xy_axis_movement

    def update(self):
        if self.effect:
            self.power_effect(self.pwr_name)
        self.player_input()
        self.screen_limit()


class Laser(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, type):
        super().__init__()
        cog = -5 if type == 1 else 55
        sprites = ('Graphics/Lasers/laserGreen08.png',
                   'Graphics/Lasers/laserRed04.png')
        self.image = pygame.image.load(sprites[type - 1]).convert_alpha()
        self.rect = self.image.get_rect(center=(x_pos + 55, y_pos + cog))
        self.type = type

    def move(self):
        if self.type == 1:
            self.rect.y -= 20
        else:
            self.rect.y += 10

    def delete_conditions(self):
        if self.rect.y <= -50:
            self.kill()

    def update(self):
        self.move()
        self.delete_conditions()


class Enemies(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        enemy_type, self.direction = random.randint(
            1, 5), random.choice(('left', 'right'))
        left_origin, right_origin, i = (
            (-30, 100), (-30, 230)), ((730, 100), (730, 230)), random.randint(0, 1)
        spawn_direction = left_origin[i] if self.direction == 'left' else right_origin[i]
        sprites = ('Graphics/Enemies/enemy1.png', 'Graphics/Enemies/enemy2.png',
                   'Graphics/Enemies/enemy3.png', 'Graphics/Enemies/enemy4.png',
                   'Graphics/Enemies/enemy5.png')
        sound_effects = ('Audio/laser2.ogg',
                         'Audio/laser3.ogg', 'Audio/laser4.ogg')
        self.image = pygame.image.load(sprites[enemy_type - 1]).convert_alpha()
        self.rect = self.image.get_rect(
            center=(spawn_direction))  # Add position later
        self.timer = 0
        self.speed, self.cooldown = random.randint(
            3, 6), random.choice((100, 150, 200))
        self.sound = pygame.mixer.Sound(random.choice(sound_effects))
        self.sound.set_volume(0.1)

    def shoot(self):
        global enemy_laser
        self.timer += 5
        if (self.timer % self.cooldown) == 0:
            self.sound.play()
            enemy_laser.add(Laser(self.rect.x, self.rect.y, 2))
            self.cooldown = random.choice((100, 150, 200))

    def move(self):
        if self.direction == 'left':
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed

    def delete_conditions(self):
        if self.rect.x <= -100 or self.rect.x >= 800:
            self.kill()

    def update(self):
        self.move()
        self.shoot()
        self.delete_conditions()


class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        x_pos = random.choice(
            (50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650))
        sprites = ('Graphics/Meteorites/big.png', 'Graphics/Meteorites/med.png',
                   'Graphics/Meteorites/small.png', 'Graphics/Meteorites/small.png')
        self.image = pygame.image.load(random.choice(sprites)).convert_alpha()
        self.rect = self.image.get_rect(center=(x_pos, -10))
        self.movement = 7 if type == 1 else 10
        self.angle = 0

    def move(self):
        self.rect.y += self.movement

    def delete_conditions(self):
        if self.rect.y >= 670:
            self.kill()

    def update(self):
        self.move()
        self.delete_conditions()


class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.power_type = random.randint(1, 3)
        powerups = ('Graphics/Powerups/bolt_gold.png', 'Graphics/Powerups/pill_green.png',
                    'Graphics/Powerups/shield_silver.png')
        sounds = ('Audio/bolt.ogg', 'Audio/pick_up.wav', 'Audio/armor_up.wav')
        self.powerup_names = ('bolt', 'pill', 'shield')
        x_pos = random.choice(
            (50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650))
        self.image = pygame.image.load(powerups[self.power_type - 1])
        self.rect = self.image.get_rect(center=(x_pos, -10))
        self.type = self.powerup_names[self.power_type - 1]
        self.sound = pygame.mixer.Sound(sounds[self.power_type - 1])
        if self.power_type != 3:
            self.sound.set_volume(0.2)
        else:
            self.sound.set_volume(0.05)

    def picked_up(self):
        self.sound.play()
        self.kill()

    def move(self):
        self.rect.y += 3

    def delete_conditions(self):
        if self.rect.y >= 670:
            self.kill()

    def update(self):
        self.move()
        self.delete_conditions()


class Explode(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        frame1 = pygame.image.load(
            'Graphics/Explode/explode1.png').convert_alpha()
        frame2 = pygame.image.load(
            'Graphics/Explode/explode2.png').convert_alpha()
        frame3 = pygame.image.load(
            'Graphics/Explode/explode3.png').convert_alpha()
        self.frames, self.index = (frame1, frame2, frame3), 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(center=(x_pos, y_pos))

    def animate(self):
        try:
            self.index += 0.15
            self.image = self.frames[int(self.index)]
        except IndexError:
            self.kill()

    def update(self):
        self.animate()


class LaserHit(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.image = pygame.image.load(
            'Graphics/Lasers/redframe1.png').convert_alpha()
        self.rect = self.image.get_rect(center=(x_pos, y_pos))
        self.time_passed = 0

    def time_on_screen(self):
        self.time_passed += 1
        quarter_seconds_passed = math.floor(self.time_passed / 4)
        if quarter_seconds_passed > 3:
            self.kill()

    def update(self):
        self.time_on_screen()
