from tensorforce import Agent, Environment
import matplotlib.pyplot as plt
import numpy as np
import math
import pickle
from tqdm import tqdm
episode_number=1500
average_over=20
# Pre-defined or custom environment
environment = Environment.create(
    environment='gym', level='LunarLander-v2')
'''
    Actions:
        Type: Discrete(4)
        Num   Action
        0     Do Nothing
        1     Fire Left Engine
        2     Fire Main Engine
        3     Fire Right Engine

    Observation: Box(-np.inf, np.inf, shape=(8,))

        Type: Box(8)
        Num     Observation
        0       (pos.x - VIEWPORT_W/SCALE/2) / (VIEWPORT_W/SCALE/2)
        1       (pos.y - (self.helipad_y+LEG_DOWN/SCALE)) / (VIEWPORT_H/SCALE/2)
        2       vel.x*(VIEWPORT_W/SCALE/2)/FPS
        3       vel.y*(VIEWPORT_H/SCALE/2)/FPS
        4       Lander Angle
        5       20.0*self.lander.angularVelocity/FPS
        6       Legs[0] Contact with ground
        7       Legs[1] Contact with gound

    Terminal State:
        abs(state[0]) >= 1.0

    Prohibitive Boundary:
       the boundary set around abs(state[0])=0.95
           when x position is greater than 0.05, action 3
           when x position is less than -0.05, action 1
       the angle at abs(22) 0.4 radius
'''
# Intialize reward record and set parameters

def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'valid') / w

length=np.zeros(episode_number)
measure_length=moving_average(length,average_over)

prohibition_parameter=[0,-5,-10,-15,-20,-25,-30]
prohibition_position=[0.1,0.3,0.5,0.7,0.9,0.95,0.99]

reward_record=np.zeros((len(prohibition_position),len(prohibition_parameter),len(measure_length)))
theta_threshold_radians=0.4


#plot results
color_scheme=['green','orange','red','blue','yellowgreen','magenta','cyan']
x=range(len(measure_length))
for i in range(len(prohibition_position)):
    plt.figure()
    plt.plot(x,reward_record_without,label='without prohibitive boundary',color='black')
    for j in range(len(prohibition_parameter)):
        plt.plot(x,reward_record[i][j],label='position '+str(prohibition_position[i])+' parameter '+str(prohibition_parameter[j]),color=color_scheme[j])
    plt.xlabel('episodes')
    plt.ylabel('reward')
    plt.legend(loc="upper left")
    plt.savefig('lander_with_angle_boundary_at_%s_plot.png' %prohibition_position[i])

pickle.dump( reward_record, open( "lander_angle_record.p", "wb"))
agent.close()
environment.close()