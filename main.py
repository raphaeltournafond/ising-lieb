from models.ising import Ising
from models.imager import Imager
import gc

ising = Ising()
images = 10
grid, energy, magnet = ising.metropolis(315, 2.229, 300, lieb=False, store_times=images)

imager = Imager()
imager.gif_from_grid(grid, images)
del grid
gc.collect()