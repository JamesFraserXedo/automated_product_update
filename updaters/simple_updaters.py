from updaters.base_updater import BaseUpdater


class MorileeUpdater(BaseUpdater):
    def __init__(self):
        super().__init__()
        self.driver = None
        self.customer_code = 'morilee'