import pygame as pg
from pygame import transform
import perlin_noise as pn
import utility as ut
import numpy as np
import random as rand
import opensimplex as opsim

class Terrain:
    def __init__(self):
        self._size_chunks = (100, 50)
        self._seed = rand.randint(1,99999)
        self._sealevel = 0.43

        self._world_map_resolution = 4

        self._island_ramp = 5 #in chunks

        self._countour_image = []
        self._reset_world_map_heightmap()
    
    def set_world_size(self, size_chunks):
        self._size_chunks = size_chunks
        self._reset_world_map_heightmap()

    def get_world_size(self):
        return self._size_chunks

    def set_seed(self, seed: int):
        if seed == -1:
            seed = rand.randint(1,99999)
        self._seed = seed
    
    def get_seed(self) -> int:
        return self._seed

    def set_sealevel(self, numb):
        self._sealevel = numb
        self.convert_heightmap_to_mapimage()

    def _reset_world_map_heightmap(self):
        self._world_map_heightmap = np.zeros((self._size_chunks[0], self._size_chunks[1], 4, 4))
        self._reset_world_map_image()
        
    def _reset_world_map_image(self):
        self._image = np.zeros((self._size_chunks[0] * 4, self._size_chunks[1] * 4, 3))

    # def generate_chunk(self, chunk_coords, resolution = 4, insert_to_map = False):
    #     opsim.seed(self.get_seed())

    #     if type(chunk_coords) is int:
    #         chunk_coords = (chunk_coords % self._size_chunks[0] , chunk_coords // self._size_chunks[0])

    #     coords = np.arange(chunk_coords[0]* self._world_map_resolution, (chunk_coords[0]* self._world_map_resolution) + resolution), np.arange(chunk_coords[1], chunk_coords[1] + resolution)

    #     generated_chunk = opsim.noise2array(coords[0]/(self._size_chunks[0]* self._world_map_resolution), coords[1]/(self._size_chunks[1]* self._world_map_resolution))

    #     generated_chunk = ut.rescale(np.transpose(generated_chunk), -1, 1, 0, 1)
    #     # generated_chunk = np.transpose(generated_chunk)

    #     if insert_to_map == True:
    #         self._world_map_heightmap[chunk_coords[0]][chunk_coords[1]] = generated_chunk
        
    #     return generated_chunk    

    def generate_chunk(self, chunk_coords, resolution = 2, insert_to_map = False):
        if type(chunk_coords) is int:
            chunk_coords = (chunk_coords % self._size_chunks[0] , chunk_coords // self._size_chunks[0])
        #world standard size is 400x200 chunks, rough chunk res is 2x2
        #print("chunk: " + str(chunk_coords))

        noise_size = max(resolution * self._size_chunks)/( 100)

        noise1 = pn.PerlinNoise(octaves=1*(noise_size), seed=self.get_seed())
        noise2 = pn.PerlinNoise(octaves=2*(noise_size), seed=self.get_seed())
        noise3 = pn.PerlinNoise(octaves=4*(noise_size), seed=self.get_seed())
        noise4 = pn.PerlinNoise(octaves=8*(noise_size), seed=self.get_seed())

        coords = (chunk_coords[0] * resolution, chunk_coords[1] * resolution)
        generated_chunk = []

        for i in range(0, resolution):
            row = []
            for j in range(0, resolution):

                pos = [(i+coords[0])/(self._size_chunks[0]*resolution), (j+coords[1])/(self._size_chunks[1]*resolution)]

                noise_val =  0.6 * noise1(pos)
                noise_val += 0.2 * noise2(pos)
                noise_val += 0.1 * noise3(pos)
                noise_val += 0.1 * noise4(pos)
    
                noise_val = ut.rescale(noise_val, -1, 1, 0, 1)
                row.append(noise_val)
        
            generated_chunk.append(row)

        if insert_to_map == True:
            self._world_map_heightmap[chunk_coords[0]][chunk_coords[1]] = generated_chunk
        
        return generated_chunk
        
    
    def convert_heightmap_to_mapimage(self):
        self._reset_world_map_image()
        for chunk_y, chunk_column in enumerate(self._world_map_heightmap):
            for chunk_x, chunk in enumerate(chunk_column):
                
                sea_level = self._sealevel

                # chunk_sea_bool = (chunk >= sea_level).astype(int)

                # red_channel = np.zeros(chunk.shape)
                # green_channel = chunk_sea_bool * ut.rescale(chunk, sea_level, 1, 50, 255)
                # blue_channel = (chunk_sea_bool * -1 + 1) * ut.rescale(chunk, 0, sea_level, 50, 255)

                # sub_image = np.array([red_channel, green_channel, blue_channel])
                # sub_image = np.transpose(sub_image)
                
                # self._image[(chunk_x * 4):((chunk_x * 4) + 4), (chunk_y * 4):((chunk_y * 4) + 4)] = sub_image

                # pass
                for y in range(len(chunk)):
                    for x in range(len(chunk[0])):
                        if chunk[x][y] >= sea_level:
                            self._image[(chunk_x * len(chunk)) + x, (chunk_y * len(chunk)) + y, 1] = ut.rescale(chunk[x][y], sea_level, 1, 50, 255)
                        else:
                            self._image[(chunk_x * len(chunk)) + x, (chunk_y * len(chunk)) + y, 2] = ut.rescale(chunk[x][y], 0, sea_level, 50, 255)
    
    def convert_heightmap_to_countourmap_image(self, resolution = 2):

        self._image= np.ones((self._size_chunks[0] * resolution, self._size_chunks[1] * resolution, 3)) * 255

        for countour_line in np.linspace(0, 1, 100):
            for chunk_x, chunk_column in enumerate(self._world_map_heightmap):
                for chunk_y, chunk, in enumerate(chunk_column):

                    for x in range(len(chunk)):
                        for y in range(len(chunk[0])):
                            if chunk[x][y] >= countour_line and chunk[x][y] <= countour_line + 0.0025:
                                self._image[(chunk_x * 2) + x, (chunk_y * 2) + y] = (0,0,0)


    def draw_worldmap(self, screen, x, y, scale = 1):
        image = self._image
        surf = pg.surfarray.make_surface(image)
        surf = transform.scale(surf, (800,800))
        screen.blit(surf, (x, y))

    def draw_chunk(self, screen, x, y, scale = 1):
        pass