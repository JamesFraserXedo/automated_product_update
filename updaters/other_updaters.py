from updaters.base_updater import BaseUpdater


class VoyageUpdater(BaseUpdater):
    def __init__(self):
        super().__init__()
        self.driver = None
        self.customer_code = 'morilee'