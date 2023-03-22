import numpy as np
import random as rand
import opensimplex as opsim
import multiprocessing as mp
import utility as ut

class Terrain:
    def __init__(self, shape_chunks: tuple, resolution: int, seed: int = -1, sea_level = 0.5):
        
        self.world_map_res = resolution

        self._sea_level = sea_level
        self._beach_length = 0.001

        self._shape_chunks = shape_chunks

        if seed == -1:
            self._seed = rand.randint(0, 99999)
        else:
            self._seed = seed

        self._heightmap = HeightMap(shape_chunks, resolution)
        self._terrain_generator = TerrainGenerator(self._seed)

    def generate_world_map(self):
        for x in range(self._shape_chunks[0]):
            for y in range(self._shape_chunks[1]):
                generated_chunk = self.generate_chunk((x,y))
                self._heightmap.set_chunk((x,y), generated_chunk)

    def set_seed(self, seed:int):
        self._seed = seed
        self._terrain_generator = TerrainGenerator(self._seed)

    def generate_chunk(self, coords: tuple):
        return self._terrain_generator.generate_chunk(coords, self.world_map_res)

    def get_world_map_image(self):
        hmap_arr = self._heightmap.get_heightmap_array()

        sea_bool = (hmap_arr <= self._sea_level)
        beach_bool = np.logical_and(hmap_arr > self._sea_level, hmap_arr <= (self._sea_level + self._beach_length))
        mountain_bool = (hmap_arr > 0.8)
        land_bool = np.logical_and(hmap_arr > self._sea_level + self._beach_length, hmap_arr < 0.8)

        sea_colors = [(0, 0, 100),(0, 50, 255)]
        beach_colors = [(234, 204, 31),(214, 184, 11)]
        mountain_colors = [(150,150,150),(255,255,255)]
        land_colors = [(0, 100, 0),(0, 255, 0)]

        sea         = ut.color_grad_arr(hmap_arr, 0, self._sea_level,                       sea_colors[0], sea_colors[1], enable_arr = sea_bool.astype(int))
        beach       = ut.color_grad_arr(hmap_arr, self._sea_level, self._sea_level+self._beach_length,    beach_colors[0], beach_colors[1], enable_arr = beach_bool.astype(int))
        mountain    = ut.color_grad_arr(hmap_arr, 0.8, 1,                                   mountain_colors[0], mountain_colors[1], enable_arr = mountain_bool.astype(int))
        land        = ut.color_grad_arr(hmap_arr, self._sea_level + self._beach_length, 0.8,              land_colors[0], land_colors[1], enable_arr = land_bool.astype(int))

        image = sea + beach + mountain + land
        return np.array(image)



class TerrainGenerator:
    def __init__(self, seed:int):
        opsim.seed(seed)

        self.noise_params = [[0.1, 0.1], [0.5, 0.1], [1, 0.1], [4, 0.01], [6, 0.01]]

    def generate_chunk(self, coords: tuple, resolution: int):
        coords = (coords[0] * resolution, coords[1] * resolution)
        chunk_coords = np.array((np.arange(coords[0], coords[0]+resolution),np.arange(coords[1], coords[1]+resolution)))
        chunk = np.zeros((resolution, resolution))
        for noise in self.noise_params:
            chunk += opsim.noise2array((noise[0] * chunk_coords[0]) / 100, (noise[0] * chunk_coords[1]) / 100) * noise[1]
        chunk = ut.rescale(chunk, -1, 1, 0, 1)
        return np.transpose(chunk)



class HeightMap:
    def __init__(self, shape_chunks, resolution):
        self._heightmap = np.zeros((shape_chunks[0] * resolution, shape_chunks[1] * resolution))
        self._chunk_res = resolution
        self._shape_chunks = shape_chunks

    def to_tuple_coords(self, coords: int or tuple) -> tuple:
        if type(coords) is tuple:
            pass
            return (coords[0] * self._chunk_res, coords[1] * self._chunk_res)
        pass
        return coords % (self._shape_chunks[0] * self._chunk_res), coords // (self._shape_chunks[0] * self._chunk_res) 

    def get_chunk(self, coords: int or tuple):
        x, y = self.to_tuple_coords(coords)
        return self._heightmap[x:x+self._chunk_res, y:y+self._chunk_res]

    def set_chunk(self, coords: int or tuple, chunk: np.array):
        x, y = self.to_tuple_coords(coords)
        self._heightmap[x:x+self._chunk_res, y:y+self._chunk_res] = chunk

    def get_heightmap_array(self):
        return self._heightmap