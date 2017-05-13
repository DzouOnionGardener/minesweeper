# Initial framework for minesweeper
from gym.spaces import Discrete
from gym.spaces.tuple_space import Tuple
from gym.spaces import seed
import numpy as np
import random
import sys

class Minefield(object):
    UNKNOWN = -1
    MINE = -99

    def __init__(self, rows=8, cols=8, mines=10):
        seed()                  # Initialize RNG
        self.action_space = Tuple((Discrete(rows),Discrete(cols)))
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.nonMines = rows*cols - mines
        self.clickedCoords = set()
        self.letter_Axis = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t']
        self.chosenCoords = []
        self.state = np.full([self.rows, self.cols], Minefield.UNKNOWN)
        self.neighboring_mines = 0
    def reset(self):
        # Internal state: where are all the mines?
        self.mine_coords = set()
        mines_to_place = self.mines
        while mines_to_place > 0:
            r = random.randrange(self.rows)
            c = random.randrange(self.cols)
            if (r, c) not in self.mine_coords:  # new coord
                self.mine_coords.add((r, c))
                mines_to_place -= 1
        print("SECRET locations:", self.mine_coords)
        self.state = np.full([self.rows, self.cols], Minefield.UNKNOWN)
        self.coords_to_clear = self.rows * self.cols - self.mines
        return self.state
    
    def step(self, coord):
        reward = 0
        done = False
        self.coord = coord
        if self.state[coord] != Minefield.UNKNOWN:
            reward = -2
        elif coord in self.mine_coords:
            # Clicked on a mine!
            self.state[coord] = Minefield.MINE
            reward = Minefield.MINE # -99
            done = True
        else:
            self.neighboring_mines = 0
            for r in range(coord[0]-1, coord[0]+2):
                for c in range(coord[1]-1, coord[1]+2):
                    if r >= 0 and c >= 0:
                        if (r,c) in self.mine_coords:
                            self.neighboring_mines += 1
            self.state[coord] = self.neighboring_mines
            self.neighboring_mines = 0
            self.coords_to_clear -= 1
            if self.coords_to_clear == 0:
                reward = 50     # Yay you won.
                done = True
            else:
                reward = 1
        return (self.state, reward, done, None)

    def render(self):
        for x in range(self.rows):
            sys.stdout.write(self.letter_Axis[x])
            for y in range(self.cols):
                if self.state[x][y] == -99:                  
                    sys.stdout.write(' x')
                elif self.state[x][y] == -1:                  
                    sys.stdout.write(' .')
                elif self.state[x][y] != -1:
                    sys.stdout.write(' %s' % int(self.state[x][y]))
                if y != self.cols-1:
                    sys.stdout.write(' ')
                    if y == (self.cols - 1):
                        sys.stdout.write('\n')
            sys.stdout.write('\n')
        sys.stdout.write(' ')
        for k in range(self.cols):
            sys.stdout.write(' %s ' % k)
        print ""

    def conCoord(self, userInput):
        # rows x cols
        self.cc = userInput
        firstVal = self.letter_Axis[self.cc[0]]
        x = str(firstVal)
        y = str(self.cc[1])
        xy = x + y
        return xy
if __name__ == "__main__":
    from constraints import Constraints
    constraints = Constraints()
    env = Minefield()
    obs = env.reset()
    env.render()
    done = False
    total = 0
    clicked = []
    while not done:

        act = input('Pick a coordinate: ')
        ##act = env.action_space.sample()
        obs, reward, done, info = env.step(act)
        total += reward
        if not done:
            # Add the fact to the constraint DB.
            neighbors = []
            for r in range(act[0]-1, act[0]+2):
                for c in range(act[1]-1, act[1]+2):
                    if (r,c) != act:
                        neighbors.append((r,c))
            constraints.add(obs[act], neighbors)
            Queue = constraints.getQue()
            if len(Queue) != 0:
                for x in Queue:
                    if x[0] >= 0 and x[1] >= 0 and x[0]<= 7 and x[1] <= 7:  ##prevents out of bounds : (-1, 0), (8, 0) and so on
                        act = x
                        obs, reward, done, info = env.step(act)
            constraints.ClearQue()
        ##this prints the value print obs[act]
        print(act, reward, done)
        print "visited %s" % clicked
        constraints.show()
        print
        env.render()
    print("Game over, total is", total)
