class Observation:
    def __init__(self, kind, rect, distance_to=None):
        self.kind = kind
        self.rect = rect
        self.d_to = distance_to
    
    def __eq__(self, other):
        return True
        