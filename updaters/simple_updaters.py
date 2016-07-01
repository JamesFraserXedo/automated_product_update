from updaters.base_updater import BaseUpdater


class MainUpdater(BaseUpdater):
    def __init__(self):
        super().__init__()
        self.driver = None
        self.customer_code = 'morilee'


class BluUpdater(BaseUpdater):
    def __init__(self):
        super().__init__()
        self.driver = None
        self.customer_code = 'morilee'