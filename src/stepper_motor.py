#! /usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class StepperMotor:
    def __init__(self, increment, speed):
        self.increment = increment
        self.speed = speed

        self.time = [0.0]
        self.position = [0.0]
        self.velocity = [0.0]

        self.h = 0.001

        self.Kp = 160.0
        self.Kd = 100.0

        self.e_prev = 0.0

        self.target_position = [-increment]
        self.target = 0.0

        self.counter = 0

    def set_target(self, target):
        self.target = target

    def show(self, tf=1):
        self.fig = plt.figure()
        self.ax = plt.axes(xlim=(0, tf), ylim=(0, 1))
        self.ax.grid(True)
        self.line, = self.ax.plot([], [], color="teal", label="position réelle")
        self.command_line, = self.ax.plot([], [], color="crimson", label="position commandée")
        self.target_line, = self.ax.plot([], [], '--', color="purple", label="position cible")
        anim = animation.FuncAnimation(self.fig, self.step, frames=int(tf/self.h), interval=self.h, blit=True)
        plt.xlabel(r"Temps (en $s$)")
        plt.ylabel(r"Angle de l'arbre moteur (en $rad$)")
        plt.legend(loc="lower right")
        plt.show()

    def step(self, i):
        if i % 100 == 0 and self.counter < 10:
            self.set_target(self.target_position[-1] + self.increment)
            self.counter += 1
        e = self.target - self.position[-1]
        cmd = self.Kp * e + self.Kd * (e - self.e_prev) / self.h
        self.e_prev = e

        self.time.append(self.time[-1] + self.h)
        self.target_position.append(self.target)
        self.velocity.append(self.velocity[-1] + self.h * cmd)
        self.position.append(self.position[-1] + self.h * self.velocity[-1])

        self.line.set_data(self.time, self.position)
        self.command_line.set_data(self.time, 0.95*np.ones(len(self.position)))
        self.target_line.set_data(self.time, self.target_position)

        return self.target_line, self.line, self.command_line

if __name__ == "__main__":
    sm = StepperMotor(0.1, 1)
    sm.set_target(0.1)
    sm.show()