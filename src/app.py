from threading import Thread

from PyQt6.QtCore import (QPropertyAnimation, QParallelAnimationGroup, QEasingCurve, QPoint, Qt,
                          QTimer)
from PyQt6.QtGui import QFontDatabase, QPixmap, QPainter, QColor, QIcon

from src.game_launch import LaunchThread
from src.modpacks import MrpackInstallThread
from src.modrinth import download_from_modrinth, get_from_modrinth
from src.threads import *
from src.config import *
from src import values as v
from src.json_parser import dump_data, load_data
from src.tabs import *


def colorize_icon(path: str, color: str) -> QIcon:
    """ Перекраска иконок в определённый цвет color """
    pixmap = QPixmap(path)
    colored = QPixmap(pixmap.size())
    colored.fill(Qt.GlobalColor.transparent)

    painter = QPainter(colored)
    painter.drawPixmap(0, 0, pixmap)
    painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
    painter.fillRect(colored.rect(), QColor(color))
    painter.end()

    return QIcon(colored)


class MyApplication(QApplication):
    def __init__(self, *args):
        super().__init__(*args)
        self._setup_parameters()
        self._add_font()

    def _setup_parameters(self):
        self.setWindowIcon(QIcon('./assets/images/logo.png'))
        self.setApplicationName("RayLauncher")
        self.setApplicationVersion(v.version)

    @staticmethod
    def _add_font():
        QFontDatabase.addApplicationFont('./assets/resources/Rubik-VariableFont_wght.ttf')


class MainWindow(QMainWindow):
    def __init__(self, *args):
        super().__init__(*args)
        self._setup_parameters()
        self._launcher_run()

    def _launcher_run(self):
        if v.config["launcher_run"]:
            self.launcher_run()
        else:
            self.setStyleSheet(v.stylesheet_start)
            self.st0 = StartWizard(self)

    def _setup_parameters(self):
        self.setWindowTitle(f"RayLauncher {v.version}")
        self.setFixedSize(QSize(940, 560))

    def _init_ui(self):
        self.tab_loading = Loading(self)
        self.t0 = Main(self)

        self.tabs = StackedWidget(self, 830, 460)
        self.tabs.move(90, 70)

        tabs = (
            Home(self),
            Settings(self),
            About(self),
            Servers(self),
            Content(self),
            Accounts(self),
            WebPlay(self),
            Versions(self),
            Console(self),
            Socials(self)
        )

        for widget in tabs:
            self.tabs.addWidget(widget)

        self.tab_loading.show()
        self.tab_loading.raise_()

        light = load_data('settings')['design']['theme']
        color_logo = 'dark' if light == 'light' else 'light'

        self.ld_logo.set_image(f'logo_{color_logo}.png')
        self.logo_text.set_image(f'logo_{color_logo}.png', size=(180, 30))
        self.about_logo.set_image(f'logo_{color_logo}.png', size=(300, 50))

        self.change_theme()

    def _on_loading_finished(self):
        if v.tab_start_now:
            self.st0.deleteLater()
            self.t0.show()
            self.tabs.show()

        self.tab_loading.deleteLater()

    def launcher_run(self):
        self._init_ui()

        # Потоки
        self.thread_progress = ProgressThread(self)
        self.thread_progress.progress.connect(self.ld_progress_bar.setValue)
        self.thread_progress.finished.connect(self._on_loading_finished)
        self.thread_progress.start()

        self.thread_loading = LoadingThread(self)
        self.thread_loading.start()

        self.launch_thread = LaunchThread(self)
        self.launch_thread.state_update_signal.connect(self.state_update)
        self.launch_thread.progress_update_signal.connect(self.update_progress)
        self.launch_thread.finished.connect(self.to_play)

        self.install_mrpack_thread = MrpackInstallThread(self)
        self.install_mrpack_thread.progress.connect(self.update_progress_mrpack)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.start_network_check)
        self.timer.start(5000)

    # ==========================================================================================
    # ВКЛАДКИ И НАВИГАЦИЯ
    # ==========================================================================================
    def next_start_tab(self):
        if v.tab_start_now == 3:
            username = check_nickname(self.start_entryE4.text())
            if not username:
                return
            self.start_button.setText("Играть!")

        v.tab_start_now += 1
        self.start_tabs.setCurrentIndex(v.tab_start_now)

        if v.tab_start_now == 5:
            data = load_data('settings')

            data['minecraft']['path'] = self.start_entryE3.text()
            data['java']['my_java'] = bool(self.start_entryE2.text())
            data['java']['my_path'] = self.start_entryE2.text()
            user, uuid = self.start_entryE4.text(), generate_random_uuid()

            dump_data(data, 'settings')
            dump_data({user: uuid}, 'users')

            v.users[user] = uuid

            data = load_data('config')
            data['launcher_run'] = True
            dump_data(data, 'config')

            self.st0.hide()
            self.launcher_run()

        else:
            self.nav_labels[v.tab_start_now].setStyleSheet(v.style_tab_active)

    def open_tab(self, name, act=False, to_home=False):
        if not act:
            if name == 'home' and to_home:
                v.tab_list, v.tab_now = ['home'], 0
            else:
                v.tab_list = v.tab_list[:v.tab_now + 1] + [name]
                v.tab_now = len(v.tab_list) - 1

        if name == 'settings':
            self.load_settings_to_ui()
        elif name == 'console':
            self.update_logs()

        tab_title = v.tabs_list[name]
        tab_idx = v.tabs_index[name]

        self.tabs.setCurrentIndex(tab_idx)
        self.info_title.setText(tab_title)

        self._update_navigation_buttons()
        self._update_sidebar_style(name)

        target_widget = self.tabs.widget(tab_idx)
        if v.animation and target_widget:
            self.run_tab_animation(target_widget)

    def load_settings_to_ui(self):
        data = load_data('settings')

        mapping = {
            self.checkbox11: data["design"]['button_web_play'],
            self.checkbox12: data["design"]['animation'],

            self.checkbox21: data["parameters"]['button_black'],
            self.combobox_network: data["parameters"]['network_check'],
            self.checkbox22: data["parameters"]['incognito'],

            self.entry_minecraft: data['minecraft']['path'],
            self.checkbox31: data['minecraft']['hide_in_game'],
            self.checkbox32: data['minecraft']['files_log4j'],
            self.checkbox33: data['minecraft']['lock_multiplayer'],
            self.checkbox34: data['minecraft']['lock_chat'],
            self.checkbox35: data['minecraft']['demo'],
            self.checkbox37: data['minecraft']['show_all_versions'],
            self.checkbox36: data['minecraft']['show_modpacks'],

            self.checkbox41: data['java']["my_java"],
            self.entry_java: data['java']["my_path"],
            self.checkbox42: data['java']["console_show"]
        }

        for widget, value in mapping.items():
            if isinstance(widget, CheckBox):
                widget.setChecked(value)
            elif isinstance(widget, LineEdit):
                widget.setText(str(value))

    def _update_navigation_buttons(self):
        img1 = int(v.tab_now > 0)
        img2 = int(v.tab_now < len(v.tab_list) - 1)
        self.button_left.set_icon(f'left{img1}.png')
        self.button_right.set_icon(f'right{img2}.png')

    def _update_sidebar_style(self, name):
        for btn in self.side_buttons:
            btn.setStyleSheet(v.style_side)

        if name in v.side_tabs:
            self.side_buttons[v.side_tabs[name]].setStyleSheet(v.style_side_active)

    def run_tab_animation(self, target_widget):
        if not target_widget or not v.animation:
            return

        effect = target_widget.graphicsEffect()
        if not isinstance(effect, QGraphicsOpacityEffect):
            effect = QGraphicsOpacityEffect(target_widget)
            target_widget.setGraphicsEffect(effect)

        if hasattr(self, '_current_anim') and self._current_anim:
            self._current_anim.stop()
            self._current_anim.deleteLater()

        self._current_anim = QParallelAnimationGroup(self)

        anim_opacity = QPropertyAnimation(effect, b"opacity")
        anim_opacity.setDuration(300)
        anim_opacity.setStartValue(0.0)
        anim_opacity.setEndValue(1.0)

        anim_pos = QPropertyAnimation(target_widget, b"pos")
        anim_pos.setDuration(400)
        anim_pos.setStartValue(QPoint(0, 20))
        anim_pos.setEndValue(QPoint(0, 0))
        anim_pos.setEasingCurve(QEasingCurve.Type.OutCubic)

        self._current_anim.addAnimation(anim_opacity)
        self._current_anim.addAnimation(anim_pos)

        self._current_anim.start()

    def open_settings_tab(self, index):
        self.tabs_stack.setCurrentIndex(index)

        for btn in self.buttons:
            btn.setStyleSheet(v.style_settings)

        self.buttons[index].setStyleSheet(v.style_settings_active)

    def action_to(self, to):
        if to:
            if v.tab_now < len(v.tab_list) - 1:
                v.tab_now += 1
        else:
            if v.tab_now > 0:
                v.tab_now -= 1

        self.open_tab(v.tab_list[v.tab_now], act=True)

    # ==========================================================================================
    # ЗАПУСК ИГРЫ
    # ==========================================================================================
    def to_play(self):
        if v.game_launch_type == 'yes':
            if v.game_launch_type == 'update':
                v.game_updates.remove(self.combobox_versions.currentText())
            else:
                v.game_no_installs.remove(self.combobox_versions.currentText())

            v.game_launch_type = 'play'
            self.button_play.setText('Играть!')

    def state_update(self, value):
        self.progress_label.setVisible(value)
        self.progress_bar.setVisible(value)
        self.button_play.setDisabled(value)

    def update_progress(self, progress, max_progress, label):
        self.progress_bar.setValue(progress)
        self.progress_bar.setMaximum(max_progress)
        self.progress_label.setText(f'{progress - 1} из {max_progress} файлов [{label}]')

    def launch_game(self, in_server=False, server_version=None):
        user = self.combobox_users.currentText()
        ver = self.combobox_versions.currentText()

        if not user:
            return Message('info', "Ошибка", "У вас нет аккаунта, создайте его.")

        if v.demo:
            one, two = version_info(ver)
            if two != 'none' or one in {'1.0', '1.1', '1.2.1', '1.2.2', '1.2.3', '1.2.4', '1.2.5'}:
                return Message('info', "Ошибка", "Данная версия не поддерживает демо-версию.")

        # Параметры
        users_data = load_data('users')
        v.game_parameters.update({"user": user, "uuid": users_data.get(user)})

        data = load_data('config')
        data.update({"user": user, "version": ver})
        dump_data(data, 'config')

        v.g_version, v.g_modloader = version_info(server_version if in_server else ver)

        # Запуск игры
        self.launch_thread.start()
        return None

    # ==========================================================================================
    # РАЗЛИЧНЫЙ ФУНКЦИОНАЛ
    # ==========================================================================================
    def update_logs(self):
        log_dir = os.path.join(os.environ['APPDATA'], ".raylauncher", "launcher", "logs")
        log_path = os.path.join(log_dir, 'client.log')

        try:
            if os.path.exists(log_path):
                with open(log_path, 'r', encoding='utf-8', errors='ignore') as file:
                    content = file.read()
                    self.log_area.setPlainText(content)

                    scroll_bar = self.log_area.verticalScrollBar()
                    scroll_bar.setValue(scroll_bar.maximum())
            else:
                self.log_area.setPlainText("Консоль пуста")
        except Exception as e:
            self.log_area.setPlainText(f"Ошибка при чтении логов: {e}")

    def change_version(self):
        ver = self.combobox_versions.currentText()

        if ver in v.game_no_installs:
            res = ('Установить', 'install')
        elif ver in v.game_updates:
            res = ('Обновить', 'update')
        else:
            res = ('Играть!', 'play')

        self.button_play.setText(res[0])
        v.game_launch_type = res[1]

    def update_list_versions(self):
        tip = v.game_versions_type[self.combobox_vr1.currentText()]

        self.combobox_vr2.clear()
        self.combobox_vr2.addItems(get_versions_list(tip))

    def select_version(self):
        val = self.combobox_vr2.currentText()
        idx = self.combobox_versions.findText(val)

        if idx == -1:
            self.combobox_versions.addItem(val)
            self.combobox_versions.setCurrentIndex(self.combobox_versions.count() - 1)
            self.button_play.setText('Установить')
            v.game_launch_type = 'install'
            v.game_no_installs.append(val)
        else:
            self.combobox_versions.setCurrentIndex(idx)
            self.button_play.setText('Обновить')
            v.game_launch_type = 'update'
            v.game_updates.append(val)

        self.open_tab('home')

    def start_network_check(self):
        if hasattr(self, 'check_thread') and self.check_thread.isRunning():
            return

        self.check_thread = CheckNetworkThread()
        self.check_thread.status_checked.connect(self.set_connect)
        self.check_thread.start()

    def set_connect(self, is_online):
        v.network = is_online
        self.info_icon0.set_image(f'connected{int(v.network)}.png')

    def update_progress_mrpack(self, label):
        self.pk_label5.setText(label)

    def mrpack_install(self):
        if not v.mrpack_path:
            Message('info', "Информация", "Выберите файл .mrpack для установки сборки.")
            return

        self.install_mrpack_thread.start()

    def change_content_tabs(self, index):
        if index != 0:
            self.combobox_m2.clear()
            self.combobox_m2.addItems({1: ['forge', 'fabric'], 2: ['optifine', 'iris']}[index])

        index = 0 if index == 0 else 1
        self.tabs1.setCurrentIndex(index)

    def get_mods(self):
        tip = {'Моды': 'mod', 'Шейдеры': 'shader'}[self.combobox_pp.currentText()]
        loader = self.combobox_m2.currentText()
        version = self.combobox_m3.currentText()

        v.mods = {'tip': tip, 'loader': loader, 'version': version}
        mods = get_from_modrinth(tip, 6, loader, version)

        while len(mods) < 6:
            mods.append('...')

        for i in range(6):
            self.mbuttons[i].text.setText(mods[i])

            if not v.mod:
                self.mbuttons[i].button.set_function(partial(self.download_mod, i))

        v.mod = True

    def download_mod(self, text):
        mod = self.mbuttons[text].text.text()

        if mod != '...':
            download_from_modrinth(v.mods['tip'], mod, v.mods['loader'], v.mods['version'])

    def choose_java(self):
        file, _ = QFileDialog.getOpenFileName(self, 'Выберите Java',
                                              filter='Java (java.exe javaw.exe)')
        if file:
            self.start_entryE2.setText(file)

    def choose_minecraft(self, entry):
        path = QFileDialog.getExistingDirectory(self, 'Выберите папку для Minecraft')
        if path:
            entry.setText(path)

    def choose_background(self, index, combo_box, v_path_attr):
        if index == 7:
            file, _ = QFileDialog.getOpenFileName(self, 'Выберите изображение',
                                                  filter='Изображение (*.png *.jpg *.bmp)')
            if file:
                setattr(v, f'img_path{v_path_attr}', file)
            else:
                combo_box.setCurrentIndex(0)

    def now_change_background(self):
        data = load_data('settings')

        data["design"]["launcher"] = [self.combobox_backgrounds1.currentIndex() + 1, v.img_path2]

        dump_data(data, 'settings')

        v.img2, v.img_path2 = data["design"]["launcher"]
        if v.img2 == 8:
            self.label_background.set_image(v.img_path2, all_path=True, size=(980, 580))
        else:
            self.label_background.set_image(f'bg{v.img2}.jpg')

    def _refresh_servers(self):
        for slot in self.slots:
            for child in slot.findChildren((Label, Button)):
                child.deleteLater()

        data_servers = load_data('servers')

        for i, data in data_servers.items():
            idx = int(i) - 1
            if idx >= len(self.slots):
                continue

            self.serv_icon = Label(self.slots[idx], 64, 64)
            self.serv_icon.set_image(f'server{data["icon"]}.png')
            self.serv_icon.move(13, 13)
            self.serv_icon.show()

            self.serv_name = Label(self.slots[idx], 220, 35, tag='name_server')
            self.serv_name.setText(data["name"])
            self.serv_name.move(96, 10)
            self.serv_name.show()

            self.serv_delete_btn = Button(self.slots[idx], 32, 32, tag='delete_button')
            self.serv_delete_btn.set_icon('delete.png', (24, 24))
            self.serv_delete_btn.set_function(partial(self.server_delete, i))
            self.serv_delete_btn.move(96, 46)
            self.serv_delete_btn.show()

            self.serv_play_btn = Button(self.slots[idx], 60, 60, tag='play', cursor=True)
            self.serv_play_btn.set_icon('server_play.png', (44, 44))
            self.serv_play_btn.set_function(partial(self.server_play, i))
            self.serv_play_btn.move(465, 15)
            self.serv_play_btn.show()

    def server_add(self):
        self.serv_frame.hide()
        self.serv_frame2.show()
        self.serv_add.set_function(partial(self.server_add_function))

    def server_add_function(self):
        data_servers = load_data('servers')

        if len(data_servers) >= 3:
            Message('warn', "Лимит", "Максимум можно добавить 3 сервера!")
            self.serv_frame2.hide()
            self.serv_frame.show()
            return

        new_id = str(len(data_servers) + 1)
        icon_key = self.serv_set2.currentText()

        data_servers[new_id] = {
            "name": self.serv_set1.text(),
            "server": self.serv_set3.text(),
            "port": self.serv_set4.text(),
            "version_game": self.serv_set5.currentText(),
            "icon": v.servers_icons.get(icon_key, "default.png")
        }

        dump_data(data_servers, 'servers')
        self._refresh_servers()
        self.serv_frame2.hide()
        self.serv_frame.show()

        self.serv_add.set_function(partial(self.server_add))
        Message('info', "Успех", "Сервер был успешно добавлен!")

    def server_play(self, number):
        data_server = load_data('servers')[str(number)]

        v.game_parameters.update({"server": data_server['server'], "port": data_server['port']})

        self.launch_game(in_server=True, server_version=data_server['version_game'])

    def server_delete(self, number):
        data = load_data('servers')

        data.pop(str(number), None)
        new_data = {str(i + 1): val for i, val in enumerate(data.values())}

        dump_data(new_data, 'servers')

        self._refresh_servers()
        self.serv_frame2.hide()

        Message('info', "Информация", "Сервер был удалён из списка!")

    def _save_accounts(self, data):
        dump_data(data, 'users')
        v.users = data

        usernames = list(v.users.keys())
        for combobox in (self.combobox_users, self.combobox_users2):
            combobox.clear()
            combobox.addItems(usernames)

    def add_account(self):
        username = check_nickname(self.textbox.text())
        if not username:
            return None

        data = load_data('users')

        if len(data) >= 20:
            return Message('warn', "Ошибка", "Лимит - 20 аккаунтов!")

        if username in data:
            return Message('warn', "Ошибка", "Аккаунт уже существует!")

        data[username] = generate_random_uuid()
        self._save_accounts(data)

        return Message('info', "Информация", "Новый аккаунт создан успешно")

    def delete_account(self):
        username = self.combobox_users2.currentText()
        if not username:
            return

        data = load_data('users')

        if username in data:
            del data[username]
            self._save_accounts(data)
            Message('info', "Информация", "Аккаунт удалён")

    def change_theme(self):
        themed_icons = (
            "side_home.png", "side_settings.png", "side_servers.png",
            "side_content.png", "side_about.png", "side_console.png",
        )

        color = load_data('settings')['design']['theme']

        if color == 'light':
            self.setStyleSheet(v.stylesheet_light)

            color = '#2A2C3A'
            for btn, icon in zip(self.side_buttons, themed_icons):
                btn.setIcon(colorize_icon(f"assets/images/{icon}", color))

            self.button_left.setIcon(colorize_icon("assets/images/left0.png", color))
            self.button_right.setIcon(colorize_icon("assets/images/right0.png", color))
            self.button_add.setIcon(colorize_icon("assets/images/add.png", color))
            self.button_add2.setIcon(colorize_icon("assets/images/add.png", color))
            self.button_m1.setIcon(colorize_icon("assets/images/add.png", color))
            self.tool3.setIcon(colorize_icon("assets/images/b_logs.png", color))
            self.tool4.setIcon(colorize_icon("assets/images/b_saves.png", color))
            self.tool5.setIcon(colorize_icon("assets/images/b_images.png", color))
            self.tool6.setIcon(colorize_icon("assets/images/b_folder.png", color))

            v.style_side = """
                    #side {background: #CDD1E2}
                    #side:hover {background: #BEC3D8}
                    #side:pressed {background: #9BA3C0}
                    """

            v.style_side_active = """
                    #side {background: #219CC2}
                    #side:hover {background: #27ADD6}
                    #side:pressed {background: #3EB3D6}
                    """
        else:
            self.setStyleSheet(v.stylesheet_dark)

            for btn, icon in zip(self.side_buttons, themed_icons):
                btn.setIcon(QIcon(f"assets/images/{icon}"))

            self.button_left.setIcon(QIcon("assets/images/left0.png"))
            self.button_right.setIcon(QIcon("assets/images/right0.png"))
            self.button_add.setIcon(QIcon("assets/images/add.png"))
            self.button_add2.setIcon(QIcon("assets/images/add.png"))
            self.button_m1.setIcon(QIcon("assets/images/add.png"))
            self.tool3.setIcon(QIcon("assets/images/b_logs.png"))
            self.tool4.setIcon(QIcon("assets/images/b_saves.png"))
            self.tool5.setIcon(QIcon("assets/images/b_images.png"))
            self.tool6.setIcon(QIcon("assets/images/b_folder.png"))

            v.style_side = """
                    #side {background: #262A3B}
                    #side:hover {background: #33394F}
                    #side:pressed {background: #404866}
                    """

            v.style_side_active = """
                    #side {background: #377ca3}
                    #side:hover {background: #399bc4}
                    #side:pressed {background: #399bc4}
                    """

    # ==========================================================================================
    # УПРАВЛЕНИЕ НАСТРОЙКАМИ
    # ==========================================================================================
    def _async_load_versions(self):
        try:
            versions = get_versions()
            self.combobox_versions.clear()
            self.combobox_versions.addItems(versions)
        except Exception:
            pass

        def update_ui():
            if versions:
                self.combobox_versions.clear()
                self.combobox_versions.addItems(versions)
            self.button_play.setDisabled(False)

        QTimer.singleShot(10, update_ui)

    def _update_ui_elements(self, data):
        self.button_web.setVisible(data["design"]["button_web_play"])

        button_black = data["parameters"]["button_black"]
        v.animation = data["design"]["animation"]
        v.demo = data["minecraft"]["demo"]
        v.network_check = data["parameters"]["network_check"]
        v.incognito = data["parameters"]["incognito"]

        self.tool2.set_function(
            lambda: open_site(f"https://modrinth.{'black' if button_black else 'com'}/mods"))

        v.img2, v.img_path2 = data["design"]["launcher"]
        if v.img2 == 5:
            self.label_background.set_image(v.img_path2, all_path=True, size=(980, 580))
        else:
            self.label_background.set_image(f'bg{v.img2}.jpg')

        self.change_theme()

    def set_default_settings(self):
        current_defaults = self.defaults.get(self.tabs_stack.currentIndex() + 1, {})

        for widget, value in current_defaults.items():
            if isinstance(widget, ComboBox):
                widget.setCurrentIndex(value)
            else:
                widget.setChecked(bool(value))

    def save_settings(self):
        self.button_play.setDisabled(True)

        data = {
            "design": {
                "theme": ('dark', 'light')[self.combobox_themes.currentIndex()],
                "loading": [self.combobox_art.currentIndex() + 1, v.img_path1],
                "launcher": [self.combobox_backgrounds.currentIndex() + 1, v.img_path2],
                "button_web_play": self.checkbox11.isChecked(),
                "animation": self.checkbox12.isChecked()
            },
            "parameters": {
                "button_black": self.checkbox21.isChecked(),
                "network_check": self.combobox_network.currentIndex(),
                "incognito": self.checkbox22.isChecked(),
            },
            "minecraft": {
                "path": self.entry_minecraft.text(),
                "memory": int(self.combobox_memores.currentText()[0]),
                "hide_in_game": self.checkbox31.isChecked(),
                "files_log4j": self.checkbox32.isChecked(),
                "lock_multiplayer": self.checkbox33.isChecked(),
                "lock_chat": self.checkbox34.isChecked(),
                "demo": self.checkbox35.isChecked(),
                "show_all_versions": self.checkbox37.isChecked(),
                "show_modpacks": self.checkbox36.isChecked()
            },
            "java": {
                "my_java": self.checkbox41.isChecked(),
                "my_path": self.entry_java.text(),
                "console_show": self.checkbox42.isChecked(),
            }
        }

        dump_data(data, 'settings')
        self._update_ui_elements(data)
        Thread(target=self._async_load_versions, daemon=True).start()
