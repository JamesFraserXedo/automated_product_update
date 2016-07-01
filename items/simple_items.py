from items.base_item import BaseItem


class MainItem(BaseItem):

    def __init__(self, style, uk_wholesale_price, colours_available, uk_size_range):
        super().__init__(style, uk_wholesale_price, colours_available, uk_size_range)


class BluItem(BaseItem):

    def __init__(self, style, uk_wholesale_price, colours_available, uk_size_range):
        super().__init__(style, uk_wholesale_price, colours_available, uk_size_range)


class AngelinaItem(BaseItem):

    def __init__(self, style, uk_wholesale_price, colours_available, uk_size_range):
        super().__init__(style, uk_wholesale_price, colours_available, uk_size_range)


class JuliettaItem(BaseItem):

    def __init__(self, style, uk_wholesale_price, colours_available, uk_size_range):
        super().__init__(style, uk_wholesale_price, colours_available, uk_size_range)


class VizcayaItem(BaseItem):

    def __init__(self, style, uk_wholesale_price, colours_available, uk_size_range):
        super().__init__(style, uk_wholesale_price, colours_available, uk_size_range)


class SticksItem(BaseItem):

    def __init__(self, style, uk_wholesale_price, colours_available, uk_size_range):
        super().__init__(style, uk_wholesale_price, colours_available, uk_size_range)


class PaparazziContItem(BaseItem):

    def __init__(self, style, uk_wholesale_price, colours_available, uk_size_range):
        super().__init__(style, uk_wholesale_price, colours_available, uk_size_range)


class AbmItem(BaseItem):

    def __init__(self, style, uk_wholesale_price, colours_available, uk_size_range):
        super().__init__(style, uk_wholesale_price, colours_available, uk_size_range)


class TulleAffairsItem(BaseItem):

    def __init__(self, style, uk_wholesale_price, colours_available, uk_size_range):
        super().__init__(style, uk_wholesale_price, colours_available, uk_size_range)


class AffairsItem(BaseItem):

    def __init__(self, style, uk_wholesale_price, colours_available, uk_size_range):
        super().__init__(style, uk_wholesale_price, colours_available, uk_size_range)


class AfAbmItem(BaseItem):

    def __init__(self, style, uk_wholesale_price, colours_available, uk_size_range):
        super().__init__(style, uk_wholesale_price, colours_available, uk_size_range)


class VoyageItem(BaseItem):

    def __init__(self, style, comments, uk_wholesale_price, colours_available, uk_size_range):
        super().__init__(style, uk_wholesale_price, colours_available, uk_size_range)
        self.comments = comments
