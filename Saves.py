from pickle import dump, load


def save(parameters):
    with open('saves/save.zs', 'wb') as game_save:
        dump(parameters, game_save)
        game_save.close()


def load_settings():
    try:
        with open('saves/save.zs', 'rb') as game_save:
            game_save.close()
            return load(game_save)
    except FileNotFoundError:
        return False

