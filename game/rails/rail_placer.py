from game.rails.splines import Spline, SplineNode
from game.rails.rails import RailLayer
import pygame as pg
import numpy as np
from game.rails.action import Action

class RailPlacer():
    action:Action
    rail_layer:RailLayer

    last_point:np.array = None

    hover_spline:Spline

    def __init__(self, rail_layer:RailLayer, action:Action):
        self.rail_layer = rail_layer
        self.action = action

    def mouse_button_down_eventhandler(self, splines):
        snap_distance = 20

        if self.action.get_action() == "spline_first_point":
            print("[DEBUG] Begining building rails")

            # get position of click
            self.last_point = pg.mouse.get_pos()

            # check if node already exists within the snap distance
            for id in self.rail_layer.railnodes_id_ob.keys():
                if((self.last_point[0] - id.as_pos()[0])**2 + (self.last_point[1] - id.as_pos()[1])**2) < (snap_distance)**2:
                    print("[DEBUG] Found an already existing node")
                    self.last_point = id.as_pos()

            # set action to second point mode
            self.action.update_action("spline_second_point")

            # update / create hover spline
            self.hover_spline = Spline(SplineNode(self.last_point), SplineNode(self.last_point))

        elif self.action.get_action() == "spline_second_point":
            print("[DEBUG] Created rail section")
            point_temp = pg.mouse.get_pos()

            # check if node already exists within the snap distance
            for id in self.rail_layer.railnodes_id_ob.keys():
                if((point_temp[0] - id.as_pos()[0])**2 + (point_temp[1] - id.as_pos()[1])**2) < (snap_distance)**2:
                    print("[DEBUG] Found an already existing node")
                    point_temp = id.as_pos()

            self.hover_spline.node_1.position = np.array(point_temp)

            self.rail_layer.create_rail(self.last_point, point_temp)

            if pg.key.get_mods() & pg.KMOD_SHIFT:
                self.action.update_action("spline_second_point")
                self.last_point = point_temp
            else:
                print("[DEBUG] Finished building rails")
                self.action.update_action("none")
                self.last_point = None

    def draw_hoverspline(self, screen):
        if self.action.get_action() == "spline_second_point":
            self.hover_spline.node_2.position = np.array(pg.mouse.get_pos())
            self.hover_spline.mode = 1
            self.hover_spline.recalculate()
            self.hover_spline.draw(screen)