import xlrd

from items.simple_items import MorileeItem
from loaders.base_loader import BaseLoader
from loaders.colour_sets.mori_lee_colour_sets import *


class VoyageLoader(BaseLoader):
    def __init__(self):
        super().__init__()
        self.item_type = type(MorileeItem())

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


class ColourSetLoader(BaseLoader):
    def __init__(self):
        super().__init__()
        self.item_type = type(MorileeItem())

    def load(self, collection_name, rows, product_type):
        self.rows = rows
        self.collection = collection_name
        self.items = []
        for row in self.rows:
            if row[0].ctype == xlrd.biffh.XL_CELL_TEXT:
                self.items[-1].marketing_info = row[0].value
            else:

                # Hacky hack
                colour_set_text = str(row[2].value).lower()
                if colour_set_text.startswith('all solid'):
                    colour_set = [SOLID_LACE]
                elif colour_set_text.startswith('all satin colours'):
                    colour_set = [SATIN_AND_CHIFFON]
                elif colour_set_text.startswith('all chiffon colours'):
                    colour_set = [SATIN_AND_CHIFFON]
                elif colour_set_text.startswith('all jersey colours'):
                    colour_set = [JERSEY]
                elif colour_set_text.startswith('all tulle colours'):
                    colour_set = [TULLE]
                elif colour_set_text.startswith('all luxe chiffon colours'):
                    colour_set = [LUXE_CHIFFON]
                elif colour_set_text.startswith('all beaded chiffon colours'):
                    colour_set = [BEADED_CHIFFON_AND_BEADED_SATIN]
                elif colour_set_text.startswith('all beaded satin colours'):
                    colour_set = [BEADED_CHIFFON_AND_BEADED_SATIN]
                elif colour_set_text.startswith('all sequin mesh colours'):
                    colour_set = [SEQUIN_MESH]
                else:
                    raise ValueError("Not programmed to handle colour set '{}'".format(str(row[2].value)))

                self.items.append(
                    self.item_type(
                        style=str(row[0].value).replace('.0', ''),
                        uk_wholesale_price=float(row[1].value),
                        colour_set=colour_set,
                        uk_size_range=str(row[3].value),
                        product_type=product_type,
                        collection=self.collection
                    )
                )
