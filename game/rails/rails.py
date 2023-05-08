from game.rails.splines import Spline, SplineNode
from game.gameObject import GameObject
from game.rails.rail_id import Id1, Id2
import numpy as np

class RailNode():
    id:int
    node:SplineNode
    p_attached_rails:list = []
    s_attached_rails:list = []

    def __init__(self, pos):
        pos = np.array([int(pos[0]),int(pos[1])])
        self.id = Id1()
        self.id.from_pos(pos)
        self.node = SplineNode(pos)
    
    def get_dir(self) -> np.array:
        return self.p_attached_rails[0].spline.get_d2()

    def get_mode(self) -> int:
        return len(self.p_attached_rails)

    def attach_rail(self, rail):
        print("test")
        if len(self.p_attached_rails) >= 2:
            self.s_attached_rails.append(rail)
        else:
            self.p_attached_rails.append(rail)
    
    def remove_rail(self, rail):
        if rail in self.p_attached_rails:    pass
        elif rail in self.s_attached_rails:  pass

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

        if self.node_1.get_mode() > 1: d1 = self.node_1.get_dir()
        else: d1 = None
        if self.node_2.get_mode() > 1: d2 = self.node_2.get_dir()
        else: d2 = None

        print(self.node_1.get_mode())
        print(self.node_1.p_attached_rails)
        print(d1)
        print(d2)
        
        self.spline = Spline(self.node_1.node, self.node_2.node, d1, d2)
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
    def create_rail(self, in1, in2):
        if not in1 is RailNode: node_1 = RailNode(in1)
        if not in2 is RailNode: node_2 = RailNode(in2)

        id1 = node_1.id
        id2 = node_2.id

        id1_match, id2_match = False, False
        for id in self.railnodes_id_ob.keys():
            if id1 == id: id1_match = True
            if id2 == id: id2_match = True
                
        if not id1_match: 
            print("creating new node")
            self.railnodes_id_ob.update({id1: node_1})
        if not id2_match: 
            print("creating new node")
            self.railnodes_id_ob.update({id2: node_2})

        self._create_rail(id1, id2)

    def _create_rail(self, node_id1:Id1, node_id2:Id1):
        # create rail id using id2 to allow for the 2 ids to be store together
        rail_id = Id2()
        rail_id.from_pos([node_id1.as_pos(), node_id2.as_pos()])

        node_1 = self.railnodes_id_ob.get(node_id1)
        node_2 = self.railnodes_id_ob.get(node_id2)

        # create the rail object
        rail = Rail(rail_id, node_1, node_2, self.railscale)

        node_1.attach_rail(rail)
        node_2.attach_rail(rail)

        # put the rail object into the rails dict
        self.rails_id_ob.update({rail_id:rail})
    
    ## drawing
    def draw_rails(self, surface):
        for rail in self.rails_id_ob.values():
            rail.draw(surface)