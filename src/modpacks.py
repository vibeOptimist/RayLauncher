from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import QFileDialog
from minecraft_launcher_lib import mrpack

from src import values as v
from src.json_parser import get_minecraft_directory, dump_data, load_data


def mrpack_select(label):
    file, _ = QFileDialog.getOpenFileName(None, 'Выберите файл mrpack', filter='mrpack (*.mrpack)')
    if not file:
        return

    v.mrpack_path = file
    info = mrpack.get_mrpack_information(file)
    name, mc_ver = info['name'], info['minecraftVersion']
    loader = mrpack.get_mrpack_launch_version(file)
    v.mrpack_name = name

    data = load_data('modpacks')
    data[name] = [mc_ver, loader]
    dump_data(data, 'modpacks')

    label.setText(f"Название: {name}\nВерсия: {mc_ver}\nЗагрузчик: {loader}")


class MrpackInstallThread(QThread):
    progress = pyqtSignal(str)

    def run(self):
        if not v.mrpack_path:
            return

        mc_dir = get_minecraft_directory()
        modpack_dir = f"{mc_dir}\\{v.mrpack_name}"

        mrpack.install_mrpack(
            v.mrpack_path,
            mc_dir,
            modpack_directory=modpack_dir,
            callback={"setStatus": self.progress.emit}
        )
