import pygame
import sprite_classes as spr
import ui_elements as ui
from sys import exit

pygame.init()
screen = pygame.display.set_mode((700, 650))
clock = pygame.time.Clock()
icon = pygame.image.load('Graphics/icon.png')
pygame.display.set_caption("Galactic n' Guns")  # Change name later
pygame.display.set_icon(icon)

gameover = True
main_menu = True
retry_screen = False
mouse_ui_pressed = False
buttons = ui.buttons
song, song_volume, audio_paused = pygame.mixer.Sound(
    'Audio/ending.wav'), 0.1, False
song.set_volume(song_volume)

player = pygame.sprite.GroupSingle()
lasers = pygame.sprite.Group()
powerups, pwr_value, prev_value = pygame.sprite.Group(), 0, None
score_value = 0
difficulty = ''

enemies = pygame.sprite.Group()
enemy_lasers = spr.enemy_laser
meteorites = pygame.sprite.Group()
effects = pygame.sprite.Group()

background = pygame.image.load('Graphics/background.png').convert_alpha()
background2 = pygame.image.load('Graphics/background2.png').convert_alpha()
bg_movement = 0

shoot_cooldown, shoot_time = pygame.USEREVENT + 1, 0
spawn_timer = pygame.USEREVENT + 2
meteor_timer = pygame.USEREVENT + 3
powerup_timer = pygame.USEREVENT + 4
score_timer = pygame.USEREVENT + 5
damage_timer, dmg_vul = pygame.USEREVENT + 6, False
scaling_timer, scale_time, scale_level = pygame.USEREVENT + 7, 30000, 15
gameover_timer = pygame.USEREVENT + 8
start_timer = pygame.USEREVENT + 9
back_to_menu_timer = pygame.USEREVENT + 10
in_game_start_timer = pygame.USEREVENT + 11

pygame.time.set_timer(scaling_timer, scale_time)
button_cog = False


def scaling_difficulty():
    global scale_level
    print(f'Scale level {scale_level}')
    if scale_level > 1:
        pygame.time.set_timer(spawn_timer, 350 * scale_level)  # 250
        pygame.time.set_timer(meteor_timer, 150 * scale_level)  # 100
        pygame.time.set_timer(powerup_timer, 450 * (scale_level + 5))
        scale_level -= 1


def collision_check():
    def player_damaged():
        global dmg_vul
        pygame.time.set_timer(damage_timer, 250)
        dmg_vul = True
        if player.sprite:
            if player.sprite.shield <= 0:
                effects.add(spr.Explode(
                    player.sprite.rect.x + 60, player.sprite.rect.y + 20))
                pygame.time.set_timer(gameover_timer, 3000)
            player.sprite.damaged()
    global score_value, pwr_value, prev_value
    meteors_collided = pygame.sprite.groupcollide(
        lasers, meteorites, True, True)
    enemies_collided = pygame.sprite.groupcollide(lasers, enemies, True, True)
    powerups_collected = pygame.sprite.spritecollide(
        player.sprite, powerups, False)
    meteors_hit = pygame.sprite.spritecollide(player.sprite, meteorites, True)
    lasers_hit = pygame.sprite.spritecollide(player.sprite, enemy_lasers, True)

    if powerups_collected:
        pwr_type = ('bolt', 'pill', 'shield')
        for powerup in powerups_collected:
            for x in range(3):
                if powerup.type == pwr_type[x]:
                    player.sprite.powerup(pwr_type[x])
            if powerup.type != pwr_type[2]:
                pwr_value = powerup.power_type
                prev_value = powerup.power_type
            else:
                pwr_value = prev_value
            powerup.picked_up()

    for enemy in enemies_collided:
        effects.add(spr.Explode(enemy.rect.x + 15, enemy.rect.y - 25))
        score_value += 5
    for meteor in meteors_collided:
        effects.add(spr.Explode(meteor.rect.x, meteor.rect.y))
        score_value += 3
    if not dmg_vul:
        for meteor in meteors_hit:
            effects.add(spr.Explode(meteor.rect.x + 25, meteor.rect.y + 50))
            player_damaged()
        for laser in lasers_hit:
            effects.add(spr.LaserHit(laser.rect.x +
                        25, laser.rect.y + 45))
            player_damaged()


def start_game():
    global scale_level, difficulty, score_value, insane_mode_song, song
    if difficulty == 'normal':
        scale_level = 10
        song.play(loops=-1)
    elif difficulty == 'insane':
        scale_level = 5
        song.play(loops=-1)
    score_value = 0
    player.add(spr.Player())
    pygame.time.set_timer(in_game_start_timer, 1000)


def reset_game():
    pygame.time.set_timer(spawn_timer, 0)
    pygame.time.set_timer(meteor_timer, 0)
    pygame.time.set_timer(powerup_timer, 0)
    enemies.empty(), enemy_lasers.empty(), powerups.empty()
    meteorites.empty(), effects.empty()


while True:  # Game loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if not gameover:
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or event.type == pygame.MOUSEBUTTONDOWN:
                if shoot_time == 0 and player.sprite:
                    player.sprite.shoot()
                    lasers.add(spr.Laser(player.sprite.rect.x,
                                         player.sprite.rect.y, 1))
                    if player.sprite.on_pills:
                        lasers.add(spr.Laser(player.sprite.rect.x +
                                             45, player.sprite.rect.y + 60, 1))
                        lasers.add(spr.Laser(player.sprite.rect.x -
                                             45, player.sprite.rect.y + 60, 1))
                    shoot_time = 100 if not player.sprite.on_pills else 50
                    pygame.time.set_timer(shoot_cooldown, shoot_time)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    if song_volume > 0:
                        song_volume = 0
                    else:
                        song_volume = 0.1
                    song.set_volume(song_volume)
                if event.key == pygame.K_q:
                    if not audio_paused:
                        audio_paused = True
                    else:
                        audio_paused = False
            if event.type == shoot_cooldown:
                shoot_time = 0
                pygame.time.set_timer(shoot_cooldown, shoot_time)
            if event.type == meteor_timer:
                meteorites.add(spr.Meteor())
            if event.type == spawn_timer:
                enemies.add(spr.Enemies())
            if event.type == score_timer:
                if player.sprite:
                    score_value += 1
            if event.type == scaling_timer:
                scaling_difficulty()
            if event.type == powerup_timer:
                powerups.add(spr.PowerUp())
            if event.type == damage_timer:
                dmg_vul = False
                pygame.time.set_timer(damage_timer, 0)
            if event.type == in_game_start_timer:
                pygame.time.set_timer(in_game_start_timer, 0)
                pygame.time.set_timer(score_timer, 1000)
                scaling_difficulty()
            if event.type == gameover_timer:
                pygame.time.set_timer(gameover_timer, 0)
                pygame.time.set_timer(score_timer, 0)
                ui.buttons_spawned, button_cog = False, False
                song.stop()
                gameover = True
                retry_screen = True
                reset_game()
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_ui_pressed = True
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_ui_pressed = False
            if event.type == start_timer:
                gameover = False
                main_menu = False if main_menu else main_menu
                retry_screen = False if retry_screen else retry_screen
                ui.buttons_spawned = False
                # ui.normal_button.sprite.delete(), ui.insane_button.sprite.delete()
                pygame.time.set_timer(start_timer, 0), start_game()
            if event.type == back_to_menu_timer:
                pygame.time.set_timer(back_to_menu_timer, 0)
                ui.buttons_spawned = False
                # ui.again_button.sprite.delete(), ui.menu_button.sprite.delete()
                retry_screen = False
                button_cog = False
                main_menu = True
    if gameover:
        mouse_pos = pygame.mouse.get_pos()
        screen.blit(background2, (0, bg_movement))
        screen.blit(background2, (0, -650 + bg_movement))
        if (bg_movement % 650) == 0:
            bg_movement = 0
        bg_movement += 5
        if not button_cog:
            if main_menu:
                ui.main_menu(mouse_pos, mouse_ui_pressed)
                if ui.normal_button.sprite.buttons['normal']:
                    pygame.time.set_timer(start_timer, 200)
                    difficulty = 'normal'
                    button_cog = True
                    ui.normal_button.sprite.buttons['normal'] = False
                elif ui.insane_button.sprite.buttons['insane']:
                    pygame.time.set_timer(start_timer, 200)
                    difficulty = 'insane'
                    button_cog = True
                    ui.insane_button.sprite.buttons['insane'] = False
            if retry_screen:
                ui.retry_screen(score_value, mouse_pos, mouse_ui_pressed)
                if ui.again_button.sprite.buttons['again']:
                    pygame.time.set_timer(start_timer, 300)
                    button_cog = True
                    ui.again_button.sprite.buttons['again'] = False
                elif ui.menu_button.sprite.buttons['menu']:
                    pygame.time.set_timer(back_to_menu_timer, 1)
                    button_cog = True
                    ui.menu_button.sprite.buttons['menu'] = False
    else:
        if audio_paused:
            pygame.mixer.pause()
        else:
            pygame.mixer.unpause()
        screen.blit(background, (0, bg_movement))
        screen.blit(background, (0, -650 + bg_movement))
        if (bg_movement % 650) == 0:
            bg_movement = 0
        bg_movement += 5

        powerups.update()
        powerups.draw(screen)

        lasers.update()
        lasers.draw(screen)
        enemy_lasers.update()
        enemy_lasers.draw(screen)

        player.update()
        player.draw(screen)

        meteorites.update()
        meteorites.draw(screen)

        enemies.update()
        enemies.draw(screen)

        effects.update()
        effects.draw(screen)

        ui.score(score_value)
        if player.sprite:
            ui.powerup_display(pwr_value, player.sprite.effect,
                               player.sprite.two_buffs)
            ui.shield_display(player.sprite.shield)
            collision_check()

    pygame.display.update()
    clock.tick(60)
