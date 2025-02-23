from src.sites import SiteType

class Site:
    def __init__(self, x, y, type: SiteType):
        self.x = x
        self.y = y
        self.type = type