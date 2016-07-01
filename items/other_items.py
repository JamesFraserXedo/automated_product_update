from items.base_item import BaseItem


class VoyageItem(BaseItem):

    def __init__(self, style, comments, uk_wholesale_price, colours_available, uk_size_range, collection):
        super().__init__(style, uk_wholesale_price, colours_available, uk_size_range, collection)
        self.comments = comments

    def __repr__(self):
        return str({
            "style": self.style,
            "comments": self.comments,
            "uk_wholesale_price": self.uk_wholesale_price,
            "colours_available": self.colours_available,
            "uk_size_range": self.uk_size_range,
            "collection": self.collection,
            "marketing_info": self.marketing_info
        })