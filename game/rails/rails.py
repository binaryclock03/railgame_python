from game.rails.splines import Spline, SplineNode
from game.gameObject import GameObject
from game.rails.rail_id import Id1, Id2
import numpy as np

class RailNode():
    id:int
    node:SplineNode
    mode:int

    def __init__(self, pos):
        pos = np.array([int(pos[0]),int(pos[1])])
        self.id = Id1().from_pos(pos)
        self.node = SplineNode(pos)
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

    def __init__(self, id:int, node1:RailNode, node2:RailNode, unit_scale:float=1, max_allowable_curve:float= 1):
        self.id = id
        self.unit_scale = unit_scale
        self.max_allowable_curve = max_allowable_curve
        self.node_1=node1
        self.node_2=node2

        self.spline = Spline(self.node_1.node, self.node_2.node)
        self.spline.recalculate()
    
    def set_railnode_1(self, railnode:RailNode):
        self.node_1=railnode
    
    def set_railnode_2(self, railnode:RailNode):
        self.node_2=railnode

    def _draw(self, surface):
        self.spline.draw(surface)

class RailLayer():
    # internal vars
    rails_id_ob:dict = {}
    railnodes_id_ob:dict = {}

    railscale = 1

    ## Creating rails
    def create_rail1(self, pos1, pos2):
        node_1 = RailNode(pos1)
        node_2 = RailNode(pos2)

        id1 = Id1()
        id1.from_pos(pos1)
        id2 = Id1()
        id2.from_pos(pos2)

        if id1 in self.railnodes_id_ob.keys() or id2 in self.railnodes_id_ob.keys():
            print("[WARNING] Rail node already exists at this location!")
            return

        self.railnodes_id_ob.update({id1: node_1})
        self.railnodes_id_ob.update({id2: node_2})

        self._create_rail(id1, id2)

    def create_rail2(self, node_id:Id1, pos2):
        node_2 = RailNode(pos2)

        id2 = Id1().from_pos(pos2)

        if id2 in self.railnodes_id_ob.keys():
            print("[WARNING] Rail node already exists at this location!")
            return

        self.railnodes_id_ob.update({id2, node_2})

        self._create_rail(node_id, id2)

    def create_rail3(self, node_id1:Id1, node_id2:Id1):
        self._create_rail(node_id1, node_id2)

    def _create_rail(self, node_id1:Id1, node_id2:Id1):
        # create rail id using id2 to allow for the 2 ids to be store together
        rail_id = Id2()
        rail_id.from_pos([node_id1.as_pos(), node_id2.as_pos()])

        # create the rail object
        rail = Rail(rail_id, self.railnodes_id_ob.get(node_id1), self.railnodes_id_ob.get(node_id2), self.railscale)

        # put the rail object into the rails dict
        self.rails_id_ob.update({rail_id:rail})
    
    ## drawing
    def draw_rails(self, surface):
        for rail in self.rails_id_ob.values():
            rail.draw(surface)
