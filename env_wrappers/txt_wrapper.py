import sys
from PIL import Image
from PIL import ImageTk
import numpy as np
from PIL import Image
import tkinter
import scipy.ndimage
import scipy.misc

class GridWorld:
    def __init__(self, load_path=None):
        self.rewardFunction = None
        self.nb_actions = 4
        if load_path != None:
            self.read_file(load_path)

        self.agentX, self.agentY = self.startX, self.startY
        self.nb_states = self.nb_rows * self.nb_cols

        self.win = tkinter.Toplevel()

        screen_width = self.win.winfo_screenwidth()
        screen_height = self.win.winfo_screenheight()

        # calculate position x and y coordinates
        x = screen_width + 100
        y = screen_height + 100

        self.win.geometry('+%d+%d' % (200, 200))
        self.win.title("Gridworld")

    def render(self):
        mdp_screen = np.array(self.MDP)
        mdp_screen = np.expand_dims(mdp_screen, 2)
        mdp_screen[mdp_screen == -1] = 255
        mdp_screen = np.tile(mdp_screen, [1, 1, 3])
        mdp_screen[self.agentX, self.agentY] = [0, 0, 255]
        mdp_screen[self.goalX, self.goalY] = [255, 0, 0]
        screen = scipy.misc.imresize(mdp_screen, [200, 200, 3], interp='nearest')
        screen = Image.fromarray(screen, 'RGB')
        screen = screen.resize((512, 512))

        self.win.geometry('%dx%d' % (screen.size[0], screen.size[1]))

        tkpi = ImageTk.PhotoImage(screen)
        label_img = tkinter.Label(self.win, image=tkpi)
        label_img.place(x=0, y=0,
                        width=screen.size[0], height=screen.size[1])

        # self.win.mainloop()            # wait until user clicks the window
        self.win.update_idletasks()
        self.win.update()

    def read_file(self, load_path):
        with open(load_path, "r") as f:
            lines = f.readlines()
        self.nb_rows, self.nb_cols = lines[0].split(',')
        self.nb_rows, self.nb_cols = int(self.nb_rows), int(self.nb_cols)
        self.MDP = np.zeros((self.nb_rows, self.nb_cols))
        lines = lines[1:]
        for i in range(self.nb_rows):
            for j in range(self.nb_cols):
                if lines[i][j] == '.':
                    self.MDP[i][j] = 0
                elif lines[i][j] == 'X':
                    self.MDP[i][j] = -1
                elif lines[i][j] == 'S':
                    self.MDP[i][j] = 0
                    self.startX = i
                    self.startY = j
                else: # 'G'
                    self.MDP[i][j] = 0
                    self.goalX = i
                    self.goalY = j

    def get_state_index(self, x, y):
        idx = y + x * self.nb_cols
        return idx

    def get_initial_state(self):
        agent_state_index = self.get_state_index(self.startX, self.startY)
        self.agentX, self.agentY = self.startX, self.startY
        return agent_state_index

    def get_next_state(self, a):
        action = ["up", "right", "down", "left", 'terminate']
        nextX, nextY = self.agentX, self.agentY

        if action[a] == 'terminate':
            return -1, -1


        if self.MDP[self.agentX][self.agentY] != -1:
            if action[a] == 'up' and self.agentX > 0:
                nextX, nextY = self.agentX - 1, self.agentY
            elif action[a] == 'right' and self.agentY < self.nb_cols - 1:
                nextX, nextY = self.agentX, self.agentY + 1
            elif action[a] == 'down' and self.agentX < self.nb_rows - 1:
                nextX, nextY = self.agentX + 1, self.agentY
            elif action[a] == 'left' and self.agentY > 0:
                nextX, nextY = self.agentX, self.agentY - 1

        if self.MDP[nextX][nextY] != -1:
            return nextX, nextY
        else:
            return self.agentX, self.agentY

    def is_terminal(self, nextX, nextY):
        if nextX == self.goalX and nextY == self.goalY:
            return True
        else:
            return False

    def get_next_reward(self, nextX, nextY):
        if self.rewardFunction is None:
            if nextX == self.goalX and nextY == self.goalY:
                reward = 1
            else:
                reward = 0
        else:
            currStateIdx = self.get_state_index(self.agentX, self.agentY)
            nextStateIdx = self.get_state_index(nextX, nextY)

            reward = self.rewardFunction[nextStateIdx] \
                     - self.rewardFunction[currStateIdx]

        return reward

    def get_state_xy(self, idx):
        y = idx % self.nb_cols
        x = int((idx - y) / self.nb_rows)

        return x, y

    def get_next_state_and_reward(self, currState, a):
        if currState == self.nb_states:
            return currState, 0

        tmpx, tmpy = self.agentX, self.agentY
        self.agentX, self.agentY = self.get_state_xy(currState)
        nextX, nextY = self.agentX, self.agentY

        nextStateIdx = None
        reward = None

        nextX, nextY = self.get_next_state(a)
        if nextX != -1 and nextY != -1:  # If it is not the absorbing state:
            reward = self.get_next_reward(nextX, nextY)
            nextStateIdx = self.get_state_index(nextX, nextY)
        else:
            reward = 0
            nextStateIdx = self.nb_states

        self.agentX, self.agentY = tmpx, tmpy

        return nextStateIdx, reward

    def step(self, a):
        nextX, nextY = self.get_next_state(a)

        self.agentX, self.agentY = nextX, nextY

        done = False
        if self.is_terminal(nextX, nextY):
            done = True

        reward = self.get_next_reward(nextX, nextY)
        nextStateIdx = self.get_state_index(nextX, nextY)

        return nextStateIdx, reward, done

    def get_action_set(self):
        return range(0, 3)

    def define_reward_function(self, vector):
        self.rewardFunction = vector
