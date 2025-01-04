from random import randint

import pygame

from objects.Asteroid import Asteroid
from objects.Projectile import Projectile
from objects.Starship import Starship
from util import detect_events

# configuration
game_name = 'Asteroid Buster'
window_width = 1920
window_height = 1080
FPS = 30

facts = [
    "Asteroids can contain water ice and minerals",
    "Asteroids vary in size from small to massive",
    "Most asteroids orbit in the asteroid belt",
    "Ceres is the largest known asteroid object",
    "Some asteroids are remnants of early planets",
    "Asteroids can have irregular, rocky surfaces",
    "NASA studies asteroids to learn Earth's history",
    "Some asteroids pass close to Earth's orbit",
    "Impact craters are caused by asteroid collisions",
    "Asteroid mining may be future resource source"
]
game_over_fact = facts[randint(0, len(facts) - 1)]

# setup
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption(game_name)

# fonts
large_text_size = 60
medium_text_size = 30
small_text_size = 16
large_font = pygame.font.Font('assets/fonts/canavar.ttf', large_text_size)
medium_font = pygame.font.Font('assets/fonts/canavar.ttf', medium_text_size)
small_font = pygame.font.Font('assets/fonts/canavar.ttf', small_text_size)

# variables
rect_size = 32
rect_max_x = window_width - rect_size
rect_max_y = window_height - rect_size

# objects
spawn_space_rect = pygame.Rect(0, 0, 400, 400)
spawn_space_rect.center = (400, 300)



def create_asteroid_list():
    result: list[Asteroid] = []

    while len(result) < 1:
        asteroid = Asteroid(0, 0,
            rect_max_x, rect_max_y)
        if not asteroid.rect.colliderect(spawn_space_rect):
            result.append(asteroid)
    return result

asteroids: list[Asteroid] = []

projectiles: list[Projectile] = []

starship = Starship(400, 300)

game_state = 'starting'

# start game loop
while True:
    events = detect_events(pygame.event.get())
    keys_pressed = pygame.key.get_pressed()

    if keys_pressed[pygame.K_ESCAPE]:
        pygame.quit()
        break

    if game_state == 'starting':
        # fill the screen a solid color
        screen.fill('black')

        # create the game start heading
        start_text_render = medium_font.render('Press Space to Start', 1, 'white')
        heading_rect = start_text_render.get_rect(center=(window_width / 2, window_height / 2))

        # draw the game start screen
        screen.blit(start_text_render, heading_rect)

        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                asteroids = create_asteroid_list()
                game_state = 'running'
    elif game_state == 'running':
        if len(asteroids) == 0:
            game_state = 'won'

        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                projectiles.append(
                    Projectile(starship.rect.centerx, starship.rect.centery,
                               starship.angle))
    
        if keys_pressed[pygame.K_LEFT]:
            starship.rotate('left')
        if keys_pressed[pygame.K_RIGHT]:
            starship.rotate('right')
        if keys_pressed[pygame.K_UP]:
            starship.go('forward')
        if keys_pressed[pygame.K_DOWN]:
            starship.go('backward')

        if starship.rect.bottom > window_height:
            starship.rect.bottom = window_height
            starship.y_vel = 0
        if starship.rect.top < 0:
            starship.rect.top = 0
            starship.y_vel = 0
        if starship.rect.left < 0:
            starship.rect.left = 0
            starship.x_vel = 0
        if starship.rect.right > window_width:
            starship.rect.right = window_width
            starship.x_vel = 0

        # draw black background
        screen.fill('black')
        pygame.draw.rect(screen, 'white', screen.get_rect(), 2)
    
        # --- your code below ---
        for asteroid in asteroids:
            screen.blit(asteroid.img, asteroid.rect)
            asteroid.move()
            if asteroid.rect.right > window_width:
                asteroid.x_vel *= -1
                asteroid.rect.right = window_width
            if asteroid.rect.bottom > window_height:
                asteroid.y_vel *= -1
                asteroid.rect.bottom = window_height
            if asteroid.rect.top < 0:
                asteroid.y_vel *= -1
                asteroid.rect.top = 0
            if asteroid.rect.left < 0:
                asteroid.x_vel *= -1
                asteroid.rect.left = 0
            if asteroid.rect.colliderect(starship.rect):
                game_state = 'ended'
    
        for proj in projectiles:
            pygame.draw.rect(screen, 'white', proj.rect)
            for asteroid in asteroids:
                if proj.rect.colliderect(asteroid.rect):
                    asteroids.remove(asteroid)
                    projectiles.remove(proj)
            proj.move()
    
        screen.blit(starship.img, starship.rect)
        starship.move()
    
        # --- your code above ---
    elif game_state == 'won':
        # fill the screen a solid color
        screen.fill('black')

        # create the game over heading
        heading_render = large_font.render('You won!', 1, 'white')
        heading_rect = heading_render.get_rect(center=(window_width / 2, window_height / 2))

        # create the random fact text
        body_render = small_font.render(game_over_fact, 1, 'white')
        body_rect = body_render.get_rect(center=(window_width / 2, window_height / 2 + large_text_size + 40))

        restart_render = small_font.render('Play again? [press space to restart]', 1, 'white')
        restart_rect = body_rect.copy()
        restart_rect.y += 20

        # draw the game over screen
        screen.blit(heading_render, heading_rect)
        screen.blit(body_render, body_rect)
        screen.blit(restart_render, restart_rect)

        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                asteroids = create_asteroid_list()
                starship = Starship(400, 300)
                projectiles = []
                game_state = 'running'

    elif game_state == 'ended':
        # fill the screen a solid color
        screen.fill('black')

        # create the game over heading
        heading_render = large_font.render('Game Over', 1, 'white')
        heading_rect = heading_render.get_rect(center=(window_width / 2, window_height / 2))

        # create the random fact text
        body_render = small_font.render(game_over_fact, 1, 'white')
        body_rect = body_render.get_rect(center=(window_width / 2, window_height / 2 + large_text_size + 40))

        restart_render = small_font.render('[press space to restart]', 1, 'white')
        restart_rect = body_rect.copy()
        restart_rect.y += 20

        # draw the game over screen
        screen.blit(heading_render, heading_rect)
        screen.blit(body_render, body_rect)
        screen.blit(restart_render, restart_rect)

        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                asteroids = create_asteroid_list()
                starship = Starship(400, 300)
                projectiles = []
                game_state = 'running'

    pygame.display.flip()
    clock.tick(FPS)
