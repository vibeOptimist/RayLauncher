from functools import partial

from src.widgets import *
from src import values as v
from src.game_versions import get_versions, get_versions_list
from src.modpacks import mrpack_select
from src.actions import *


class StartWizard(Widget):
    def __init__(self, main_window, *args):
        super().__init__(main_window, 940, 560, *args)
        self.window = main_window
        self.init_ui()

    def init_ui(self):
        self.start_frame_up = Frame(self, 940, 70, tag='start-frame')
        self.start_frame_up.move(0, 0)

        self.start_frame_down = Frame(self, 940, 70, tag='start-frame')
        self.start_frame_down.move(0, 490)

        self.window.nav_labels = []

        nav_items = ("Добро пожаловать!", "Java", "Minecraft", "Аккаунт", "Всё готово!")
        x_positions = (195, 385, 465, 585, 690)

        for text, x in zip(nav_items, x_positions):
            label = Label(self.start_frame_up, 180, 20, tag='start-label')
            label.setText(text)
            label.move(x, 28)
            self.window.nav_labels.append(label)

        self.window.start_button = Button(self.start_frame_down, 200, 40, text="Далее",
                                          tag='start-button')
        self.window.start_button.move(370, 15)
        self.window.start_button.set_function(self.window.next_start_tab)

        self.window.start_tabs = StackedWidget(self, 940, 450)
        self.window.start_tabs.move(0, 60)

        self.wss1 = Widget(self, 940, 450)
        self.window.start_tabs.addWidget(self.wss1)

        self.start_logo = Label(self.wss1, 300, 50)
        self.start_logo.set_image('logo_white.png', size=(300, 50))
        self.start_logo.move(320, 55)

        for i in range(4):
            f = Frame(self.wss1, 340, 110, tag='start-frame-part')
            f.move(480 if i // 2 else 120, 260 if i % 2 else 130)

            icon = Label(f, 72, 72)
            icon.set_image(f'start_icon{i + 1}.png')
            icon.move(20, 20)

            title = Label(f, 130, 22, tag='start-title')
            title.setText(v.start_text[i][0])
            title.move(110, 25)

            info = Label(f, 230, 40, tag='start-info')
            info.setText(v.start_text[i][1])
            info.move(110, 52)

        self.wss2 = Widget(self, 940, 450)
        self.window.start_tabs.addWidget(self.wss2)

        f2 = Frame(self.wss2, 500, 280, tag='start-frame-part')
        f2.move(220, 80)
        self._setup_page_base(f2, 'start_java.png', 'Выбор Java', v.start_text_java)

        self.window.start_entryE2 = LineEdit(f2, 440, 36, tag='start-entry')
        self.window.start_entryE2.move(30, 158)

        btn_java = Button(f2, 200, 36, text='Выбрать свою Java', tag='start-button')
        btn_java.move(50, 210)
        btn_java.set_function(self.window.choose_java)

        btn_dl_java = Button(f2, 180, 36, text='Скачать Java', tag='start-button')
        btn_dl_java.move(270, 210)
        btn_dl_java.set_function(lambda: open_site('https://www.java.com/ru/download/'))

        self.wss3 = Widget(self, 940, 450)
        self.window.start_tabs.addWidget(self.wss3)
        f3 = Frame(self.wss3, 500, 280, tag='start-frame-part')
        f3.move(220, 80)
        self._setup_page_base(f3, 'start_minecraft.png', 'Папка Minecraft', v.start_text_minecraft)

        self.window.start_entryE3 = LineEdit(f3, 440, 36, tag='start-entry')
        self.window.start_entryE3.move(30, 158)
        self.window.start_entryE3.setText(default_minecraft_directory())

        btn_mc = Button(f3, 150, 36, text='Выбрать путь', tag='start-button')
        btn_mc.move(175, 210)
        btn_mc.set_function(lambda: self.window.choose_minecraft(self.window.start_entryE3))

        self.wss4 = Widget(self, 940, 450)
        self.window.start_tabs.addWidget(self.wss4)

        f4 = Frame(self.wss4, 500, 280, tag='start-frame-part')
        f4.move(220, 80)
        self._setup_page_base(f4, 'start_account.png', 'Создание аккаунта', v.start_text_account)

        self.window.start_entryE4 = LineEdit(f4, 440, 36, tag='start-entry')
        self.window.start_entryE4.move(30, 158)

        self.wss5 = Widget(self, 940, 450)
        self.window.start_tabs.addWidget(self.wss5)

        title5 = Label(self.wss5, 300, 30, tag='start-title')
        title5.setText('Лаунчер готов к запуску!')
        title5.move(350, 200)

        self.window.nav_labels[0].setStyleSheet(v.style_tab_active)

    @staticmethod
    def _setup_page_base(frame, icon_path, title_text, info_text):
        icon = Label(frame, 80, 80, tag='start-title')
        icon.set_image(icon_path)
        icon.move(30, 30)

        title = Label(frame, 300, 30, tag='start-title')
        title.setText(title_text)
        title.move(130, 25)

        info = Label(frame, 290, 70, tag='start-info')
        info.setText(info_text)
        info.move(130, 50)


class Loading(Widget):
    def __init__(self, main_window, *args):
        super().__init__(main_window, 940, 560, *args)
        self.window = main_window
        self.init_ui()

    def init_ui(self):
        self.ld_background = Label(self, 940, 560)

        if v.img1 == 2:
            self.ld_background.set_image(v.img_path1, all_path=True, size=(940, 560))
        else:
            self.ld_background.set_image(f'bg{v.ai}.jpg')

        self.window.ld_progress_bar = ProgressBar(self, 940, 25, tag='start-progressbar')
        self.window.ld_progress_bar.move(0, 535)
        self.window.ld_progress_bar.setRange(0, 700)
        self.window.ld_progress_bar.setStyleSheet(v.style_bar)

        self.ld_frame = Frame(self, 440, 100, tag='start-frame')
        self.ld_frame.move(250, 26)

        self.window.ld_logo = Label(self.ld_frame, 360, 60)
        self.window.ld_logo.set_image('logo_white.png')
        self.window.ld_logo.move(40, 20)


class Main(Widget):
    def __init__(self, main_window, *args):
        super().__init__(main_window, 940, 560, *args)
        self.window = main_window
        self.init_ui()

    def init_ui(self):
        self.t0 = Widget(self, 940, 560)

        # Фон
        self.window.label_background = Label(self.t0, 940, 560)

        if v.img2 == 8:
            self.window.label_background.set_image(v.img_path2, all_path=True, size=(940, 560))
        else:
            self.window.label_background.set_image(f'bg{v.img2}.jpg')

        self.window.dark_background = Frame(self.t0, 980, 580, tag='dark-background')
        self.window.dark_background.setVisible(True)
        self.window.dark_background.move(0, 0)

        # Фреймы
        self.window.frame_top = Frame(self.t0, 900, 50, tag='fly-frame')
        self.window.frame_top.move(20, 10)

        self.window.frame_side = Frame(self.t0, 60, 460, tag='fly-frame')
        self.window.frame_side.move(20, 70)

        # Контент верхнего фрейма
        self.window.logo_text = Label(self.window.frame_top, 180, 30)
        self.window.logo_text.set_image('logo_white.png', size=(180, 30))
        self.window.logo_text.move(16, 10)

        self.window.button_left = Button(self.window.frame_top, 36, 36, tag='top')
        self.window.button_left.move(210, 6)
        self.window.button_left.set_icon('left0.png', (26, 26))
        self.window.button_left.set_function(lambda: self.window.action_to(False))

        self.window.button_right = Button(self.window.frame_top, 36, 36, tag='top')
        self.window.button_right.move(255, 6)
        self.window.button_right.set_icon('right0.png', (26, 26))
        self.window.button_right.set_function(lambda: self.window.action_to(True))

        self.window.info_title = Label(self.window.frame_top, 260, 24, tag='toper-label')
        self.window.info_title.setText('Главная')
        self.window.info_title.move(310, 13)

        self.window.top_button_3 = Button(self.window.frame_top, 180, 36, tag='top')
        self.window.top_button_3.move(650, 6)
        self.window.top_button_3.setText('Соцсети')
        self.window.top_button_3.set_function(lambda: self.window.open_tab('socials'))
        self.window.top_button_3.set_icon('socials.png', (22, 22))

        self.window.info_icon0 = Label(self.window.frame_top, 25, 25)
        self.window.info_icon0.set_image('connected0.png')
        self.window.info_icon0.move(850, 12)

        # Контент на боковой панели
        side_cfg = (
            ('side_home.png', 'Главная', 50, lambda: self.window.open_tab('home', True), (27, 27)),
            ('side_settings.png', 'Настройки', 100, lambda: self.window.open_tab('settings'),
             (31, 31)),
            ('side_servers.png', 'Сервера', 150, lambda: self.window.open_tab('servers'), (26, 26)),
            ('side_content.png', 'Контент', 200, lambda: self.window.open_tab('content'), (28, 28)),
            ('side_about.png', 'О лаунчере', 316, lambda: self.window.open_tab('about'), (32, 32)),
            ('side_console.png', 'Консоль', 366, lambda: self.window.open_tab('console'), (28, 28)),
        )

        self.window.side_buttons = []
        for icon, tip, y, func, size in side_cfg:
            btn = Button(self.window.frame_side, 44, 44, tag='side', cursor=True)
            btn.move(8, y)
            btn.set_icon(icon, size)
            btn.setToolTip(tip)
            btn.set_function(func)
            self.window.side_buttons.append(btn)

        self.window.side_buttons[0].setStyleSheet(v.style_side_active)

        # Прогресс-бар
        self.window.progress_bar = ProgressBar(self, 940, 20, tag='ray')
        self.window.progress_bar.setProperty('value', 99)
        self.window.progress_bar.move(0, 540)

        self.window.progress_label = Label(self, 400, 20)
        self.window.progress_label.setText('')
        self.window.progress_label.move(40, 540)

        self.window.progress_label.hide()
        self.window.progress_bar.hide()


class Home(Widget):
    def __init__(self, main_window, *args):
        super().__init__(main_window, 940, 560, *args)
        self.window = main_window
        self.init_ui()

    def init_ui(self):
        tab = Widget(self, 830, 460)

        # Фреймы
        self.frame_down = Frame(tab, 810, 60, tag='base')
        self.frame_down.move(10, 400)

        self.frame_home11 = Frame(tab, 250, 170, tag='base')
        self.frame_home11.move(10, 210)

        self.frame_home3 = Frame(tab, 250, 220, tag='base')
        self.frame_home3.move(570, 160)

        # Фон
        self.window.label_fon = Label(self.frame_home11, 80, 30, tag='big')
        self.window.label_fon.setText("Фон")
        self.window.label_fon.move(112, 20)

        self.window.combobox_backgrounds1 = ComboBox(self.frame_home11, 170, 36)
        self.window.combobox_backgrounds1.addItems(v.list_backgrounds)
        self.window.combobox_backgrounds1.move(40, 60)
        self.window.combobox_backgrounds1.currentIndexChanged.connect(
            lambda index: self.window.choose_background(index,
                                                        self.window.combobox_backgrounds1, 2))
        self.window.combobox_backgrounds1.setCurrentIndex(0)

        self.window.tool11 = Button(self.frame_home11, 170, 30, text="Применить", tag='cbutton')
        self.window.tool11.move(40, 110)
        self.window.tool11.set_function(self.window.now_change_background)

        # Виджеты нижней панели
        self.window.combobox_users = ComboBox(self.frame_down, 200, 40, tag='s')
        self.window.combobox_users.addItems(v.users.keys())
        self.window.combobox_users.move(15, 10)
        self.window.combobox_users.setCurrentIndex(v.index_user)

        self.window.button_add = Button(self.frame_down, 34, 34, tag='add')
        self.window.button_add.move(177, 13)
        self.window.button_add.set_icon('add.png', (30, 30))
        self.window.button_add.set_function(lambda: self.window.open_tab('accounts'))

        self.window.combobox_versions = ComboBox(self.frame_down, 220, 40, tag='s')
        self.window.combobox_versions.move(230, 10)
        self.window.combobox_versions.addItems(get_versions())

        if v.index_version:
            self.window.combobox_versions.setCurrentIndex(v.index_version)

        self.window.combobox_versions.currentIndexChanged.connect(self.window.change_version)

        self.window.button_add2 = Button(self.frame_down, 34, 34, tag='add')
        self.window.button_add2.move(412, 13)
        self.window.button_add2.set_icon('add.png', (30, 30))
        self.window.button_add2.set_function(lambda: self.window.open_tab('versions'))

        self.window.button_web = Button(self.frame_down, 40, 40, tag='play', cursor=True)
        self.window.button_web.move(540, 10)
        self.window.button_web.set_icon('web_play.png', (28, 28))
        self.window.button_web.set_function(lambda: self.window.open_tab('web_play'))

        if not v.button_web:
            self.window.button_web.hide()

        self.window.button_play = Button(self.frame_down, 200, 40, text="Играть!", tag='play',
                                         cursor=True)
        self.window.button_play.move(590, 10)
        self.window.button_play.set_function(self.window.launch_game)

        # Инструменты
        self.window.label_tools = Label(self.frame_home3, 140, 30, tag='big')
        self.window.label_tools.setText("Инструменты")
        self.window.label_tools.move(74, 20)

        self.window.tool1 = Button(self.frame_home3, 190, 30, text="Minecraft Wiki", tag='cbutton')
        self.window.tool1.move(30, 60)
        self.window.tool1.set_function(lambda: open_site('https://minecraft.wiki'))

        self.window.tool2 = Button(self.frame_home3, 190, 30, text="Modrinth", tag='cbutton')
        self.window.tool2.move(30, 100)
        self.window.tool2.set_function(lambda: open_site(f'https://modrinth.'
                                                         f'{'black' if v.button_black else 'com'}'
                                                         f'/mods'))

        self.window.tool3 = Button(self.frame_home3, 40, 40, tag='cbutton')
        self.window.tool3.move(30, 140)
        self.window.tool3.set_icon('b_logs.png', (28, 28))
        self.window.tool3.set_function(lambda: open_directory("logs"))

        self.window.tool4 = Button(self.frame_home3, 40, 40, tag='cbutton')
        self.window.tool4.move(80, 140)
        self.window.tool4.set_icon('b_saves.png', (28, 28))
        self.window.tool4.set_function(lambda: open_directory("saves"))

        self.window.tool5 = Button(self.frame_home3, 40, 40, tag='cbutton')
        self.window.tool5.move(130, 140)
        self.window.tool5.set_icon('b_images.png', (30, 30))
        self.window.tool5.set_function(lambda: open_directory("screenshots"))

        self.window.tool6 = Button(self.frame_home3, 40, 40, tag='cbutton')
        self.window.tool6.move(180, 140)
        self.window.tool6.set_icon('b_folder.png', (30, 30))
        self.window.tool6.set_function(lambda: open_directory("game"))


class Settings(Widget):
    def __init__(self, main_window, *args):
        super().__init__(main_window, 940, 560, *args)
        self.window = main_window
        self.init_ui()

    def init_ui(self):
        tab = Widget(self, 830, 460)

        # Фреймы
        self.window.set_frame = Frame(tab, 750, 340, tag='base')
        self.window.set_frame.move(40, 30)

        self.window.set_frame_bar = Frame(tab, 420, 60, tag='base')
        self.window.set_frame_bar.move(200, 390)

        # Виджеты
        self.window.set_title = Label(self.window.set_frame, 110, 30, tag='set-label1')
        self.window.set_title.setText('Настройки')
        self.window.set_title.move(90, 22)

        self.window.tabs_stack = QStackedWidget(self.window.set_frame)
        self.window.tabs_stack.setGeometry(250, 10, 490, 320)

        self.window.settings_tabs_content = []

        sizes = (400, 400, 520, 400, 400)
        for i, h in enumerate(sizes):
            content_widget = Widget(None, 472, h)
            self.window.settings_tabs_content.append(content_widget)
            setattr(self.window, f'sws{i + 1}', content_widget)
            scroll = ScrollArea(None, 490, 320)
            scroll.setWidget(content_widget)

            self.window.tabs_stack.addWidget(scroll)

        # Вкладки
        s_texts = ("Оформление", "Параметры", "Minecraft", "Java", "Справка")

        self.window.buttons = []
        for i in range(5):
            button = Button(self.window.set_frame, 188, 38, text=f' \u203A  {s_texts[i]}',
                            tag='set-button')

            button.move(30, 65 + i * 48)
            button.set_function(partial(self.window.open_settings_tab, i))
            self.window.buttons.append(button)

        if self.window.buttons:
            self.window.buttons[0].setStyleSheet(v.style_settings_active)

        # Кнопки
        self.set_button1 = Button(self.window.set_frame_bar, 170, 40, text='По умолчанию',
                                  tag='cbutton')
        self.set_button1.move(30, 10)
        self.set_button1.set_function(self.window.set_default_settings)

        self.set_button2 = Button(self.window.set_frame_bar, 170, 40, text='Сохранить',
                                  tag='cbutton')
        self.set_button2.move(220, 10)
        self.set_button2.set_function(self.window.save_settings)

        # Вкладка 1
        self.s_label = Label(self.window.sws1, 100, 25, tag='set-title')
        self.s_label.setText('Тема:')
        self.s_label.move(20, 25)

        self.window.combobox_themes = ComboBox(self.window.sws1, 180, 36)
        self.window.combobox_themes.addItems(('Тёмная', 'Светлая'))
        self.window.combobox_themes.move(30, 60)
        self.window.combobox_themes.setCurrentIndex(0)

        self.s_label11 = Label(self.window.sws1, 160, 25, tag='set-title')
        self.s_label11.setText('Задний фон:')
        self.s_label11.move(20, 115)

        self.s_label_0 = Label(self.window.sws1, 100, 20)
        self.s_label_0.setText('Лаунчер:')
        self.s_label_0.move(30, 158)

        self.s_label_1 = Label(self.window.sws1, 100, 20)
        self.s_label_1.setText('Загрузка:')
        self.s_label_1.move(30, 218)

        self.window.combobox_backgrounds = ComboBox(self.window.sws1, 180, 36)
        self.window.combobox_backgrounds.addItems(v.list_backgrounds)
        self.window.combobox_backgrounds.move(100, 150)
        self.window.combobox_backgrounds.currentIndexChanged.connect(
            lambda index: self.window.choose_background(index, self.window.combobox_backgrounds, 2))
        self.window.combobox_backgrounds.setCurrentIndex(0)

        self.window.combobox_art = ComboBox(self.window.sws1, 180, 36)
        self.window.combobox_art.addItems(v.list_arts)
        self.window.combobox_art.currentIndexChanged.connect(
            lambda index: self.window.choose_background(index, self.window.combobox_art, 1))
        self.window.combobox_art.move(100, 210)

        self.s_label12 = Label(self.window.sws1, 150, 25, tag='set-title')
        self.s_label12.setText('Интерфейс:')
        self.s_label12.move(20, 270)

        self.window.checkbox11 = CheckBox(self.window.sws1, 270, 20)
        self.window.checkbox11.setText("Кнопка игры в браузере")
        self.window.checkbox11.move(30, 305)

        self.window.checkbox12 = CheckBox(self.window.sws1, 450, 20)
        self.window.checkbox12.setText("Плавные анимации")
        self.window.checkbox12.move(30, 333)

        # Вкладка 2
        self.s_label41 = Label(self.window.sws2, 230, 25, tag='set-title')
        self.s_label41.setText('Зеркало Modrinth:')
        self.s_label41.move(20, 25)

        self.window.checkbox21 = CheckBox(self.window.sws2, 400, 20)
        self.window.checkbox21.setText("Открывать modrinth.black вместо modrinth.com")
        self.window.checkbox21.move(30, 60)

        self.s_label42 = Label(self.window.sws2, 330, 25, tag='set-title')
        self.s_label42.setText('Сервис проверки интернета:')
        self.s_label42.move(20, 100)

        self.window.combobox_network = ComboBox(self.window.sws2, 180, 36)
        self.window.combobox_network.addItems(('Cloudflare', 'Google', 'Yandex'))
        self.window.combobox_network.move(30, 140)
        self.window.combobox_network.setCurrentIndex(0)

        self.s_label43 = Label(self.window.sws2, 330, 25, tag='set-title')
        self.s_label43.setText('Инкогнито-проверка подключения:')
        self.s_label43.move(20, 190)

        self.window.checkbox22 = CheckBox(self.window.sws2, 400, 30)
        self.window.checkbox22.setText("Жёстко шифровать трафик подключения \n"
                                       "(Значительно увеличивает нагрузку на CPU)")
        self.window.checkbox22.move(30, 225)

        # Вкладка 3
        self.s_label21 = Label(self.window.sws3, 220, 25, tag='set-title')
        self.s_label21.setText('Папка Minecraft:')
        self.s_label21.move(20, 25)

        self.window.entry_minecraft = LineEdit(self.window.sws3, 370, 30)
        self.window.entry_minecraft.move(30, 60)

        self.button011 = Button(self.window.sws3, 30, 30, tag='cbutton')
        self.button011.move(410, 60)
        self.button011.set_function(
            lambda: self.window.choose_minecraft(self.window.entry_minecraft))

        self.s_label210 = Label(self.window.sws3, 280, 25, tag='set-title')
        self.s_label210.setText('Выделяемая память (ОЗУ):')
        self.s_label210.move(20, 105)

        self.window.combobox_memores = ComboBox(self.window.sws3, 160, 36)
        self.window.combobox_memores.addItems(v.memory_uses)
        self.window.combobox_memores.move(30, 140)
        self.window.combobox_memores.setCurrentIndex(v.memory_count)

        self.s_label22 = Label(self.window.sws3, 220, 25, tag='set-title')
        self.s_label22.setText('Игровые опции:')
        self.s_label22.move(20, 190)

        self.window.checkbox31 = CheckBox(self.window.sws3, 220, 20)
        self.window.checkbox31.setText("Скрыть лаунчер во время игры")
        self.window.checkbox31.move(30, 225)

        self.window.checkbox32 = CheckBox(self.window.sws3, 270, 20)
        self.window.checkbox32.setText("Разрешить файлы конфигурации Log4J")
        self.window.checkbox32.move(30, 253)

        self.window.checkbox33 = CheckBox(self.window.sws3, 250, 20)
        self.window.checkbox33.setText("Заблокировать мультиплеер")
        self.window.checkbox33.move(30, 281)

        self.window.checkbox34 = CheckBox(self.window.sws3, 270, 20)
        self.window.checkbox34.setText("Заблокировать чат в мультиплеере")
        self.window.checkbox34.move(30, 309)

        self.window.checkbox35 = CheckBox(self.window.sws3, 270, 20)
        self.window.checkbox35.setText("Запуск демо-версии игры")
        self.window.checkbox35.move(30, 337)

        self.s_label23 = Label(self.window.sws3, 140, 25, tag='set-title')
        self.s_label23.setText('Список версий:')
        self.s_label23.move(20, 370)

        self.window.checkbox36 = CheckBox(self.window.sws3, 200, 20)
        self.window.checkbox36.setText("Отображать модпаки")
        self.window.checkbox36.move(30, 405)

        self.window.checkbox37 = CheckBox(self.window.sws3, 270, 20)
        self.window.checkbox37.setText("Загружать список всех версий Minecraft")
        self.window.checkbox37.move(30, 433)

        # Вкладка 4
        self.s_label31 = Label(self.window.sws4, 200, 25, tag='set-title')
        self.s_label31.setText('Путь к Java:')
        self.s_label31.move(20, 25)

        self.window.checkbox41 = CheckBox(self.window.sws4, 270, 20)
        self.window.checkbox41.setText("Использовать свою Java")
        self.window.checkbox41.move(30, 60)

        self.window.entry_java = LineEdit(self.window.sws4, 330, 30)
        self.window.entry_java.move(30, 90)

        self.s_label32 = Label(self.window.sws4, 200, 25, tag='set-title')
        self.s_label32.setText('Опции Java:')
        self.s_label32.move(20, 145)

        self.window.checkbox42 = CheckBox(self.window.sws4, 290, 20)
        self.window.checkbox42.setText("Показывать консоль Java")
        self.window.checkbox42.move(30, 180)

        # Вкладка 5
        self.set6_label1 = Label(self.window.sws5, 390, 25, tag='set-title')
        self.set6_label1.setText(f'RayLauncher {v.version} (by Danila)')
        self.set6_label1.move(30, 25)

        self.set6_label2 = Label(self.window.sws5, 390, 50, tag='set-title')
        self.set6_label2.setText('RayLauncher — это стильный, быстрый и бесплатный \n'
                                 'Minecraft-лаунчер.')
        self.set6_label2.move(30, 55)

        self.open1 = Button(self.window.sws5, 160, 30, tag='cbutton')
        self.open1.setText('Подробнее')
        self.open1.move(30, 120)
        self.open1.set_function(lambda: self.window.open_tab('about'))

        self.open2 = Button(self.window.sws5, 160, 30, tag='cbutton')
        self.open2.setText('GitHub')
        self.open2.move(200, 120)
        self.open2.set_function(lambda: open_site('https://github.com/vibeOptimist/RayLauncher'))

        self.open3 = Button(self.window.sws5, 160, 30, tag='cbutton')
        self.open3.setText('Telegram')
        self.open3.move(30, 160)
        self.open3.set_function(lambda: open_site('https://t.me/raylauncher'))

        self.open4 = Button(self.window.sws5, 160, 30, tag='cbutton')
        self.open4.setText('Вконтакте')
        self.open4.move(200, 160)
        self.open4.set_function(lambda: open_site('https://vk.com/raylauncher'))

        self.window.defaults = {
            1: {self.window.combobox_art: 0, self.window.combobox_backgrounds: 0,
                self.window.combobox_themes: 0,
                self.window.checkbox11: True, self.window.checkbox12: True},

            2: {self.window.checkbox21: False, self.window.combobox_network: 0,
                self.window.checkbox22: False},

            3: {self.window.checkbox31: True, self.window.checkbox37: False,
                self.window.checkbox36: True, self.window.checkbox32: False,
                self.window.checkbox33: False, self.window.checkbox34: False,
                self.window.checkbox35: False, self.window.combobox_memores: 1},

            4: {self.window.checkbox41: False, self.window.checkbox42: False}
        }


class About(Widget):
    def __init__(self, main_window, *args):
        super().__init__(main_window, 940, 560, *args)
        self.window = main_window
        self.init_ui()

    def init_ui(self):
        tab = Widget(self, 830, 460)

        # Фреймы
        self.about_frame1 = Frame(tab, 360, 70, tag='base')
        self.about_frame1.move(220, 50)

        self.about_frame2 = Frame(tab, 360, 240, tag='base')
        self.about_frame2.move(220, 130)

        # Информация
        self.window.about_logo = Label(self.about_frame1, 300, 50)
        self.window.about_logo.set_image('logo_white.png', size=(300, 50))
        self.window.about_logo.move(30, 10)

        self.about_text = Label(self.about_frame2, 340, 200, tag='infa')
        self.about_text.setText(v.about)
        self.about_text.move(30, 20)


class Servers(Widget):
    def __init__(self, main_window, *args):
        super().__init__(main_window, 940, 560, *args)
        self.window = main_window
        self.init_ui()

    def init_ui(self):
        tab = Widget(self, 830, 460)

        # Виджеты
        self.window.serv_frame = Frame(tab, 590, 350, tag='base')
        self.window.serv_frame.move(140, 30)

        self.window.serv_add = Button(tab, 210, 40, text='Добавить', tag='cbutton')
        self.window.serv_add.set_function(partial(self.window.server_add))
        self.window.serv_add.move(330, 400)

        # Серверы
        self.window.serv1 = Frame(self.window.serv_frame, 540, 90, tag='base')
        self.window.serv1.move(25, 20)

        self.window.serv2 = Frame(self.window.serv_frame, 540, 90, tag='base')
        self.window.serv2.move(25, 130)

        self.window.serv3 = Frame(self.window.serv_frame, 540, 90, tag='base')
        self.window.serv3.move(25, 240)

        self.window.slots = (self.window.serv1, self.window.serv2, self.window.serv3)
        self.window._refresh_servers()

        self.window.serv_frame2 = Frame(tab, 590, 350, tag='base')
        self.window.serv_frame2.move(140, 30)
        self.window.serv_frame2.hide()

        # Текстовые метки
        self.serv_lab1 = Label(self.window.serv_frame2, 190, 30, tag='big')
        self.serv_lab1.move(40, 40)
        self.serv_lab1.setText('Название сервера:')

        self.serv_lab2 = Label(self.window.serv_frame2, 190, 30, tag='big')
        self.serv_lab2.move(40, 90)
        self.serv_lab2.setText('Иконка сервера:')

        self.serv_lab3 = Label(self.window.serv_frame2, 390, 30, tag='big')
        self.serv_lab3.move(40, 180)
        self.serv_lab3.setText('IP-адрес (Например mc.hypixel.net):')

        self.serv_lab4 = Label(self.window.serv_frame2, 390, 30, tag='big')
        self.serv_lab4.move(40, 230)
        self.serv_lab4.setText('Порт (Например 25565):')

        self.serv_lab5 = Label(self.window.serv_frame2, 390, 30, tag='big')
        self.serv_lab5.move(40, 280)
        self.serv_lab5.setText('Версия игры для подключения:')

        # Настройки
        self.window.serv_set1 = LineEdit(self.window.serv_frame2, 170, 36)
        self.window.serv_set1.move(370, 40)

        self.window.serv_set2 = ComboBox(self.window.serv_frame2, 170, 36)
        self.window.serv_set2.addItems(v.servers_icons.keys())
        self.window.serv_set2.move(370, 90)
        self.window.serv_set2.setCurrentIndex(0)

        self.window.serv_set3 = LineEdit(self.window.serv_frame2, 170, 36)
        self.window.serv_set3.move(370, 180)

        self.window.serv_set4 = LineEdit(self.window.serv_frame2, 170, 36)
        self.window.serv_set4.move(370, 230)

        self.window.serv_set5 = ComboBox(self.window.serv_frame2, 170, 36)
        self.window.serv_set5.addItems(get_versions(mp=False))
        self.window.serv_set5.move(370, 280)
        self.window.serv_set5.setCurrentIndex(0)


class Content(Widget):
    def __init__(self, main_window, *args):
        super().__init__(main_window, 940, 560, *args)
        self.window = main_window
        self.init_ui()

    def init_ui(self):
        tab = Widget(self, 830, 460)

        # Фреймы
        self.pk_frame = Frame(tab, 670, 380, tag='base')
        self.pk_frame.move(100, 60)

        self.window.combobox_pp = ComboBox(tab, 170, 36)
        self.window.combobox_pp.addItems(['Сборки', 'Моды', 'Шейдеры'])
        self.window.combobox_pp.currentIndexChanged.connect(self.window.change_content_tabs)
        self.window.combobox_pp.move(350, 10)

        self.window.tabs1 = StackedWidget(self.pk_frame, 670, 380)
        self.window.tabs1.move(0, 0)
        self.window.tabs1.show()

        self.pack1 = Widget(self, 830, 460)
        self.window.tabs1.addWidget(self.pack1)

        self.window.pk_frame1 = Frame(self.pack1, 630, 100, tag='base')
        self.window.pk_frame1.move(20, 20)

        self.window.pk_frame2 = Frame(self.pack1, 320, 215, tag='base')
        self.window.pk_frame2.move(20, 135)

        self.window.pk_frame3 = Frame(self.pack1, 290, 215, tag='base')
        self.window.pk_frame3.move(360, 135)

        # Виджеты
        self.pk_label5 = Label(self.window.pk_frame1, 50, 30)
        self.pk_label5.move(25, 366)

        self.box = Label(self.window.pk_frame1, 50, 50)
        self.box.set_image('box.png')
        self.box.move(25, 25)

        self.pk_label1 = Label(self.window.pk_frame1, 170, 24, tag='big')
        self.pk_label1.setText("Что такое сборки?")
        self.pk_label1.move(100, 10)

        self.pk_label2 = Label(self.window.pk_frame1, 520, 50, tag='infa')
        self.pk_label2.setText(v.text_modpacks)
        self.pk_label2.move(100, 36)

        self.pk_button0 = Button(self.window.pk_frame2, 260, 36, text='Скачать сборку на Modrinth',
                                 tag='cbutton')
        self.pk_button0.move(30, 40)
        self.pk_button0.set_function(lambda: open_site('https://modrinth.com/modpacks'))

        self.pk_button1 = Button(self.window.pk_frame2, 260, 36, text='Выбрать файл .mrpack',
                                 tag='cbutton')
        self.pk_button1.move(30, 90)
        self.pk_button1.set_function(lambda: mrpack_select(self.pk_label4))

        self.pk_button2 = Button(self.window.pk_frame2, 260, 36, text='Установить сборку',
                                 tag='cbutton')
        self.pk_button2.move(30, 140)
        self.pk_button2.set_function(self.window.mrpack_install)

        self.pk_label4 = Label(self.window.pk_frame3, 330, 68, tag='big')
        self.pk_label4.setText("Название сборки: ? \nВерсия игры: ? \nЗагрузчик: ?")
        self.pk_label4.move(60, 80)

        self.window.pack2 = Widget(self, 830, 460)
        self.window.tabs1.addWidget(self.window.pack2)

        self.window.m_frame_top = Frame(self.window.pack2, 650, 60, tag='base')
        self.window.m_frame_top.move(10, 10)

        self.window.m_frame_main = Frame(self.window.pack2, 650, 280, tag='base')
        self.window.m_frame_main.move(10, 80)

        # Верхний фрейм
        self.window.combobox_m2 = ComboBox(self.window.m_frame_top, 160, 40)
        self.window.combobox_m2.addItems(['forge', 'fabric'])
        self.window.combobox_m2.move(50, 10)

        self.window.combobox_m3 = ComboBox(self.window.m_frame_top, 160, 40)
        self.window.combobox_m3.addItems(v.game_versions)
        self.window.combobox_m3.move(240, 10)

        self.search = Button(self.window.m_frame_top, 100, 40, text='Поиск', tag='cbutton')
        self.search.set_function(self.window.get_mods)
        self.search.move(530, 10)

        # Главный контент
        layout = QGridLayout(self.window.m_frame_main)

        self.window.mbuttons = []

        for i in range(6):
            mbutton = Frame(self.window.m_frame_main, 200, 100, tag='base')
            mbutton.move(20, 20)

            mbutton.text = Label(mbutton, 180, 20, tag='big')
            mbutton.text.move(10, 10)
            mbutton.text.setText('...')

            mbutton.button = Button(mbutton, 130, 30, text='Скачать', tag='cbutton')
            mbutton.button.move(10, 40)

            self.window.mbuttons.append(mbutton)
            layout.addWidget(self.window.mbuttons[i], i // 2, i % 2)

        self.window.tabs1.setCurrentIndex(0)


class Accounts(Widget):
    def __init__(self, main_window, *args):
        super().__init__(main_window, 940, 560, *args)
        self.window = main_window
        self.init_ui()

    def init_ui(self):
        tab = Widget(self, 830, 460)

        # Фреймы
        self.frame_manager1 = Frame(tab, 290, 320, tag='base')
        self.frame_manager1.move(90, 60)

        self.frame_manager2 = Frame(tab, 340, 320, tag='base')
        self.frame_manager2.move(430, 60)

        # Левый фрейм
        self.label2 = Label(self.frame_manager1, 140, 25)
        self.label2.setText('Твой никнейм')
        self.label2.move(35, 30)

        self.window.textbox = LineEdit(self.frame_manager1, 170, 40)
        self.window.textbox.move(35, 60)

        self.window.button_m1 = Button(self.frame_manager1, 36, 40, tag='cbutton')
        self.window.button_m1.move(220, 60)
        self.window.button_m1.set_icon('add.png', (25, 25))
        self.window.button_m1.set_function(self.window.add_account)

        self.window.combobox_users2 = ComboBox(self.frame_manager1, 170, 40)
        self.window.combobox_users2.addItems(v.users.keys())
        self.window.combobox_users2.move(35, 150)
        self.window.combobox_users2.setCurrentIndex(0)

        self.button_m2 = Button(self.frame_manager1, 36, 40, tag='delete_button')
        self.button_m2.move(220, 150)
        self.button_m2.set_icon('delete.png', (25, 25))
        self.button_m2.set_function(self.window.delete_account)

        self.button_m4 = Button(self.frame_manager1, 220, 36, text="Вернуться обратно",
                                tag='cbutton')
        self.button_m4.move(35, 250)
        self.button_m4.set_function(lambda: self.window.open_tab('home'))

        # Правый фрейм с описанием
        self.label_title_m = Label(self.frame_manager2, 200, 40, tag='big')
        self.label_title_m.setText('Менеджер аккаунтов')
        self.label_title_m.move(30, 20)

        self.label_about_m = Label(self.frame_manager2, 340, 230, tag='infa')
        self.label_about_m.setText(v.text_accounts)
        self.label_about_m.move(30, 60)


class WebPlay(Widget):
    def __init__(self, main_window, *args):
        super().__init__(main_window, 940, 560, *args)
        self.window = main_window
        self.init_ui()

    def init_ui(self):
        tab = Widget(self, 830, 460)

        # Виджеты
        self.web_frame1 = Frame(tab, 330, 180, tag='base')
        self.web_frame1.move(70, 100)

        self.web_frame2 = Frame(tab, 330, 180, tag='base')
        self.web_frame2.move(440, 100)

        self.web_frame3 = Frame(tab, 700, 70, tag='base')
        self.web_frame3.move(70, 300)

        self.web_title1 = Label(self.web_frame1, 220, 40, tag='big')
        self.web_title1.setText("Об EaglerCraft")
        self.web_title1.move(30, 15)

        self.web_text1 = Label(self.web_frame1, 350, 120, tag='infa')
        self.web_text1.setText(v.text_web1)
        self.web_text1.move(30, 48)

        self.web_title2 = Label(self.web_frame2, 220, 40, tag='big')
        self.web_title2.setText("Как это работает?")
        self.web_title2.move(30, 15)

        self.web_text2 = Label(self.web_frame2, 280, 120, tag='infa')
        self.web_text2.setText(v.text_web2)
        self.web_text2.move(30, 48)

        self.window.checkBox_web = CheckBox(self.web_frame3, 320, 20)
        self.window.checkBox_web.setText("Офлайн версия EaglerCraft")
        self.window.checkBox_web.move(50, 25)

        self.web_button1 = Button(self.web_frame3, 180, 36, tag='play', cursor=True)
        self.web_button1.move(460, 16)
        self.web_button1.set_function(lambda: play_in_browser(self.window.checkBox_web.isChecked()))
        self.web_button1.setText('Играть!')


class Versions(Widget):
    def __init__(self, main_window, *args):
        super().__init__(main_window, 940, 560, *args)
        self.window = main_window
        self.init_ui()

    def init_ui(self):
        tab = Widget(self, 830, 460)

        self.vr_frame = Frame(tab, 360, 260, tag='base')
        self.vr_frame.move(220, 100)

        self.window.combobox_vr1 = ComboBox(self.vr_frame, 200, 36)
        self.window.combobox_vr1.addItems(v.game_versions_type.keys())
        self.window.combobox_vr1.currentIndexChanged.connect(self.window.update_list_versions)
        self.window.combobox_vr1.move(80, 30)

        self.window.combobox_vr2 = ComboBox(self.vr_frame, 200, 36)
        self.window.combobox_vr2.addItems(get_versions_list('vanilla'))
        self.window.combobox_vr2.move(80, 90)

        self.button_vr1 = Button(self.vr_frame, 220, 36, text="Выбрать", tag='cbutton')
        self.button_vr1.move(70, 160)
        self.button_vr1.set_function(self.window.select_version)

        self.button_vr2 = Button(self.vr_frame, 220, 36, text="Вернуться обратно", tag='cbutton')
        self.button_vr2.move(70, 210)
        self.button_vr2.set_function(lambda: self.window.open_tab('home'))


class Console(Widget):
    def __init__(self, main_window, *args):
        super().__init__(main_window, 940, 560, *args)
        self.window = main_window
        self.init_ui()

    def init_ui(self):
        tab = Widget(self, 830, 460)

        self.vr_frame4 = Frame(tab, 600, 320, tag='base')
        self.vr_frame4.move(115, 60)

        self.window.log_area = TextEdit(self.vr_frame4, 560, 280)
        self.window.log_area.setReadOnly(True)
        self.window.log_area.move(20, 20)

        self.window.update_logs()


class Socials(Widget):
    def __init__(self, main_window, *args):
        super().__init__(main_window, 940, 560, *args)
        self.window = main_window
        self.init_ui()

    def init_ui(self):
        tab = Widget(self, 830, 460)

        self.frame_home2 = Frame(tab, 390, 160, tag='base')
        self.frame_home2.move(220, 80)

        self.frame_home1 = Frame(tab, 390, 110, tag='base')
        self.frame_home1.move(220, 260)

        # Соцсети
        self.social1 = Button(self.frame_home2, 160, 36, tag='cbutton', text='Telegram ')
        self.social1.move(30, 20)
        self.social1.set_function(lambda: open_site('https://t.me/raylauncher'))
        self.social1.set_icon('i_telegram.png', (26, 26))
        self.social1.setStyleSheet(v.social_styles[0])

        self.social2 = Button(self.frame_home2, 160, 36, tag='cbutton', text='Вконтакте')
        self.social2.move(200, 20)
        self.social2.set_function(lambda: open_site('https://vk.com/raylauncher'))
        self.social2.set_icon('i_vk.png', (26, 26))
        self.social2.setStyleSheet(v.social_styles[1])

        self.social3 = Button(self.frame_home2, 160, 36, tag='cbutton', text='YouTube  ')
        self.social3.move(30, 65)
        self.social3.set_function(lambda: open_site('https://www.youtube.com/@vibe_optimist'))
        self.social3.set_icon('i_youtube.png', (26, 26))
        self.social3.setStyleSheet(v.social_styles[2])

        self.social4 = Button(self.frame_home2, 160, 36, tag='cbutton', text='Discord  ')
        self.social4.move(200, 65)
        self.social4.set_function(lambda: open_site('https://discord.gg/Z546FYmDmB'))
        self.social4.set_icon('i_discord.png', (26, 26))
        self.social4.setStyleSheet(v.social_styles[3])

        self.social5 = Button(self.frame_home2, 160, 36, tag='cbutton', text="Наш сайт ")
        self.social5.move(30, 110)
        self.social5.set_function(lambda: open_site('https://raylauncher.foo.ng'))
        self.social5.set_icon('i_site.png', (26, 26))
        self.social5.setStyleSheet(v.social_styles[4])

        self.social6 = Button(self.frame_home2, 160, 36, tag='cbutton', text="GitHub   ")
        self.social6.move(200, 110)
        self.social6.set_function(lambda: open_site('https://github.com/vibeOptimist/RayLauncher'))
        self.social6.set_icon('i_github.png', (26, 26))
        self.social6.setStyleSheet(v.social_styles[5])

        # Рекомендация
        self.reference_image = Label(self.frame_home1, 90, 90)
        self.reference_image.set_image('sleep_photo.png')
        self.reference_image.move(65, 10)

        self.reference_text = Label(self.frame_home1, 240, 42, tag='big')
        self.reference_text.setText("@SleepPhoto \nЛамповые фото")
        self.reference_text.move(170, 15)

        self.reference_button = Button(self.frame_home1, 140, 32, text="Перейти", tag='abutton')
        self.reference_button.move(170, 60)
        self.reference_button.set_function(lambda: open_site('https://t.me/SleepPhoto'))
