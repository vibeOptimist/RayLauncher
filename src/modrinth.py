import requests
import shutil

from src.json_parser import get_minecraft_directory
from src.widgets import Message


def get_from_modrinth(project, limit, loader, game_version):
    # Получение списка модификаций с сайта Modrinth

    base_url = "https://api.modrinth.com/v2/search"
    try:
        # Ищем модификации по загрузчику и версии Майнкрафта
        params = {
            "query": "",
            "facets": f'[["project_type:{project}"],["game_versions:{game_version}"],'
                      f'["categories:{loader}"]]',
            "limit": limit,
            "index": "downloads"
        }

        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Проверка ошибок
        results = response.json()["hits"]

        # Формируем список модификаций
        mods = [result["title"] for result in results]
        return mods

    except requests.exceptions.RequestException as e:
        Message('crit', "Ошибка", "Произошла критическая ошибка", info=e)
        return []


def download_from_modrinth(project, project_name, loader, game_version):
    # Скачивает модификацию с сайта Modrinth

    base_url = "https://api.modrinth.com/v2/search"
    try:
        # Ищем проект по названию
        params = {
            "query": project_name,
            "facets": f'[["project_type:{project}"],["game_versions:{game_version}"],'
                      f'["categories:{loader}"]]',
            "limit": 1
        }
        response = requests.get(base_url, params=params, timeout=2)
        response.raise_for_status()
        results = response.json()["hits"]

        if results:
            # Получаем ID проекта и загружаем последнюю версию
            project_id = results[0]["project_id"]
            versions_url = f"https://api.modrinth.com/v2/project/{project_id}/version"
            version_response = requests.get(versions_url)
            version_response.raise_for_status()

            # Фильтруем по Майнкрафту и загрузчику
            versions = version_response.json()
            for version in versions:
                if loader in version["loaders"] and game_version in version["game_versions"]:

                    # Скачать файл
                    file_info = version["files"][0]
                    download_url = file_info["url"]
                    file_name = file_info["filename"]

                    file_response = requests.get(download_url)
                    file_response.raise_for_status()
                    with open(file_name, "wb") as f:
                        f.write(file_response.content)

                    Message('info', "Информация",
                            f"Модификация {project_name} успешно скачана!")

                    try:
                        n = 'shaderpacks' if project == 'shader' else 'mods'
                        shutil.move(file_name, f"{get_minecraft_directory()}\\{n}\\{file_name}")
                    except:
                        Message('warn', "Ошибка", "Доступ к этой директории запрещён!")

                    return

            Message('warn', "Ошибка", "Не найдена подходящая версия модификации.")

        else:
            Message('warn', "Ошибка", "Модификация с таким названием не найдена.")

    except requests.exceptions.RequestException as e:
        Message('crit', "Ошибка", "Произошла критическая ошибка", info=e)
