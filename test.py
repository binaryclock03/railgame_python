import terrain2
import time

if __name__ == "__main__":
    terrain = terrain2.Terrain((100,100), 4)

    time1 = time.time()
    terrain.generate_world_map()
    time2 = time.time()
    print(time2 - time1)

    time1 = time.time()
    terrain.get_world_map_image()
    time2 = time.time()
    print(time2 - time1)