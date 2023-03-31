from models.ising import Ising
from models.imager import Imager

ising = Ising()
grid, energy, magnet = ising.metropolis(137, 2.229, 100000)

imager = Imager()
imager.gif_from_grid(grid, 50)
