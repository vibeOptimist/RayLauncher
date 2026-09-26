import sys
import webbrowser
from pathlib import Path
from uuid import uuid1
import os

from psutil import virtual_memory
from minecraft_launcher_lib.utils import get_minecraft_directory

from src import json_parser as jp
from src.widgets import Message


def default_minecraft_directory():
    path = Path(get_minecraft_directory())
    return str(path.with_name('.raylauncher') / 'minecraft')


def version_info(version: str):
    """ Парсит строку в кортеж 'Forge 1.12.2 '-> ('1.12.2', 'forge') """
    if not version:
        return 'unknown', 'none'

    parts = version.split(maxsplit=1)

    if len(parts) == 1:
        return version, 'none'

    prefix, rest = parts[0], parts[1]

    prefixes = {
        'MP': (rest, 'MP'),
        'Версия': (rest, 'none'),
        'Снапшот': (rest, 'none'),
        'Beta': (f'b{rest}', 'none'),
        'Alpha': (f'a{rest}', 'none'),
        'Forge': (rest, 'forge'),
        'Fabric': (rest, 'fabric'),
        'Quilt': (rest, 'quilt'),
        'NeoForge': (rest, 'neoforge')
    }

    return prefixes.get(prefix, (version, 'none'))


def get_memory_total():
    return round(virtual_memory().total / (1024 ** 3))


def remove_logs():
    """ Автоочистка логов каждые 12 запусков лаунчера """
    data = jp.load_data('config')
    data['clean_step'] += 1
    jp.dump_data(data, 'config')

    if data['clean_step'] == 12:
        log_dir = Path("logs")
        if not log_dir.exists():
            return

        for item in log_dir.iterdir():
            if item.is_file():
                item.unlink()


def open_directory(mode):
    base_dir = Path(jp.get_minecraft_directory())

    directories = {
        'game': base_dir,
        'screenshots': base_dir / 'screenshots',
        'saves': base_dir / 'saves',
        'logs': Path(sys.argv[0]).parent / 'logs'
    }

    target = directories.get(mode)

    if not target or not target.is_dir():
        texts = {
            'game': "Папка игры не существует.",
            'screenshots': "Скриншоты ещё не были созданы.",
            'saves': "Игровые миры ещё не созданы.",
            'logs': "Папка логов отсутствует."
        }
        Message('crit', "Ошибка", "Каталог не найден", info=texts.get(mode, ""))
        return

    os.startfile(target)


def generate_random_uuid():
    return str(uuid1())


def check_nickname(name):
    username = name.strip()
    if not username:
        Message('warn', "Ошибка", "Никнейм не может быть пустым!")
        return None

    if ' ' in username:
        Message('warn', "Ошибка", "Никнейм не должен содержать пробелы!")
        return None

    if len(username) > 16:
        Message('warn', "Ошибка", "Максимальная длина никнейма - 16 символов!")
        return None

    return username


def open_site(url):
    webbrowser.open(url, new=1)


def play_in_browser(offline):
    if offline:
        html_path = Path('assets/resources/EaglercraftX_1.8_u53_Offline_Signed.html').resolve()
        open_site(html_path.as_uri())
    else:
        open_site('https://eaglercraft.com')
