import pygame
import tkinter as tk
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

def open_settings():
    settings_window = tk.Tk()
    settings_window.title("Настройки")
    settings_window.geometry("300x200")
    settings_window.mainloop()

def open_achievements():
    achievements_window = tk.Tk()
    achievements_window.title("Достижения")
    achievements_window.geometry("300x200")
    achievements_window.mainloop()

def open_shop():
    shop_window = tk.Tk()
    shop_window.title("Магазин")
    shop_window.geometry("300x200")
    shop_window.mainloop()
    
def score_click():
    global score
    score += 1
    print(score)

button2 = Button(
    screen,
    10, 10, 120, 40,
    text='Настройки',
    fontSize=25,
    margin=20,
    inactiveColour=(115, 115, 115),
    hoverColour=(66, 66, 66),
    pressedColour=(255, 15, 31),
    radius=5,
    onClick=open_settings  # исправлено
)

button3 = Button(
    screen,
    10, 60, 120, 40,
    text='Достижения',
    fontSize=22,
    margin=20,
    inactiveColour=(115, 115, 115),
    hoverColour=(66, 66, 66),
    pressedColour=(255, 15, 31),
    radius=5,
    onClick=open_achievements  # исправлено
)

button4 = Button(
    screen,
    10, 110, 120, 40,
    text='Магазин',
    fontSize=25,
    margin=20,
    inactiveColour=(115, 115, 115),
    hoverColour=(66, 66, 66),
    pressedColour=(255, 15, 31),
    radius=5,
    onClick=open_shop  # исправлено
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
    
    pygame.display.flip()

pygame.quit()