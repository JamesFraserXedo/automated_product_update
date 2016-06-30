from items.simple_items import *
from loaders.base_loader import BaseLoader


class MainLoader(BaseLoader):
    def __init__(self):
        super().__init__()
        self.item_type = type(MainItem(None, None, None, None))
        
        
class BluLoader(BaseLoader):
    def __init__(self):
        super().__init__()
        self.item_type = type(BluItem(None, None, None, None))


class AngelinaLoader(BaseLoader):    
    def __init__(self):
        super().__init__()
        self.item_type = type(AngelinaItem(None, None, None, None))


class JuliettaLoader(BaseLoader):    
    def __init__(self):
        super().__init__()
        self.item_type = type(JuliettaItem(None, None, None, None))


class VizcayaLoader(BaseLoader):    
    def __init__(self):
        super().__init__()
        self.item_type = type(VizcayaItem(None, None, None, None))


class SticksLoader(BaseLoader):    
    def __init__(self):
        super().__init__()
        self.item_type = type(SticksItem(None, None, None, None))


class PaparazziContLoader(BaseLoader):    
    def __init__(self):
        super().__init__()
        self.item_type = type(PaparazziContItem(None, None, None, None))


class AbmLoader(BaseLoader):
    def __init__(self):
        super().__init__()
        self.item_type = type(AbmItem(None, None, None, None))
   

class TulleAffairsLoader(BaseLoader):
    def __init__(self):
        super().__init__()
        self.item_type = type(TulleAffairsItem(None, None, None, None))


class AffairsLoader(BaseLoader):
    def __init__(self):
        super().__init__()
        self.item_type = type(AffairsItem(None, None, None, None))


class AfAbmLoader(BaseLoader):
    def __init__(self):
        super().__init__()
        self.item_type = type(AfAbmItem(None, None, None, None))
