from game.rails.splines import Spline, SplineNode
from game.rails.rails import RailLayer
import pygame as pg
import numpy as np
from game.rails.action import Action

class RailPlacer():
    action:Action
    rail_layer:RailLayer

    last_point:np.array = None
    direction:np.array = None

    hover_spline:Spline

    def __init__(self, rail_layer:RailLayer, action:Action):
        self.action = action
        self.rail_layer = rail_layer

    def mouse_button_down_eventhandler(self, splines):
        if self.action.get_action() == "spline_first_point":
            print("Created first spline point")
            self.last_point = pg.mouse.get_pos()
            self.action.update_action("spline_second_point")
            self.hover_spline = Spline(SplineNode(pg.mouse.get_pos()), SplineNode(pg.mouse.get_pos()))

        elif self.action.get_action() == "spline_second_point":
            print("[DEBUG] Created Rail")
            point_temp = pg.mouse.get_pos()

            self.hover_spline.node_1.position = np.array(point_temp)

            if not self.direction is None:
                #splines.append(Spline(SplineNode(self.last_point), SplineNode(point_temp), d1=self.direction))
                self.rail_layer.create_rail1(self.last_point, point_temp)
            else:
                #splines.append(Spline(SplineNode(self.last_point), SplineNode(point_temp)))
                self.rail_layer.create_rail1(self.last_point, point_temp)
            #splines[-1].recalculate()
            if pg.key.get_mods() & pg.KMOD_SHIFT:
                self.action.update_action("spline_second_point")
                self.last_point = point_temp
                #d2 = -splines[-1].get_d2()
                #self.direction = d2
            else:
                self.action.update_action("none")
                self.direction = None
                self.last_point = None

    def draw_hoverspline(self, screen):
        if self.action.get_action() == "spline_second_point":
            if not self.direction is None: self.hover_spline.set_d1(self.direction)
            self.hover_spline.node_2.position = np.array(pg.mouse.get_pos())
            self.hover_spline.mode = 1
            self.hover_spline.recalculate()
            self.hover_spline.draw(screen)