from items.simple_items import *
from loaders.base_loader import BaseLoader


class MoriLeeLoader(BaseLoader):
    def __init__(self):
        super().__init__()
        self.item_type = type(MorileeItem(None, None, None, None, None, None))