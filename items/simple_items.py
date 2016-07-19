from items.base_item import BaseItem


class MorileeItem(BaseItem):

    def __init__(self, style=None, uk_wholesale_price=None, colours_available=None, colour_set=None, uk_size_range=None, collection=None, product_type=None, comments=None):
        super().__init__(style, uk_wholesale_price, colours_available, colour_set, uk_size_range, collection, product_type, comments)