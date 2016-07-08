import xlrd


class BaseLoader:

    def __init__(self):
        self.rows = None
        self.items = []
        self.collection = None

    def load(self, collection_name, rows, product_type):
        self.rows = rows
        self.collection = collection_name
        self.items = []
        for row in self.rows:
            if row[0].ctype == xlrd.biffh.XL_CELL_TEXT:
                self.items[-1].marketing_info = row[0].value
            else:
                self.items.append(
                    self.item_type(
                        style=str(row[0].value).replace('.0', ''),
                        uk_wholesale_price=float(row[1].value),
                        colours_available=str(row[2].value),
                        uk_size_range=str(row[3].value),
                        product_type=product_type,
                        collection=self.collection
                    )
                )