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

#Функция для корректной загрузки файлов при сборке в .exe
#Нужна чтобы игра работала и как скрипт .py и как собранный .exe
def resource_path(relative_path):
    try:
        #Если запущено из собранного .exe файла, берем временную папку
        base_path = sys._MEIPASS
    except Exception:
        #Если запущено из скрипта .py, берем текущую папку
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

#Запуск pygame и музыкального проигрывателя
pygame.init()
mixer.init()

#Загрузка и воспроизведение фоновой музыки
mixer.music.load(resource_path("БатяПлюшкин.mp3"))
mixer.music.set_volume(0.05)  #Громкость от 0 до 1, 0.05 = 5%
mixer.music.play(-1)  #(-1) означает бесконечное повторение

#Загрузка звуков
click_sound = mixer.Sound(resource_path("click.mp3"))
click_sound.set_volume(0.3)  #Громкость 30%

buy_sound = mixer.Sound(resource_path("click.mp3"))
buy_sound.set_volume(0.3)

#Размеры окна игры (ширина 500, высота 500 пикселей)
width = 500
height = 500

#Создание главного окна
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Игра про кликер')  #Название окна

#Игровые переменные
score = 0  #Текущий счет игрока, увеличивается при кликах
multiplier = 1  #Множитель клика, сколько очков дается за 1 клик
auto_clicker = False  #Флаг: куплен ли автокликер
auto_clicker_running = True  #Флаг для остановки потока автокликера при выходе
font = pygame.font.Font(None, 42)  #Шрифт для текста (None=стандартный, 42=размер)
SAVE_FILE = "save_data.json"  #Имя файла для сохранения прогресса
LOG_FILE = "game_log.txt"  #Имя файла для логов (запись действий)

#Достижения (unlocked = True когда достигнуто)
ach1 = False  #100 кликов
ach2 = False  #1000 кликов
ach3 = False  #10000 кликов

#Функция записи действий в лог-файл
#Каждое действие записывается с точным временем
def write_log(message):
    #"a" режим - добавляем в конец файла, не перезаписывая
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        #Получаем текущее время в формате Год-Месяц-День Часы:Минуты:Секунды
        time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{time_now}] {message}\n")

#Функция изменения громкости музыки
#val - значение от ползунка (0-100)
def change_volume(val):
    #Делим на 100 чтобы получить значение от 0 до 1
    mixer.music.set_volume(int(val) / 100)

#Функция открытия окна настроек
def open_settings():
    write_log("Открыты настройки")
    #Создаем новое окно через tkinter
    volumesett_window = tk.Tk()
    volumesett_window.title("Настройка громкости")
    volumesett_window.geometry("300x200")
    
    #Ползунок громкости от 0 до 100, горизонтальный
    scale = tk.Scale(volumesett_window, from_=0, to=100, orient=tk.HORIZONTAL, command=change_volume)
    scale.pack()  #Размещаем ползунок в окне
    
    volumesett_window.mainloop()  #Показываем окно (код застывает до закрытия)

#Функция открытия окна достижений
def open_achievements():
    global ach1, ach2, ach3
    achievements_window = tk.Tk()
    achievements_window.title("Достижения")
    achievements_window.geometry("300x250")
    
    #Заголовок окна
    tk.Label(achievements_window, text="ДОСТИЖЕНИЯ", font=("Arial", 16)).pack(pady=10)
    
    #Отображаем каждое достижение с галочкой ✅ или крестиком ❌
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
    
    #Показываем текущий счет игрока
    tk.Label(achievements_window, text=f"\nКликов: {score}").pack()
    
    achievements_window.mainloop()

#Функция открытия окна магазина
def open_shop():
    global multiplier, auto_clicker, score
    
    shop_window = tk.Tk()
    shop_window.title("Магазин")
    shop_window.geometry("350x350")
    
    tk.Label(shop_window, text="МАГАЗИН", font=("Arial", 16, "bold")).pack(pady=10)
    
    #Покупка 1: Улучшение клика
    def buy_multiplier():
        global score, multiplier
        cost = 50
        if score >= cost:
            score -= cost
            multiplier += 1
            buy_sound.play()  # ЗВУК ПОКУПКИ
            write_log(f"Куплено улучшение клика! Множитель: {multiplier}")
            update_labels()  #Обновляем информацию в окне
            print(f"Множитель +1! Теперь: {multiplier}")
        else:
            tk.messagebox.showwarning("Не хватает", f"Нужно {cost} кликов!")
    
    #Рамка с информацией о товаре
    frame1 = tk.Frame(shop_window)
    frame1.pack(pady=10)
    tk.Label(frame1, text=f"Улучшение клика +1", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
    tk.Label(frame1, text=f"Цена: 50", fg="green", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
    tk.Button(frame1, text="Купить", command=buy_multiplier).pack(side=tk.LEFT, padx=5)
    
    #Покупка 2: Автокликер
    def buy_auto_clicker():
        global score, auto_clicker
        cost = 200  #Стоимость автокликера
        if not auto_clicker and score >= cost:  #Проверяем не куплен ли уже и хватает ли кликов
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
    
    #Информация о текущих улучшениях
    info_frame = tk.Frame(shop_window)
    info_frame.pack(pady=20)
    tk.Label(info_frame, text="Ваши улучшения:", font=("Arial", 12, "bold")).pack()
    tk.Label(info_frame, text=f"Множитель клика: x{multiplier}", font=("Arial", 10)).pack()
    tk.Label(info_frame, text=f"Автокликер: {'Куплен' if auto_clicker else 'Не куплен'}", font=("Arial", 10)).pack()
    tk.Label(info_frame, text=f"Кликов: {score}", font=("Arial", 10)).pack()
    
    #Функция обновления информации после покупки
    #Удаляет старые надписи и создает новые с обновленными данными
    def update_labels():
        for widget in info_frame.winfo_children():  #Удаляем все старые виджеты
            widget.destroy()
        #Создаем новые с актуальными данными
        tk.Label(info_frame, text="Ваши улучшения:", font=("Arial", 12, "bold")).pack()
        tk.Label(info_frame, text=f"Множитель клика: x{multiplier}", font=("Arial", 10)).pack()
        tk.Label(info_frame, text=f"Автокликер: {'Куплен' if auto_clicker else 'Не куплен'}", font=("Arial", 10)).pack()
        tk.Label(info_frame, text=f"Кликов: {score}", font=("Arial", 10)).pack()
    
    shop_window.mainloop()

#Функция работы автокликера в отдельном потоке
#Поток нужен чтобы автокликер работал параллельно с основным циклом игры
def auto_clicker_loop():
    global score
    while auto_clicker_running:  #Работает пока игра открыта
        if auto_clicker:  #Если автокликер куплен
            time.sleep(1)  #Ждем 1 секунду
            score += 1  #Добавляем 1 клик
            write_log(f"Автокликер! Счет стал: {score}")
            print(f"Автокликер: +1, всего: {score}")
        else:
            time.sleep(1)  #Если не куплен, просто ждем и проверяем снова

#Запускаем поток для автокликера
auto_clicker_thread = threading.Thread(target=auto_clicker_loop, daemon=True)
auto_clicker_thread.start()
    
#Функция клика по главной кнопке
def score_click():
    global score, ach1, ach2, ach3, multiplier
    score += multiplier  #Добавляем множитель к счету (обычно +1, но может быть больше)
    click_sound.play()  #Звук клика
    
    #Проверка достижений (каждое разблокируется один раз)
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

#Функция сохранения игры в файл
def save_game_to_file():
    #Собираем все данные в словарь
    data = {"score": score, "ach1": ach1, "ach2": ach2, "ach3": ach3, "multiplier": multiplier, "auto_clicker": auto_clicker}
    with open(SAVE_FILE, "w") as f:  #"w" режим - перезаписываем файл
        json.dump(data, f)  #Сохраняем в JSON формате
    write_log(f"Игра сохранена. Счет: {score}")

#Функция загрузки игры из файла
def load_game():
    global score, ach1, ach2, ach3, multiplier, auto_clicker
    try:
        with open(SAVE_FILE, "r") as f:  #"r" режим - читаем файл
            data = json.load(f)  #Загружаем данные из JSON
        #Восстанавливаем все переменные из сохранения
        score = data["score"]
        ach1 = data.get("ach1", False)  #.get с значением по умолчанию, если ключа нет
        ach2 = data.get("ach2", False)
        ach3 = data.get("ach3", False)
        multiplier = data.get("multiplier", 1)
        auto_clicker = data.get("auto_clicker", False)
        write_log(f"Загружена игра. Счет: {score}, Множитель: {multiplier}, Автокликер: {auto_clicker}")
        print(f"Игра загружена! Счет: {score}")
    except:
        #Если файла нет или он поврежден
        write_log("Ошибка: файл сохранения не найден")
        print("Сохранение не найдено")

#Функция новой игры (сброс прогресса)
def new_game():
    global score, ach1, ach2, ach3, multiplier, auto_clicker
    score = 0  #Обнуляем счет
    ach1 = False  #Сбрасываем достижения
    ach2 = False
    ach3 = False
    multiplier = 1  #Сбрасываем множитель
    auto_clicker = False  #Отключаем автокликер
    if os.path.exists(SAVE_FILE):  #Если файл сохранения существует
        os.remove(SAVE_FILE)  #Удаляем его
    write_log("Начата новая игра. Счет сброшен")
    print("Новая игра! Счет сброшен")

#Запись запуска игры в лог
write_log("ИГРА ЗАПУЩЕНА")

#КНОПКА "НАСТРОЙКИ"
#Координаты: x=10 (от левого края), y=10 (от верха), ширина=120, высота=40
button2 = Button(
    screen,
    10, 10, 120, 40,
    text='Настройки',
    fontSize=25,
    margin=20,
    inactiveColour=(255, 255, 255),  #Белый цвет (нормальное состояние)
    hoverColour=(227, 227, 227),     #Светло-серый (когда мышь на кнопке)
    pressedColour=(255, 15, 31),     #Красный (когда нажата)
    radius=5,  #Скругление углов
    onClick=open_settings  #Что делать при нажатии
)

#КНОПКА "ДОСТИЖЕНИЯ"
#y=60 (на 50 пикселей ниже первой кнопки)
button3 = Button(
    screen,
    10, 60, 120, 40,
    text='Достижения',
    fontSize=22,
    margin=20,
    inactiveColour=(5, 13, 255),    #Синий цвет
    hoverColour=(13, 11, 127),      #Темно-синий при наведении
    pressedColour=(255, 15, 31),    #Красный при нажатии
    radius=5,
    onClick=open_achievements
)

#КНОПКА "МАГАЗИН"
#y=110 (еще ниже)
button4 = Button(
    screen,
    10, 110, 120, 40,
    text='Магазин',
    fontSize=25,
    margin=20,
    inactiveColour=(255, 5, 5),     #Красный цвет
    hoverColour=(125, 11, 11),      #Темно-красный при наведении
    pressedColour=(255, 15, 31),    #Красный при нажатии
    radius=5,
    onClick=open_shop
)

#КНОПКА "ЗАГРУЗИТЬ ИГРУ"
#width - 130 = 370, чтобы кнопка не вылезала за правый край
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

#КНОПКА "НОВАЯ ИГРА"
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

#КНОПКА "СОХРАНИТЬ"
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

#ГЛАВНАЯ КНОПКА "CLICK"
#x=175, y=175 (центр окна 500x500, потому что 175 + 150/2 = 250)
#radius=360 делает кнопку круглой (больше половины ширины)
button = Button(
    screen,
    175, 175, 150, 150,
    text='Click',
    fontSize=50,
    margin=20,
    inactiveColour=(34, 252, 0),    #Ярко-зеленый
    hoverColour=(18, 115, 3),       #Темно-зеленый при наведении
    pressedColour=(255, 15, 31),
    radius=360,
    onClick=score_click
)

#ГЛАВНЫЙ ИГРОВОЙ ЦИКЛ
#Работает пока done = False, закрывается когда done = True
done = False
while not done:
    #Обработка событий (нажатия клавиш, мыши, закрытие окна)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  #Если нажали крестик закрытия окна
            auto_clicker_running = False  #Останавливаем поток автокликера
            write_log("Игра закрыта")
            done = True  #Выходим из цикла

        pygame_widgets.update(event)  #Обновляем состояние кнопок
    
    #Заливка фона голубым цветом (RGB: 136,230,242)
    screen.fill((136, 230, 242))

    #Рисуем все кнопки на экране
    button.draw()
    button2.draw()
    button3.draw()
    button4.draw()
    button5.draw()
    button6.draw()
    button7.draw()
    
    #Создаем и рисуем текст счета (координаты x=200, y=10)
    textsurface = font.render(f'Счет: {score}', True, (0, 0, 0))  #Черный цвет
    screen.blit(textsurface, (200, 10))
    
    #Текст с множителем (x=145, y=60)
    multisurface = font.render(f'Множитель: x{multiplier}', True, (0, 0, 0))
    screen.blit(multisurface, (145, 60))
    
    #Текст с автокликером (x=138, y=110)
    autosurface = font.render(f'Автокликер: {"Да" if auto_clicker else "Нет"}', True, (0, 0, 0))
    screen.blit(autosurface, (138, 110))
    
    #Обновляем экран (показываем всё что нарисовали)
    pygame.display.flip()

#Закрытие игры
pygame.quit()
