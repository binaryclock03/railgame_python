import numpy as np

#MUST BE A MUTLIPLE OF 2
ID_STR_LEN = 8
class Id1():
    '''A special kind of Id class that gives some usefull functions for dealing with node Ids'''
    id1:int

    def __str__(self):
        return str(self.id1).zfill(ID_STR_LEN)
    
    def as_pos(self):
        x = round(self.id1/10**(ID_STR_LEN/2))
        y = self.id1 - x*10**(ID_STR_LEN/2)
        return np.array([x, y])
    
    def from_pos(self, pos):
        if pos is list: pos = np.array(pos)
        
        # if len(pos[0]) > ID_STR_LEN/2 or len(pos[1]) > ID_STR_LEN/2:
        #     print("[WARNING] inputed positions too large for current ID_STR_LEN, will continue with errors")

        self.id1 = pos[0]*10**(ID_STR_LEN/2) + pos[1]

class Id2():
    '''A speical kind of Id class that allows two ids to be easily handeled for rails'''
    id1:int
    id2:int

    def __str__(self):
        '''returns self as string with "<id2><id1>" with size <ID_STR_LEN><ID_STR_LEN>'''
        return str(self.id2).zfill(ID_STR_LEN) + str(self.id1).zfill(ID_STR_LEN)

    def as_pos(self):
        '''returns the id as a set of positions for node1 and node2'''
        x1 = round(self.id1/10**(ID_STR_LEN/2))
        y1 = self.id1 - x1*10**(ID_STR_LEN/2)
        x2 = round(self.id1/10**(ID_STR_LEN/2))
        y2 = self.id1 - x2*10**(ID_STR_LEN/2)
        return np.array([[x1, y1],[x2, y2]])
    
    def from_pos_1(self, pos):
        '''defines internal id1 from the given point'''
        if pos is list: pos = np.array(pos)
        
        # if len(pos[0]) > ID_STR_LEN/2 or len(pos[1]) > ID_STR_LEN/2:
        #     print("[WARNING] inputed positions for pos 1 too large for current ID_STR_LEN, will continue with errors")

        self.id1 = pos[0]*10**(ID_STR_LEN/2) + pos[1]
    
    def from_pos_2(self, pos):
        '''defines internal id2 from the given point'''
        if pos is list: pos = np.array(pos)
        
        # if len(pos[0]) > ID_STR_LEN/2 or len(pos[1]) > ID_STR_LEN/2:
        #     print("[WARNING] inputed positions for pos 2 too large for current ID_STR_LEN, will continue with errors")

        self.id1 = pos[0]*10**(ID_STR_LEN/2) + pos[1]
    
    def from_pos(self, poses):
        '''defines internal ids from the given points'''
        self.from_pos_1(poses[0])
        self.from_pos_2(poses[1])