from functools import lru_cache
from minecraft_launcher_lib import mod_loader
from minecraft_launcher_lib.utils import get_installed_versions, get_version_list

from src.json_parser import load_data, get_minecraft_directory
from src import values as v


@lru_cache(maxsize=1)
def get_cached_version_list():
    try:
        return get_version_list()
    except:
        return []


@lru_cache(maxsize=3)
def get_cached_loader_versions(name):
    try:
        vers = mod_loader.get_mod_loader(name).get_minecraft_versions(True)
        if name in ('forge', 'neoforge'):
            return {vn.split('-')[0] for vn in vers}
        return set(vers)
    except:
        return set()


def format_version_name(version_id: str) -> str:
    if version_id.startswith('neoforge'):
        return f"NeoForge {version_id.split('-')[1]}"
    elif 'forge' in version_id:
        return f"Forge {version_id.split('-')[0]}"
    if 'fabric' in version_id:
        return f"Fabric {version_id.split('-')[-1]}"
    if 'quilt' in version_id:
        return f"Quilt {version_id.split('-')[-1]}"
    if version_id.startswith('b'):
        return f"Beta {version_id[1:]}"
    if version_id.startswith('a'):
        return f"Alpha {version_id[1:]}"

    if version_id in v.game_versions:
        return f"Версия {version_id}"

    return version_id


def only_installed():
    mc_dir = get_minecraft_directory()

    return [format_version_name(vn['id']) for vn in get_installed_versions(mc_dir)]


def get_versions(mp=True):
    data = load_data('settings')["minecraft"]

    needs_modpacks = data['show_modpacks']
    needs_server_data = data['show_all_versions']

    result = []

    if needs_server_data:
        all_versions_ids = [i['id'] for i in get_cached_version_list()]
        result.extend(all_versions_ids)

    else:
        if mp and needs_modpacks:
            modpacks = load_data('modpacks')
            result.extend(f'MP {m}' for m in modpacks)

        result.extend(only_installed())

    return result


def get_versions_list(tip):
    result = []
    all_versions_ids = [i['id'] for i in get_cached_version_list()]

    if tip == "vanilla":
        for ver in v.game_versions:
            result.append(f"Версия {ver}")

        result.extend(f"Beta {vid[1:]}" for vid in all_versions_ids if vid.startswith('b'))
        result.extend(f"Alpha {vid[1:]}" for vid in all_versions_ids if vid.startswith('a'))

    if tip in ('forge', 'fabric', 'quilt', 'neoforge'):
        valur = get_cached_loader_versions(tip)

        for ver in v.game_versions:
            if ver in valur:
                if tip != 'neoforge':
                    result.append(f"{tip.title()} {ver}")
                else:
                    result.append(f"NeoForge {ver}")

    if tip == 'snapshots':
        for i in get_cached_version_list():
            if i['type'] == 'snapshot':
                result.append(f"Снапшот {i['id']}")

    return result
