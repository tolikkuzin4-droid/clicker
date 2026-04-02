import pygame
import tkinter as tk
import pygame_widgets
from pygame_widgets.button import Button
from pygame import mixer
import sys
import os
import json
from datetime import datetime

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

click_sound = mixer.Sound(resource_path("click.mp3"))
click_sound.set_volume(0.3)

width = 500
height = 500

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Игра про кликер')

score = 0
font = pygame.font.Font(None, 42)
SAVE_FILE = "save_data.json"
LOG_FILE = "game_log.txt"

def write_log(message):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{time_now}] {message}\n")

def change_volume(val):
    mixer.music.set_volume(int(val) / 100)

def open_settings():
    write_log("Открыты настройки")
    volumesett_window = tk.Tk()
    volumesett_window.title("Настройка громкости")
    volumesett_window.geometry("300x200")
    
    scale = tk.Scale(volumesett_window, from_=0, to=100, orient=tk.HORIZONTAL, command=change_volume)
    scale.pack()
    
    tk.Label(volumesett_window, text=f"{scale.get()}%").pack()
    volumesett_window.mainloop()

def open_achievements():
    write_log("Открыты достижения")
    achievements_window = tk.Tk()
    achievements_window.title("Достижения")
    achievements_window.geometry("300x200")
    achievements_window.mainloop()

def open_shop():
    write_log("Открыт магазин")
    shop_window = tk.Tk()
    shop_window.title("Магазин")
    shop_window.geometry("300x200")
    shop_window.mainloop()
    
def score_click():
    global score
    score += 1
    click_sound.play()
    write_log(f"Клик! Счет стал: {score}")
    print(score)

def save_game_to_file():
    data = {"score": score}
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)
    write_log(f"Игра сохранена. Счет: {score}")

def load_game():
    global score
    try:
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
        score = data["score"]
        write_log(f"Загружена игра. Счет: {score}")
        print(f"Игра загружена! Счет: {score}")
    except:
        write_log("Ошибка: файл сохранения не найден")
        print("Сохранение не найдено")

def new_game():
    global score
    score = 0
    if os.path.exists(SAVE_FILE):
        os.remove(SAVE_FILE)
    write_log("Начата новая игра. Счет сброшен")
    print("Новая игра! Счет сброшен")

write_log("ИГРА ЗАПУЩЕНА")

button2 = Button(
    screen,
    10, 10, 120, 40,
    text='Настройки',
    fontSize=25,
    margin=20,
    inactiveColour=(245, 245, 245),
    hoverColour=(16, 2, 176),
    pressedColour=(255, 15, 31),
    radius=5,
    onClick=open_settings
)

button3 = Button(
    screen,
    10, 60, 120, 40,
    text='Достижения',
    fontSize=22,
    margin=20,
    inactiveColour=(245, 245, 245),
    hoverColour=(16, 2, 176),
    pressedColour=(255, 15, 31),
    radius=5,
    onClick=open_achievements
)

button4 = Button(
    screen,
    10, 110, 120, 40,
    text='Магазин',
    fontSize=25,
    margin=20,
    inactiveColour=(245, 245, 245),
    hoverColour=(16, 2, 176),
    pressedColour=(255, 15, 31),
    radius=5,
    onClick=open_shop
)

button5 = Button(
    screen,
    width - 130, 10, 120, 40,
    text='Загрузить игру',
    fontSize=18,
    margin=20,
    inactiveColour=(245, 245, 245),
    hoverColour=(16, 2, 176),
    pressedColour=(255, 15, 31),
    radius=5,
    onClick=load_game
)

button6 = Button(
    screen,
    width - 130, 60, 120, 40,
    text='Новая игра',
    fontSize=20,
    margin=20,
    inactiveColour=(245, 245, 245),
    hoverColour=(16, 2, 176),
    pressedColour=(255, 15, 31),
    radius=5,
    onClick=new_game
)

button7 = Button(
    screen,
    width - 130, 110, 120, 40,
    text='Сохранить',
    fontSize=20,
    margin=20,
    inactiveColour=(245, 245, 245),
    hoverColour=(16, 2, 176),
    pressedColour=(255, 15, 31),
    radius=5,
    onClick=save_game_to_file
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
            write_log("Игра закрыта")
            done = True

        pygame_widgets.update(event)
    
    screen.fill((136, 230, 242))

    button.draw()
    button2.draw()
    button3.draw()
    button4.draw()
    button5.draw()
    button6.draw()
    button7.draw()
    
    textsurface = font.render(f'Счет: {score}', True, (0, 0, 0))
    screen.blit(textsurface, (200, 125))
    
    pygame.display.flip()

pygame.quit()