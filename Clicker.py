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
settings = pygame.display.set_mode((width, height))
achievements = pygame.display.set_mode((width, height))
shop = pygame.display.set_mode((width, height))
pygame.display.set_caption('Игра про кликер')

score = 0
font = pygame.font.Font(None, 42)

settings_open = False
achievements_open = False
shop_open = False

def opensett():
    global settings_open
    settings_open = True
    print("Настройки открыты")

def openachiev():
    global achievements_open
    achievements_open = True
    print("Достижения открыты")

def openshop():
    global shop_open
    shop_open = True
    print("Магазин открыт")
    
def score_click():
    global score
    score += 1
    print(score)

button2 = Button(
    settings,
    10, 10, 120, 40,
    text='Настройки',
    fontSize=25,
    margin=20,
    inactiveColour=(115, 115, 115),
    hoverColour=(66, 66, 66),
    pressedColour=(255, 15, 31),
    radius=5,
    onClick=opensett
)

button3 = Button(
    achievements,
    10, 60, 120, 40,
    text='Достижения',
    fontSize=22,
    margin=20,
    inactiveColour=(115, 115, 115),
    hoverColour=(66, 66, 66),
    pressedColour=(255, 15, 31),
    radius=5,
    onClick=openachiev
)

button4 = Button(
    shop,
    10, 110, 120, 40,
    text='Магазин',
    fontSize=25,
    margin=20,
    inactiveColour=(115, 115, 115),
    hoverColour=(66, 66, 66),
    pressedColour=(255, 15, 31),
    radius=5,
    onClick=openshop
)

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

        pygame_widgets.update(event)
    
    screen.fill((255, 255, 255))

    button.draw()
    button2.draw()
    button3.draw()
    button4.draw()
    
    textsurface = font.render(f'Счет: {score}', True, (0, 0, 0))
    screen.blit(textsurface, (200, 125))
    
    if settings_open:
        pygame.draw.rect(settings, (255, 255, 255), (100, 100, 300, 300))
        pygame.draw.rect(settings, (0, 0, 0), (100, 100, 300, 300), 3)
        set_text = font.render('Настройки', True, (0, 0, 0))
        settings.blit(set_text, (200, 220))
    
    if achievements_open:
        pygame.draw.rect(achievements, (255, 255, 255), (100, 100, 300, 300))
        pygame.draw.rect(achievements, (0, 0, 0), (100, 100, 300, 300), 3)
        ach_text = font.render('Достижения', True, (0, 0, 0))
        achievements.blit(ach_text, (180, 220))
    
    if shop_open:
        pygame.draw.rect(shop, (255, 255, 255), (100, 100, 300, 300))
        pygame.draw.rect(shop, (0, 0, 0), (100, 100, 300, 300), 3)
        shop_text = font.render('Магазин', True, (0, 0, 0))
        shop.blit(shop_text, (200, 220))
    
    pygame.display.flip()

pygame.quit()