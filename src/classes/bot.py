class Bot(object):
    """
    Singleton Bot class, keeps information regarding game states
    and players
    """
    _instance = None

    def __init__(self):
        if not Class._instance:
            _instance = Bot()
        else:
            raise RuntimeError('Only one instance of Bot is allowed!')
