class drawable:
    def __init__(self, surf, rect):
        self.rect = rect
        self.surface = surf
    def copy(self):
        return drawable(self.surface.copy(), self.rect.copy())