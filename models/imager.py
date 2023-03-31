import imageio
import matplotlib.pyplot as plt

class Imager():
    images_index: list

    def __init__(self) -> None:
        self.images_index = []
        pass

    def create_frame(self, grid, t):
        plt.imshow(grid, cmap='binary')
        plt.title(f't = {t}', fontsize=14)
        plt.savefig(f'./images/img_{t}.png', 
            transparent = False,  
            facecolor = 'white'
            )
        plt.close()
        self.images_index.append(t)

    def create_gif(self):
        frames = []
        for f in self.images_index:
            image = imageio.v2.imread(f'./images/img_{f}.png')
            frames.append(image)

        imageio.mimsave('./images/animation.gif', # output gif
                frames,          # array of input frames
                fps = 25)         # optional: frames per second

    def gif_from_grid(self, grid, nb_img = 100):
        imager = Imager()
        steps = len(grid) // nb_img
        i = 0
        while i < len(grid):
            imager.create_frame(grid[i], i)
            for _ in range(steps):
                i += 1

        imager.create_gif()