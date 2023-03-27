import numpy as np
import pygame as pg
from CONSTANTS import BLACK
import math

class Spline():
    def __init__(self, node_1, node_2, d1=None, d2=None, id=0) -> None:
        # set basic variables
        self.id = id
        self.node_1 = node_1
        self.node_2 = node_2
        self.floating_node = None
        self.a = 2/3

        # mode setting
        if d1 is None and d2 is None:   self.mode = 2
        elif d2 is None:                self.mode = 3
        else:                           self.mode = 4

        # casting inputs to np arrays
        if not d1 is None:  self._d1 = normalize(np.array(d1))
        else:               self._d1 = None
        
        if not d2 is None:  self._d2 = normalize(np.array(d2))
        else:               self._d2 = None

        # recalculate spline
        self.recalculate()

        # render spline
        self.render()
    
    def recalculate(self):
        self._P0 = np.array(self.node_1.position)
        self._P3 = np.array(self.node_2.position)

        if (self._d1 is None and self._d2 is None) or (np.linalg.norm(self._P3 - self._P0) <= 1):
            self._d1 = self._P3 - self._P0
            if not np.linalg.norm(self._d1) == 0: self._d1 = self._d1/np.linalg.norm(self._d1)
            else: self._d1 = np.array((0.01,0))

        elif self.mode == 3:
            theta = math.asin(self._d1[1])

            print("angle of D1: " + str(theta))

            c = math.cos(theta)
            s = math.sin(theta)

            TM = np.array(((c, -s), 
                           (s,  c)))

            d1x = np.matmul(self._d1, TM)[0]
            d1y = np.matmul(self._d1, TM)[1]
            P0x = np.matmul(self._P0, TM)[0]
            P0y = np.matmul(self._P0, TM)[1]
            P3x = np.matmul(self._P3, TM)[0]
            P3y = np.matmul(self._P3, TM)[1]
            p3x = np.matmul(self._P3, TM)[0]
            p3y = np.matmul(self._P3, TM)[1]

            r   = -(-p3x**2+2*p3x*P0x-P0x**2+2*p3y*P0y-p3y**2-P0y**2)/(2*(-p3y+P0y))
            a_2 = math.acos((P0y-P3y-r)/-r)

            print("radius: " + str(r))
            print("angle:  " + str(a_2))

            t_col = (-P0x**2-P0y**2-P3x**2-P3y**2+2*P0x*P3x+2*P0y*P3y)/(2*(P0x*d1x-P3x*d1x+P0y*d1y-P3y*d1y))

            self.a = ((d1x*t_col)**2+(d1y*t_col)**2)**0.5 * (2/3)

            self._d2 = self._d1 + ((self._P0 - self._P3)/t_col)

        self.P1 = self._P0 + np.array(self._d1) * self.a

        if self._d2 is None:
            self.P2 = self._P3 - np.array(self._d1) * self.a
        else:
            self.P2 = self._P3 + np.array(self._d2) * self.a

    def render(self):
        # we can greatly speed this up if we can develop a matrix operation instead of itterating over t
        points = []
        for t in np.linspace(0, 1, 101):
            points.append((1-t)**3*self._P0 + 3*(1-t)**2*t*self.P1 + 3*(1-t)*t**2*self.P2 + t**3*self._P3)

        self.points = points

    def set_d1(self, d1):
        if d1 is None: self._d1 = None
        else: self._d1 = np.array(d1)
    
    def set_d2(self, d2):
        if d2 is None: self._d2 = None
        else: self._d2 = np.array(d2)
    
    def get_d2(self):
        if self._d2 is None:
            return -self._d1
        else:
            return self._d2
    
    def get_d1(self):
        return self._d1

    def draw(self, surface):
        pg.draw.aalines(surface, BLACK, False, self.points)

class Spline2():
    def __init__(self, node_1, node_2, d1=None, d2=None, id=0) -> None:
        self.id:int = id
        
        self.node_1:SplineNode = node_1
        self.node_2:SplineNode = node_2

        self.set_d1(d1)
        self.set_d2(d2)

        if d2 is None:
            if d1 is None:  self.mode = 1
            else:           self.mode = 2
        else:               self.mode = 3

        print(f"Mode: {self.mode}")

        self.recalculate()
        #self.render()
       
    def recalculate(self):
        if self.mode == 2:
            if self._d1[0] >= 0: theta =          -math.asin(self._d1[1])
            else:                theta = (np.pi) + math.asin(self._d1[1])
            
            c = math.cos(theta)
            s = math.sin(theta)
            TM = np.array(((c, -s), 
                           (s,  c)))
            
            print("----------------------------")
            print(f"D1 pre: {self._d1}")
            print(f"D1 mag: {np.linalg.norm(self._d1)}")
            print(f"Theta: {theta}")
            d1 = np.matmul(TM, self._d1)
            print(f"D1: {d1}")
            

            P0  = np.matmul(TM, self.node_1.position)
            P0x = P0[0]
            P0y = P0[1]
            P3  = np.matmul(TM, self.node_2.position)
            P3x = P3[0]
            P3y = P3[1]

            if (P3x - P0x) <= 0:
                P3[0] = P0x
                P3x = P0x

            print(f"P1L: {P0}")
            print(f"P3L: {P3}")

            self.radius = -(-P3x**2+2*P3x*P0x-P0x**2+2*P3y*P0y-P3y**2-P0y**2)/(2*(-P3y+P0y))

            if (P3x - P0x) <= 0: self.angle = np.deg2rad(180)
            else:                self.angle = abs(math.acos((P0y-P3y-self.radius)/-self.radius))

            r_sign = abs(self.radius)/self.radius
            d2 = np.array((-math.cos(self.angle * r_sign), math.sin(self.angle * r_sign)))
            
            print(f"D2: {d2}")
            print("--")
            print("radius: " + str(self.radius))
            print("angle:  " + str(np.rad2deg(self.angle)))

            a = abs(self.radius) * (6.823804635335345e-8 * np.rad2deg(abs(self.angle))**3 -5.662094427708215e-6 * np.rad2deg(abs(self.angle))**2 + 0.006129092971602482 * np.rad2deg(abs(self.angle)) + -0.0044854458177779515)

            c = math.cos(-theta)
            s = math.sin(-theta)
            TM = np.array(((c, -s), 
                           (s,  c)))

            d1 = np.matmul(TM, d1)
            d2 = np.matmul(TM, d2)
            self._d2 = d2
            P0 = self.node_1.position
            P3 = np.matmul(TM, P3)
            self.node_2.position = P3

        elif self.mode == 3:
            pass

        else:
            P0 = self.node_1.position
            P3 = self.node_2.position

            self.set_d1(self.node_2.position - self.node_1.position)
            self.set_d2(self.node_1.position - self.node_2.position)

            d1 = self._d1
            d2 = self._d2

            a = 1

        P1 = P0 + d1 * a
        P2 = P3 + d2 * a

        print(f"P0: {P0}")
        print(f"P1: {P1}")
        print(f"P2: {P2}")
        print(f"P3: {P3}")
        print(f"a:  {a}")

        points = []
        for t in np.linspace(0, 1, 101):
            points.append((1-t)**3*P0 + 3*(1-t)**2*t*P1 + 3*(1-t)*t**2*P2 + t**3*P3)

        self.points = points

    def render(self):
        pass
        
    def set_d1(self, d1):
        if d1 is None:  
            self._d1    = None
            self._d1m   = 0
        else:       
            self._d1 = normalize(np.array(d1))    
            self._d1m = np.linalg.norm(np.array(d1))
    
    def set_d2(self, d2):
        if d2 is None:  
            self._d2    = None
            self._d2m   = 0
        else:       
            self._d2  = normalize(np.array(d2))    
            self._d2m = np.linalg.norm(np.array(d2))
    
    def get_d2(self):
        return self._d2
    
    def get_d1(self):
        return self._d1

    def draw(self, surface):
        pg.draw.aalines(surface, BLACK, False, self.points)

class SplineNode():
    def __init__(self, position:tuple) -> None:
        self.position = np.array(position)

class Rail(Spline):
    pass

def normalize(vector):
    return vector/np.linalg.norm(vector)

#Spline2(SplineNode((100,100)), SplineNode((200,200)), d1=(0,1))