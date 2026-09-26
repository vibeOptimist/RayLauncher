import random

from src.actions import get_memory_total
from src.game_versions import get_versions
from src import json_parser as jp
from src.config import *

# Тестирование
bottom_frame = False

# Игра и версии
game_no_installs = []
game_updates = []

game_versions = ('26.1', '1.21.11', '1.21.10', '1.21.9', '1.21.8', '1.21.7', '1.21.6', '1.21.5',
                 '1.21.4', '1.21.3', '1.21.2', '1.21.1', '1.21', '1.20.6', '1.20.5', '1.20.4',
                 '1.20.3', '1.20.2', '1.20.1', '1.20', '1.19.4', '1.19.3', '1.19.2', '1.19.1',
                 '1.19', '1.18.2', '1.18.1', '1.18', '1.17.1', '1.17', '1.16.5', '1.16.4', '1.16.3',
                 '1.16.2', '1.16.1', '1.16', '1.15.2', '1.15.1', '1.15', '1.14.4', '1.14.3',
                 '1.14.2', '1.14.1', '1.14', '1.13.2', '1.13.1', '1.13', '1.12.2', '1.12.1',
                 '1.12', '1.11.2', '1.11.1', '1.11', '1.10.2', '1.10.1', '1.10', '1.9.4', '1.9.3',
                 '1.9.2', '1.9.1', '1.9', '1.8.9', '1.8.8', '1.8.7', '1.8.6', '1.8.5', '1.8.4',
                 '1.8.3', '1.8.2', '1.8.1', '1.8', '1.7.10', '1.7.9', '1.7.8', '1.7.7', '1.7.6',
                 '1.7.5', '1.7.4', '1.7.2', '1.6.4', '1.6.2', '1.6.1', '1.5.2', '1.5.1', '1.4.7',
                 '1.4.6', '1.4.5', '1.4.4', '1.4.2', '1.3.2', '1.3.1', '1.2.5', '1.2.4', '1.2.3',
                 '1.2.2', '1.2.1', '1.1', '1.0')

game_versions_type = {'Ванильные': 'vanilla', 'Снапшоты': 'snapshots', 'Forge': 'forge',
                      'Fabric': 'fabric', 'Quilt': 'quilt', 'NeoForge': 'neoforge'}

game_launch_type = 'play'
game_parameters = {"user": '', "uuid": '', "server": '', "port": ''}

g_version = ''
g_modloader = ''

# Информация о лаунчере
version = '0.2.2'

about = """
RayLauncher — это стильный, быстрый и 
бесплатный Minecraft-лаунчер.

В лаунчере есть множество инструментов, 
улучшающих ваш игровой процесс. Стильный 
дизайн создаёт атмосферу свободы и лёгкости, 
делая использование лаунчера приятным.

RayLauncher — молодой проект, который 
развивается и получает обновления. Следите 
за новостями и будьте внимательны.

Желаю всем счастливой игры!
"""

# Значения
network = False
data_loading_try = False
mod = False

servers_icons = {"Земля": 1, "Руда": 2, "Крипер": 3, "Эндермен": 4}
side_tabs = {'home': 0, 'settings': 1, 'servers': 2, 'content': 3, 'about': 4, 'console': 5}
mods = {'tip': 'mod', 'loader': 'forge', 'version': '1.12.2'}

mrpack_path = ''
mrpack_name = ''

# Вкладки
tabs_list = {
    'home': "Главная",
    'settings': "Настройки",
    'about': "О лаунчере",
    'servers': "Сервера",
    'content': "Контент",
    'accounts': "Выбор аккаунта",
    'web_play': "Играть в браузере",
    'versions': "Выбор версии",
    'console': "Консоль",
    'socials': "Соцсети"
}

tabs_index = {name: i for i, name in enumerate(tabs_list)}

tab_list = ['home']
tab_now = 0
tab_start_now = 0


# Стили
def load_stylesheet(name):
    with open(f"assets/styles/{name}.qss", encoding="utf-8") as file:
        if bottom_frame:
            return file.read() + ' \nQStackedWidget {background: rgba(30, 40, 90, 100)}'
        return file.read()


stylesheet_start = load_stylesheet("start")
stylesheet_dark = load_stylesheet("dark")
stylesheet_light = load_stylesheet("light")

style_side = """
#side {background: #262A3B}
#side:hover {background: #33394F}
#side:pressed {background: #404866}
"""

style_side_active = """
#side {background: #377ca3}
#side:hover {background: #399bc4}
#side:pressed {background: #399bc4}
"""

style_settings = """
#set-button {background: rgba(64, 65, 70, 96); color: #d7d7d7}
#set-button:hover {background: rgba(80, 82, 88, 134); color: #e5e5e5}
#set-button:pressed {background: rgba(94, 96, 102, 160); color: #f7f7f7}
"""

style_settings_active = """
#set-button {background: rgba(90, 135, 166, 168); color: #4fd2f0}
#set-button:hover {background: rgba(98, 142, 171, 188); color: #53c4f5}
#set-button:pressed {background: rgba(106, 142, 176, 209); color: #59c2ff}
"""

style_tab_active = '#start-label {color: #ebebeb}'


def make_social_style(hover_bg, hover_border, press_bg, press_border):
    return f"""
    #cbutton:hover {{background: {hover_bg}; border-color: {hover_border}}}
    #cbutton:pressed {{background: {press_bg}; border-color: {press_border}}}
    """


social_styles = [make_social_style(*colors) for colors in SOCIAL_COLORS]

# Тексты
start_text = (("Надёжный", "Бесплатный безопасный \nлаунчер без вирусов."),
              ("Быстрый", "Потребляет мало памяти и \nхорошо оптимизирован."),
              ("Стильный", "Красивый и удобный дизайн \nдаст вам комфорт."),
              ("Гибкий", "Настрой лаунчер под себя, \nон в твоих руках."))

start_text_java = """
Лаунчер автоматически устанавливает
требуемую Java для Minecraft. Но вы 
можете выбрать свою.
"""

start_text_minecraft = """
Укажите папку для хранения игры и
игровых данных: скриншоты, миры, 
модификации и т.д.
"""

start_text_account = """
Введите никнейм, он должен содержать 
только английские буквы, цифры
и знаки подчёркивания (_).
"""

text_web1 = """
Наслаждайтесь игрой Minecraft прямо в 
браузере, благодаря проекту EaglerCraft.
Он предоставляет полную версию 
Minecraft 1.8.8 и имеет поддержку одиночной
и многопользовательской игры, включая 
собственный сервер для игры с друзьями. 
Сам проект совершенно бесплатный.
"""

text_web2 = """
Eaglercraft создан энтузиастом lax1dude на 
базе инструмента TeaVM, который позволяет 
компилировать исходный Java-код игры в 
JavaScript, понятный любому браузеру. 
Благодаря использованию специальных 
веб-библиотек, масштабная работа по 
портированию заняла почти год.
"""

text_accounts = """
Данное меню позволяет управлять вашими 
аккаунтами.

- Введите никнейм в поле ввода, он может
содержать только английские буквы, цифры
и знаки подчёркивания (_).

- Нажмите "+" для создания нового аккаунта.

- Кнопка со значком корзинки удалит 
выбранный аккаунт в списке.

- Для возвращения на главную нажмите 
"Вернуться обратно".
"""

text_modpacks = """Сборки (Модпаки) - это готовые наборы модификаций для игры. Их устанавливают
через файлы .mrpack, содержащие инструкции по установке и связыванию модов.
RayLauncher позволяет установить сборку в несколько кликов."""

# Оперативная память
total_mem = min(get_memory_total(), 8)
memory_uses = tuple(f"{i} ГБ" for i in range(1, total_mem + 1))

if jp.data["minecraft"]["memory"] > total_mem:
    jp.data["minecraft"]["memory"] = 1
memory_count = jp.data["minecraft"]["memory"] - 1

# Данные
users = jp.load_data('users')
data_users = list(users.keys())
index_user = data_users.index(jp.config["user"]) if jp.config["user"] in data_users else 0

config = jp.config
index_version = 0

versions_get = get_versions()
if config["version"] in versions_get:
    for i in range(len(versions_get)):
        if versions_get[i] == config["version"]:
            index_version = i

animation = jp.data["design"]["animation"]
button_web = jp.data["design"]["button_web_play"]
button_black = jp.data["parameters"]["button_black"]
demo = jp.data["minecraft"]["demo"]
network_check = jp.data["parameters"]["network_check"]
incognito = jp.data["parameters"]["incognito"]

# Задние фоны
list_arts = ('Случайный', 'Свой фон')
list_backgrounds = ('Берёзы', 'Оазис', 'Сакуры', 'Таверна', 'Ночь', 'Океан', 'Тайга', 'Свой фон')

img1, img_path1 = jp.data["design"]["loading"]
img2, img_path2 = jp.data["design"]["launcher"]

ai = random.randint(1, 7)
g_start, g_end = GRADIENTS[ai - 1] if 1 <= ai <= 7 else GRADIENTS[7]

style_bar = (f"#start-progressbar::chunk {{background-color: QLinearGradient(x1: 0, y1: 0, x2: 1, "
             f"y2: 0, stop: 0 {g_start}, stop: 1 {g_end} )}}")
