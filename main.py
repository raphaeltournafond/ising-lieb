from models.ising import Ising
from models.imager import Imager

ising = Ising()
grid, energy, magnet = ising.metropolis(151, 2.229, 300000)

imager = Imager()
imager.gif_from_grid(grid, 30)