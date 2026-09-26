import subprocess
import os
import sys
import traceback

from PyQt6.QtCore import QThread, pyqtSignal
import minecraft_launcher_lib as mll

from src import json_parser as jp, values as v


class LaunchThread(QThread):
    launch_setup_signal = pyqtSignal(str, str)
    progress_update_signal = pyqtSignal(int, int, str)
    state_update_signal = pyqtSignal(bool)

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.progress = 0
        self.progress_max = 0
        self.progress_label = ""

    def _emit_progress(self, current=None, maximum=None, label=None):
        if current is not None: self.progress = current
        if maximum is not None: self.progress_max = maximum
        if label is not None: self.progress_label = label
        self.progress_update_signal.emit(self.progress, self.progress_max, self.progress_label)

    def run(self):
        try:
            self.state_update_signal.emit(True)
            minecraft_dir = jp.get_minecraft_directory()

            opt = jp.load_data('settings')
            opt_game = opt.get("minecraft", {})
            opt_java = opt.get("java", {})

            options = {
                'username': v.game_parameters.get("user", "Player"),
                'uuid': v.game_parameters.get("uuid", ""),
                'token': '0',
                'jvmArguments': [f'-Xmx{opt_game.get("memory", 2)}G'],
                'enableLoggingConfig': bool(opt_game['files_log4j']),
                'disableMultiplayer': bool(opt_game['lock_multiplayer']),
                'disableChat': bool(opt_game['lock_chat']),
                "launcherName": "RayLauncher",
                "launcherVersion": v.version
            }

            if v.demo:
                options['demo'] = True

            if v.game_parameters.get("server"):
                options['server'] = v.game_parameters["server"]

            if v.game_parameters.get("port"):
                options['port'] = v.game_parameters["port"]

            if opt_java.get("my_java"):
                java_path = opt_java["my_path"]
            else:
                self._emit_progress(label="Определение версии Java...")

                runtime_name = "java-runtime-alpha"

                try:
                    import json
                    version_json_path = os.path.join(minecraft_dir, "versions", v.g_version,
                                                     f"{v.g_version}.json")

                    if os.path.exists(version_json_path):
                        with open(version_json_path, 'r', encoding='utf-8') as f:
                            version_data = json.load(f)
                            if "javaVersion" in version_data:
                                runtime_name = version_data["javaVersion"].get("component",
                                                                               "java-runtime-alpha")
                except Exception as e:
                    print(f"Не удалось прочитать JSON версии: {e}")

                java_path = mll.runtime.get_executable_path(runtime_name, minecraft_dir)

                if not java_path:
                    self._emit_progress(label=f"Установка {runtime_name}...")
                    mll.runtime.install_jvm_runtime(runtime_name, minecraft_dir)
                    java_path = mll.runtime.get_executable_path(runtime_name, minecraft_dir)

            options["executablePath"] = java_path

            try:
                ver_parts = v.g_version.split('.')
                if ver_parts[0] == "1" and int(ver_parts[1]) <= 5:
                    options["gameDirectory"] = os.path.join(minecraft_dir, "versions", v.g_version)
            except:
                pass

            install_func = mll.install.install_minecraft_version
            version_to_launch = v.g_version

            if v.g_modloader == 'MP':
                mp_data = jp.load_data('modpacks').get(v.g_version)
                if mp_data:
                    version_to_install, version_to_launch = mp_data[0], mp_data[1]
                    options["gameDirectory"] = os.path.join(minecraft_dir, "instances",
                                                            v.g_version)

                    for loader_type in ('fabric', 'quilt', 'forge', 'neoforge'):
                        if loader_type in version_to_launch.lower():
                            install_func = mll.mod_loader.get_mod_loader(loader_type).install
                            break

            if v.g_modloader in ('fabric', 'quilt', 'forge', 'neoforge'):
                loader = mll.mod_loader.get_mod_loader(v.g_modloader)
                install_func = loader.install

                try:
                    l_ver = loader.get_latest_loader_version(v.g_version)

                    if v.g_modloader == 'forge':
                        version_to_launch = f"{v.g_version}-forge-{l_ver}"
                    elif v.g_modloader == 'neoforge':
                        version_to_launch = f"{v.g_version}-neoforge-{l_ver}"
                    else:
                        version_to_launch = f"{v.g_modloader}-loader-{l_ver}-{v.g_version}"

                except:
                    pass

            callbacks = {
                'setStatus': lambda x: self._emit_progress(label=str(x)),
                'setProgress': lambda x: self._emit_progress(current=int(x)),
                'setMax': lambda x: self._emit_progress(maximum=int(x))
            }

            if v.game_launch_type in ('update', 'install'):
                install_func(v.g_version, minecraft_dir, callback=callbacks)
                v.game_launch_type = 'yes'

            command = mll.command.get_minecraft_command(version_to_launch, minecraft_dir, options)

            if command:
                if opt_game.get("hide_in_game"):
                    self.parent.hide()

                log_dir = os.path.join(os.environ['APPDATA'], ".raylauncher", "launcher", "logs")
                os.makedirs(log_dir, exist_ok=True)
                log_file_path = os.path.join(log_dir, "client.log")

                print(f"Запуск команды. Логи: {log_file_path}")

                flags = 0
                if sys.platform == "win32" and not opt_java.get('console_show'):
                    flags = subprocess.CREATE_NO_WINDOW

                with open(log_file_path, "w", encoding="utf-8") as log_file:
                    process = subprocess.Popen(
                        command,
                        stdout=log_file,
                        stderr=log_file,
                        creationflags=flags
                    )
                    process.wait()

                if opt_game.get("hide_in_game"):
                    self.parent.show()

        except Exception as e:
            print(f"ОШИБКА: {e}")
            traceback.print_exc()

        finally:
            self.state_update_signal.emit(False)
