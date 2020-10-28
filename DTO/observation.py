class Observation:
    def __init__(self, kind, area, distance_to=None):
        self.kind = kind
        self.area = area
        self.d_to = distance_to
    
    # Requires to be implemented in order to be used in a PriorityQueue
    def __eq__(self, other):
        return True
        