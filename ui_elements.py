import pygame

pygame.init()
screen = pygame.display.set_mode((700, 650))

font = pygame.font.Font('Font/KenneyFuture.ttf', 20)
button_font = pygame.font.Font('Font/KenneyFuture.ttf', 35)
title_font = pygame.font.Font('Font/KenneyFuture.ttf', 50)

powerups = ('Graphics/Powerups/bolt_gold.png', 'Graphics/Powerups/pill_green.png',
            'Graphics/Powerups/shield_silver.png')
abilities = ('speed', 'multi-shot', 'shield')

buttons = pygame.sprite.Group()
normal_button = pygame.sprite.GroupSingle()
insane_button = pygame.sprite.GroupSingle()
again_button = pygame.sprite.GroupSingle()
menu_button = pygame.sprite.GroupSingle()
buttons_spawned = False


class Button(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, text, type):
        super().__init__()
        blue = pygame.image.load(
            'Graphics/UI/blue_button00.png').convert_alpha()
        red_hovered = pygame.image.load(
            'Graphics/UI/red_button11.png').convert_alpha()
        red_pushed = pygame.image.load(
            'Graphics/UI/red_button12.png').convert_alpha()
        self.type = type
        # self.normal, self.insane, self.again, self.menu = False, False, False, False
        self.buttons = {'normal': False, 'insane': False,
                        'again': False, 'menu': False}
        self.modes = (blue, red_hovered, red_pushed)
        self.image = self.modes[0]
        self.image = pygame.transform.scale2x(self.image)
        self.rect = self.image.get_rect(center=(x_pos, y_pos))
        self.font = button_font.render(text, True, (255, 255, 255))
        self.font_rect = self.font.get_rect(center=(x_pos, y_pos))
        self.sound = pygame.mixer.Sound('Audio/click1.ogg')
        self.pressed = False

    def delete(self):
        self.kill()

    def transition(self):
        func_types = ('normal', 'insane', 'again', 'menu')
        # button_func = [self.normal, self.insane, self.again, self.menu]
        self.time += 1
        if self.time > 30:
            for x in range(4):
                if self.type == func_types[x]:
                    self.buttons[self.type] = True
                    return

    def push(self):
        self.image = self.modes[2]
        self.image = pygame.transform.scale2x(self.image)
        self.sound.play()
        self.pressed = True
        self.time = 0

    def hover_check(self, pos, mouse_pressed):
        if self.rect.collidepoint(pos):
            self.image = self.modes[1]
            self.image = pygame.transform.scale2x(self.image)
            if mouse_pressed:
                self.push()
        else:
            self.image = self.modes[0]
            self.image = pygame.transform.scale2x(self.image)

    def update(self, mouse_pos, mouse_pressed):
        screen.blit(self.font, self.font_rect)
        if not self.pressed:
            self.hover_check(mouse_pos, mouse_pressed)
        else:
            self.transition()


def score(value):
    score_text = font.render(f'Score: {value}', True, (255, 255, 255))
    score_text_rect = score_text.get_rect(midleft=(20, 35))
    screen.blit(score_text, score_text_rect)


def powerup_display(power, state, two_buffs):
    global ability_state
    if not two_buffs:
        ability_text = 'None' if not state else abilities[power - 1]
    else:
        ability_text = 'Speed & Multi-shot'
    display_text = font.render(f"Buff: {ability_text}", True, (255, 255, 255))
    display_rect = display_text.get_rect(midleft=(20, 70))
    screen.blit(display_text, display_rect)


def shield_display(player_shields):
    level_text = 'Level' if player_shields > 0 else 'None'
    player_shields = '' if player_shields <= 0 else player_shields
    shield_text = font.render(
        f"Shields: {level_text} {player_shields}", True, (255, 255, 255))
    shield_rect = shield_text.get_rect(midleft=(20, 105))
    screen.blit(shield_text, shield_rect)


def main_menu(mouse_pos, mouse_pressed):
    global buttons_spawned
    if not buttons_spawned:
        normal_button.add(Button(350, 250, 'Normal Mode', 'normal'))
        insane_button.add(Button(350, 400, 'Insane Mode', 'insane'))
        buttons_spawned = True

    title = title_font.render("Galactic n' Guns", True, (255, 255, 255))
    title_rect = title.get_rect(center=(350, 100))
    name = title_font.render("By: DragonWF", True, (255, 255, 255))
    name_rect = name.get_rect(center=(350, 550))
    screen.blit(title, title_rect), screen.blit(name, name_rect)

    normal_button.draw(screen)
    normal_button.update(mouse_pos, mouse_pressed)
    insane_button.draw(screen)
    insane_button.update(mouse_pos, mouse_pressed)


def retry_screen(score, mouse_pos, mouse_pressed):
    global buttons_spawned
    if not buttons_spawned:
        again_button.add(Button(350, 250, 'Try again', 'again'))
        menu_button.add(Button(350, 400, 'Main Menu', 'menu'))
        buttons_spawned = True

    title = title_font.render("You died!", True, (255, 255, 255))
    title_rect = title.get_rect(center=(350, 100))
    score_text = title_font.render(f"Score: {score}", True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(350, 550))
    screen.blit(title, title_rect), screen.blit(score_text, score_rect)

    again_button.draw(screen)
    again_button.update(mouse_pos, mouse_pressed)
    menu_button.draw(screen)
    menu_button.update(mouse_pos, mouse_pressed)
