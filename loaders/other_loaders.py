import xlrd

from items.simple_items import MorileeItem
from loaders.base_loader import BaseLoader


class VoyageLoader(BaseLoader):
    def __init__(self):
        super().__init__()
        self.item_type = type(MorileeItem(None, None, None, None, None, None, None))
        self.collection = None

    def load(self, collection_name, rows, product_type):
        self.rows = rows
        self.items = []
        self.collection = collection_name
        for row in self.rows:
            if row[0].ctype == xlrd.biffh.XL_CELL_TEXT:
                self.items[-1].marketing_info = row[0].value
            else:
                self.items.append(
                    self.item_type(
                        style=str(row[0].value).replace('.0', ''),
                        comments=str(row[1].value),
                        uk_wholesale_price=float(row[2].value),
                        colours_available=str(row[3].value),
                        uk_size_range=str(row[4].value),
                        product_type=product_type,
                        collection=self.collection
                    )
                )
