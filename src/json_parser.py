import json
from pathlib import Path
import os
from src.config import *


def get_launcher_directory():
    roaming = os.getenv('APPDATA')

    launcher_path = Path(roaming) / ".raylauncher" / "launcher" / "data"
    launcher_path.mkdir(parents=True, exist_ok=True)

    return launcher_path


def update_missing_keys(target_dict, default_dict):
    is_updated = False

    for key, val in default_dict.items():
        if key not in target_dict:
            target_dict[key] = val
            is_updated = True
        elif isinstance(val, dict) and isinstance(target_dict[key], dict):
            if update_missing_keys(target_dict[key], val):
                is_updated = True

    return is_updated


def dump_data(data, filename):
    file_path = get_launcher_directory() / f'{filename}.json'
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def load_data(filename):
    if filename == 'settings':
        default_structure = DEFAULT_SETTINGS
    elif filename == 'config':
        default_structure = DEFAULT_CONFIG
    else:
        default_structure = {}

    file_path = get_launcher_directory() / f'{filename}.json'

    if not file_path.exists():
        if default_structure:
            dump_data(default_structure, filename)
        return default_structure

    with open(file_path, 'r', encoding='utf-8') as f:
        user_data = json.load(f)

    if default_structure and isinstance(user_data, dict):
        if update_missing_keys(user_data, default_structure):
            dump_data(user_data, filename)

    return user_data


def get_minecraft_directory():
    return load_data('settings')["minecraft"]["path"]


data = load_data('settings')
config = load_data('config')
