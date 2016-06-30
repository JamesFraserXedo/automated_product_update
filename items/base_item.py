class BaseItem(object):

    def __init__(self, style, uk_wholesale_price, colours_available, uk_size_range, marketing_info=None):
        self.style = style
        self.uk_wholesale_price = uk_wholesale_price
        self.colours_available = colours_available
        self.uk_size_range = uk_size_range
        self.marketing_info = marketing_info

    def __repr__(self):
        return str({
            "style": self.style,
            "uk_wholesale_price": self.uk_wholesale_price,
            "colours_available": self.colours_available,
            "uk_size_range": self.uk_size_range,
            "marketing_info": self.marketing_info
        })