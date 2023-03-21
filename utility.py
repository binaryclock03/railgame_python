import math
import numpy as np

def rescale(value, min_value, max_value, min_new, max_new, enable = 1):
    return ((value-min_value) * ((max_new-min_new)/(max_value-min_value)) + min_new) * enable

def ramp_up(x, ramp_len, ramp_start=0):
    return (-0.5 * math.cos(((math.pi)/(ramp_len)) * (x-ramp_start)) + 0.5)

def ramp_down(x, ramp_len, ramp_end=0):
    return -(-0.5 * math.cos(((math.pi)/(ramp_len)) * (x-ramp_end+ramp_len)) + 0.5)+1

def color_grad(value, color_start: tuple, color_end: tuple) -> tuple:
    r = rescale(value, -1, 1, color_start[0], color_end[0])
    g = rescale(value, -1, 1, color_start[1], color_end[1])
    b = rescale(value, -1, 1, color_start[2], color_end[2])
    return (r, g, b)

def color_grad_arr(arr, min_val, max_val, color_start: tuple, color_end: tuple, enable_arr = -1):
    if type(enable_arr) is int:
        enable_arr = np.ones(arr.shape)

    out = np.zeros((arr.shape[0], arr.shape[1], 3))
    out[:,:,0] = rescale(arr, min_val, max_val, color_start[0], color_end[0], enable=enable_arr)
    out[:,:,1] = rescale(arr, min_val, max_val, color_start[1], color_end[1], enable=enable_arr)
    out[:,:,2] = rescale(arr, min_val, max_val, color_start[2], color_end[2], enable=enable_arr)
    return out

    