import pygame
import pygame_widgets
from pygame_widgets.button import Button
from pygame import mixer
import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

pygame.init()
mixer.init()
mixer.music.load(resource_path("БатяПлюшкин.mp3"))
mixer.music.set_volume(0.05)
mixer.music.play(-1)

width = 500
height = 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Игра про кликер')

score = 0
font = pygame.font.Font(None, 42)

def score_click():
    global score
    score += 1
    print(score)

button = Button(
    screen,
    175, 175, 150, 150,
    text='Click',
    fontSize=50,
    margin=20,
    inactiveColour=(34, 252, 0),
    hoverColour=(18, 115, 3),
    pressedColour=(255, 15, 31),
    radius=360,
    onClick=score_click
)

done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    screen.fill((255, 255, 255))

    pygame_widgets.update(event)
    textsurface = font.render(f'Счет: {score}', True, (0, 0, 0))
    screen.blit(textsurface, (200, 125))
    pygame.display.flip()

pygame.quit()