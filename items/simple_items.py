from items.base_item import BaseItem


class MorileeItem(BaseItem):

    def __init__(self, style, uk_wholesale_price, colours_available, uk_size_range, collection, product_type, comments=None):
        super().__init__(style, uk_wholesale_price, colours_available, uk_size_range, collection, product_type, comments)