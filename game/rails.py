from splines import Spline, SplineNode
from gameObject import GameObject

class RailNode():
    node:SplineNode

    def __init__(self, position):
        self.node = SplineNode(position)

class Rail(GameObject):
    length:float
    max_curve:float
    
    node_1:RailNode
    node_2:RailNode

    spline:Spline

    def __init__(self):
        self.max_allowable_curve = -1;
