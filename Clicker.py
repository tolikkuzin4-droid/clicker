import pygame
import tkinter as tk
import pygame_widgets
from pygame_widgets.button import Button
from pygame import mixer
import sys
import os
import json
from datetime import datetime
import threading
import time

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

buy_sound = mixer.Sound(resource_path("click.mp3"))  # Звук покупки (такой же)
buy_sound.set_volume(0.3)  # Такая же громкость

width = 500
height = 500

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Игра про кликер')

score = 0
multiplier = 1
auto_clicker = False
auto_clicker_running = True
font = pygame.font.Font(None, 42)
SAVE_FILE = "save_data.json"
LOG_FILE = "game_log.txt"

ach1 = False
ach2 = False
ach3 = False

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
    
    volumesett_window.mainloop()

def open_achievements():
    global ach1, ach2, ach3
    achievements_window = tk.Tk()
    achievements_window.title("Достижения")
    achievements_window.geometry("300x250")
    
    tk.Label(achievements_window, text="ДОСТИЖЕНИЯ", font=("Arial", 16)).pack(pady=10)
    
    if ach1:
        tk.Label(achievements_window, text="✅ 100 кликов").pack()
    else:
        tk.Label(achievements_window, text="❌ 100 кликов").pack()
    
    if ach2:
        tk.Label(achievements_window, text="✅ 1000 кликов").pack()
    else:
        tk.Label(achievements_window, text="❌ 1000 кликов").pack()
    
    if ach3:
        tk.Label(achievements_window, text="✅ 10000 кликов").pack()
    else:
        tk.Label(achievements_window, text="❌ 10000 кликов").pack()
    
    tk.Label(achievements_window, text=f"\nКликов: {score}").pack()
    
    achievements_window.mainloop()

def open_shop():
    global multiplier, auto_clicker, score
    
    shop_window = tk.Tk()
    shop_window.title("Магазин")
    shop_window.geometry("350x350")
    
    tk.Label(shop_window, text="МАГАЗИН", font=("Arial", 16, "bold")).pack(pady=10)
    
    # Покупка 1: Улучшение клика
    def buy_multiplier():
        global score, multiplier
        cost = 50
        if score >= cost:
            score -= cost
            multiplier += 1
            buy_sound.play()  # ЗВУК ПОКУПКИ
            write_log(f"Куплено улучшение клика! Множитель: {multiplier}")
            update_labels()
            print(f"Множитель +1! Теперь: {multiplier}")
        else:
            tk.messagebox.showwarning("Не хватает", f"Нужно {cost} кликов!")
    
    frame1 = tk.Frame(shop_window)
    frame1.pack(pady=10)
    tk.Label(frame1, text=f"Улучшение клика +1", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
    tk.Label(frame1, text=f"Цена: 50", fg="green", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
    tk.Button(frame1, text="Купить", command=buy_multiplier).pack(side=tk.LEFT, padx=5)
    
    # Покупка 2: Автокликер
    def buy_auto_clicker():
        global score, auto_clicker
        cost = 200
        if not auto_clicker and score >= cost:
            score -= cost
            auto_clicker = True
            buy_sound.play()  # ЗВУК ПОКУПКИ
            write_log("Куплен автокликер!")
            update_labels()
            print("Автокликер куплен!")
        elif auto_clicker:
            tk.messagebox.showinfo("Уже есть", "Автокликер уже куплен!")
        else:
            tk.messagebox.showwarning("Не хватает", f"Нужно {cost} кликов!")
    
    frame2 = tk.Frame(shop_window)
    frame2.pack(pady=10)
    tk.Label(frame2, text="Автокликер (1 клик/сек)", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
    tk.Label(frame2, text=f"Цена: 200", fg="green", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
    tk.Button(frame2, text="Купить", command=buy_auto_clicker).pack(side=tk.LEFT, padx=5)
    
    # Информация о текущих улучшениях
    info_frame = tk.Frame(shop_window)
    info_frame.pack(pady=20)
    tk.Label(info_frame, text="Ваши улучшения:", font=("Arial", 12, "bold")).pack()
    tk.Label(info_frame, text=f"Множитель клика: x{multiplier}", font=("Arial", 10)).pack()
    tk.Label(info_frame, text=f"Автокликер: {'Куплен' if auto_clicker else 'Не куплен'}", font=("Arial", 10)).pack()
    tk.Label(info_frame, text=f"Кликов: {score}", font=("Arial", 10)).pack()
    
    def update_labels():
        for widget in info_frame.winfo_children():
            widget.destroy()
        tk.Label(info_frame, text="Ваши улучшения:", font=("Arial", 12, "bold")).pack()
        tk.Label(info_frame, text=f"Множитель клика: x{multiplier}", font=("Arial", 10)).pack()
        tk.Label(info_frame, text=f"Автокликер: {'Куплен' if auto_clicker else 'Не куплен'}", font=("Arial", 10)).pack()
        tk.Label(info_frame, text=f"Кликов: {score}", font=("Arial", 10)).pack()
    
    shop_window.mainloop()

def auto_clicker_loop():
    global score
    while auto_clicker_running:
        if auto_clicker:
            time.sleep(1)
            score += 1
            write_log(f"Автокликер! Счет стал: {score}")
            print(f"Автокликер: +1, всего: {score}")
        else:
            time.sleep(1)

# Запускаем поток для автокликера
auto_clicker_thread = threading.Thread(target=auto_clicker_loop, daemon=True)
auto_clicker_thread.start()
    
def score_click():
    global score, ach1, ach2, ach3, multiplier
    score += multiplier
    click_sound.play()
    
    if score >= 100 and not ach1:
        ach1 = True
        write_log("Достижение: 100 кликов!")
        print("100 кликов!")
    
    if score >= 1000 and not ach2:
        ach2 = True
        write_log("Достижение: 1000 кликов!")
        print("1000 кликов!")
    
    if score >= 10000 and not ach3:
        ach3 = True
        write_log("Достижение: 10000 кликов!")
        print("10000 кликов!")
    
    write_log(f"Клик! +{multiplier} Счет стал: {score}")
    print(score)

def save_game_to_file():
    data = {"score": score, "ach1": ach1, "ach2": ach2, "ach3": ach3, "multiplier": multiplier, "auto_clicker": auto_clicker}
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)
    write_log(f"Игра сохранена. Счет: {score}")

def load_game():
    global score, ach1, ach2, ach3, multiplier, auto_clicker
    try:
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
        score = data["score"]
        ach1 = data.get("ach1", False)
        ach2 = data.get("ach2", False)
        ach3 = data.get("ach3", False)
        multiplier = data.get("multiplier", 1)
        auto_clicker = data.get("auto_clicker", False)
        write_log(f"Загружена игра. Счет: {score}, Множитель: {multiplier}, Автокликер: {auto_clicker}")
        print(f"Игра загружена! Счет: {score}")
    except:
        write_log("Ошибка: файл сохранения не найден")
        print("Сохранение не найдено")

def new_game():
    global score, ach1, ach2, ach3, multiplier, auto_clicker
    score = 0
    ach1 = False
    ach2 = False
    ach3 = False
    multiplier = 1
    auto_clicker = False
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
    inactiveColour=(255, 255, 255),
    hoverColour=(227, 227, 227),
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
    inactiveColour=(5, 13, 255),
    hoverColour=(13, 11, 127),
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
    inactiveColour=(255, 5, 5),
    hoverColour=(125, 11, 11),
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
    inactiveColour=(255, 255, 255),
    hoverColour=(227, 227, 227),
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
    inactiveColour=(5, 13, 255),
    hoverColour=(13, 11, 127),
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
    inactiveColour=(255, 5, 5),
    hoverColour=(125, 11, 11),
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
            auto_clicker_running = False
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
    screen.blit(textsurface, (200, 10))
    
    multisurface = font.render(f'Множитель: x{multiplier}', True, (0, 0, 0))
    screen.blit(multisurface, (145, 60))
    
    autosurface = font.render(f'Автокликер: {"Да" if auto_clicker else "Нет"}', True, (0, 0, 0))
    screen.blit(autosurface, (138, 110))
    
    pygame.display.flip()

pygame.quit()