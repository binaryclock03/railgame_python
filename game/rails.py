from game.splines import Spline, SplineNode
from game.gameObject import GameObject
import game.rail_id
import numpy as np

class RailNode():
    id:int
    node:SplineNode
    mode:int

    def __init__(self, id, position):
        self.id = id
        self.node = SplineNode(position)
        self.mode = 0
    
    def get_dir(self) -> np.array:
        pass


class Rail(GameObject):
    id:int
    unit_scale:float

    length:float
    max_curve:float
    
    node_1:RailNode
    node_2:RailNode

    spline:Spline

    def __init__(self, id:int, unit_scale:float=1, max_allowable_curve:float= 1):
        self.id = id
        self.unit_scale = unit_scale
        self.max_allowable_curve = max_allowable_curve
    
    def set_railnode_1(self, railnode:RailNode):
        self.node_1=railnode
    
    def set_railnode_2(self, railnode:RailNode):
        self.node_2=railnode

    def _draw(self, surface):
        pass

class RailLayer():
    # internal vars
    rails_id_ob:dict = {}
    railnodes_id_ob:dict = {}

    railscale = 1

    ## Creating rails
    def create_rail1(self, pos1, pos2):
        pass

    def create_rail2(self, node_id:int, pos):
        pass

    def create_rail3(self, node_id1:int, node_id2:int):
        self._create_rail(node_id1, node_id2)

    def _create_rail(self, node_id1:int, node_id2:int):
        # create rail id using id2 to allow for the 2 ids to be store together
        rail_id = game.rail_id.Id2()
        rail_id.id1 = node_id1
        rail_id.id2 = node_id2

        # create the rail object
        rail = Rail(self.railscale, 1)

        # set the nodes of the rail object
        rail.set_railnode_1(self.railnodes_id_ob.get(node_id1))
        rail.set_railnode_2(self.railnodes_id_ob.get(node_id2))

        # put the rail object into the rails dict
        self.rails_id_ob.update({rail_id:rail})
    
    ## drawing
    def draw_rails(self, surface):
        for rail in self.railnodes_id_ob.values():
            rail.draw(surface)
