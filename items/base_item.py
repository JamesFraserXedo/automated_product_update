class BaseItem(object):

    def __init__(self, style, uk_wholesale_price, colours_available, uk_size_range, collection, product_type, marketing_info=None, comments=None):
        self.style = style
        self.uk_wholesale_price = uk_wholesale_price
        self.colours_available = colours_available
        self.uk_size_range = uk_size_range
        self.collection = collection
        self.product_type = product_type
        self.marketing_info = marketing_info
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