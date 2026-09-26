# Константы цветов
GRADIENTS = (
    ('#2A5E38', '#809C35'),
    ('#244532', '#5E862D'),
    ('#794778', '#C084AA'),
    ('#577AA4', '#8FAFC4'),
    ('#4B3F6F', '#836999'),
    ('#0073AA', '#40CCEF'),
    ('#91461F', '#7E2539'),
    ('#935234', '#AD7643')
)

SOCIAL_COLORS = [
    ("#398aa3", "#37788c", "#128bb0", "#0f7796"),
    ("#3964a3", "#30548a", "#1553b0", "#124796"),
    ("#a32e49", "#8a273e", "#c21b42", "#a81839"),
    ("#4752c4", "#3c45a5", "#3c45a5", "#2d3486"),
    ("#ad5b2b", "#995026", "#cf6121", "#ba571e"),
    ("#1b1a1c", "#0a090a", "#201e21", "#0c0c0d"),
]

# Дефолтные json-данные
DEFAULT_SETTINGS = {
    "design": {
        "theme": "dark",
        "loading": [1, ""],
        "launcher": [1, ""],
        "button_web_play": True,
        "animation": True
    },
    "parameters": {
        "button_black": False,
        "network_check": 0,
        "incognito": False
    },
    "minecraft": {
        "path": "",
        "memory": 4,
        "hide_in_game": True,
        "files_log4j": False,
        "lock_multiplayer": False,
        "lock_chat": False,
        "demo": False,
        "show_all_versions": False,
        "show_modpacks": True
    },
    "java": {
        "my_java": False,
        "my_path": "",
        "console_show": False
    }
}

DEFAULT_CONFIG = {
    "launcher_run": False,
    "clean_step": 0,
    "user": "",
    "version": ""
}
