import numpy as np
import random as rd
import math as m
import matplotlib.pyplot as plt
import sys

class Ising():
    grid: np.matrix
    kb: float
    J: int
    
    def __init__(self, kb=1) -> None:
        self.grid = None
        self.kb = kb
        self.J = 1
        pass
    
    def lieb(self, N):
        self.grid = np.random.choice([-1, 1], size=(N, N))
        rows, cols = self.grid.shape
        for i in range(rows):
            for j in range(cols):
                if i % 2 != 0 and j % 2 != 0:
                    self.grid[i, j] = 0
        
    def metropolis_step(self, T):
        # 2. Choisir un site j et proposer d’inverser le spin a cet endroit, c’est-a-dire sj -> -sj (si avec i =/= j reste inchange).
        i, j = self.find_random_spin()
        # 3. Calculer E = Eneuf - Eancien.
        delta = self.delta(i, j)
        # 4. Si E <= 0, garder le spin inverse et continuer `a 7.
        # 5. Si E > 0, calculer w = exp(E/(kB T)).
        if delta <= 0 or rd.random() <= m.exp(-delta / self.kb * T):
            self.grid[i, j] *= -1
        
    
    def metropolis(self, N, T, steps, fast=True, lieb=True, store_times=50):
        grid = None
        if steps >= store_times:
            # 1. Choisir un etat initial.
            if lieb:
                self.lieb(N)
            else:
                self.grid = np.random.choice([-1, 1], size=(N, N))

            grid = np.zeros((store_times, N, N), dtype=np.int8)
            energy = None
            magnet = None
            if not fast:
                energy = np.zeros((store_times, N, N), dtype=np.float32)
                magnet = np.zeros((store_times, N, N), dtype=np.float32)

            # Run simulation
            percentage = 0
            j = 0
            modulus = steps/store_times
            for i in range(steps):
                percentage = int(m.ceil((i/steps)*100))
                sys.stdout.write('\rComputing metropolis\t' + '.' * percentage + ' ' + str(percentage) + '%')
                self.metropolis_step(T)
                if i % modulus == 0:
                    grid[j] = self.grid
                    if not fast:
                        energy[j] = self.energy()
                        magnet[j] = self.magnetization()
                    j += 1
            sys.stdout.write('\n')

        return grid, energy, magnet

    def energy(self):
        E=0
        rows, cols = self.grid.shape
        for i in range(rows):
            for j in range(cols):
                E += -self.J * self.spin_e(i, j)
        return E / 2.0 / (rows*cols)

    def magnetization(self):
        rows, cols = self.grid.shape
        return np.sum(self.grid) / (rows*cols)

    def spin_e(self, i, j):
        rows, cols = self.grid.shape
        return self.grid[i, j] * (self.grid[(i+1)%rows, j] + self.grid[(i-1)%rows, j] + self.grid[i, (j+1)%cols] + self.grid[i, (j-1)%cols])
        
    def delta(self, i, j):
        return 2 * self.spin_e(i, j)
                    
    def find_random_spin(self):
        rows, cols = self.grid.shape
        i, j = rd.randint(0, rows-1), rd.randint(0, cols-1)
        while self.grid[i, j] == 0:
            i, j = rd.randint(0, rows-1), rd.randint(0, cols-1)
        return i, j
        
    def display(self):
        try:
            plt.imshow(self.grid, cmap='binary')
            plt.show()
        except:
            print('Grid is not initialized and can\'t be displayed')