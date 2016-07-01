from items.simple_items import *
from loaders.base_loader import BaseLoader


class MainLoader(BaseLoader):
    def __init__(self):
        super().__init__()
        self.item_type = type(MainItem(None, None, None, None))
        self.collection = 'Mori Lee Bridal'
        
        
class BluLoader(BaseLoader):
    def __init__(self):
        super().__init__()
        self.item_type = type(BluItem(None, None, None, None))
        self.collection = 'Blu Bridal'


class AngelinaLoader(BaseLoader):    
    def __init__(self):
        super().__init__()
        self.item_type = type(AngelinaItem(None, None, None, None))
        self.collection = 'Angelina Faccenda Bridal'


class JuliettaLoader(BaseLoader):    
    def __init__(self):
        super().__init__()
        self.item_type = type(JuliettaItem(None, None, None, None))
        self.collection = 'Julietta'


class VizcayaLoader(BaseLoader):    
    def __init__(self):
        super().__init__()
        self.item_type = type(VizcayaItem(None, None, None, None))
        self.collection = 'Vizcaya'


class SticksLoader(BaseLoader):    
    def __init__(self):
        super().__init__()
        self.item_type = type(SticksItem(None, None, None, None))
        self.collection = ''


class PaparazziContLoader(BaseLoader):    
    def __init__(self):
        super().__init__()
        self.item_type = type(PaparazziContItem(None, None, None, None))
        self.collection = ''


class AbmLoader(BaseLoader):
    def __init__(self):
        super().__init__()
        self.item_type = type(AbmItem(None, None, None, None))
        self.collection = ''
   

class TulleAffairsLoader(BaseLoader):
    def __init__(self):
        super().__init__()
        self.item_type = type(TulleAffairsItem(None, None, None, None))
        self.collection = 'Tulle Affairs'


class AffairsLoader(BaseLoader):
    def __init__(self):
        super().__init__()
        self.item_type = type(AffairsItem(None, None, None, None))
        self.collection = 'Affairs'


class AfAbmLoader(BaseLoader):
    def __init__(self):
        super().__init__()
        self.item_type = type(AfAbmItem(None, None, None, None))
        self.collection = ''
