from pickle import dump, load


def save(parameters):
    # Функция сохранения прогресса в файл
    with open('saves/save.zs', 'wb') as game_save:
        dump(parameters, game_save)
        game_save.close()


def load_settings():
    # Функция загрузки сохранения при выборе опции продолжения игры
    try:
        with open('saves/save.zs', 'rb') as game_save:
            return load(game_save)
    except FileNotFoundError:
        return False

