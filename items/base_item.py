class BaseItem(object):

    def __init__(self, style, uk_wholesale_price, colours_available, colour_set, uk_size_range, collection, product_type, marketing_info=None, comments=None):
        self.style = style
        self.uk_wholesale_price = uk_wholesale_price
        self.colours_available = colours_available
        self.colour_set = colour_set
        self.uk_size_range = uk_size_range
        self.collection = collection
        self.product_type = product_type
        self.marketing_info = marketing_info
        self.comments = comments

    @property
    def size_lower(self):
        return str(self.uk_size_range).split("-")[0].strip()

    @property
    def size_upper(self):
        return str(self.uk_size_range).split("-")[1].strip()

    def __repr__(self):
        return str(self.__dict__)