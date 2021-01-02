from tensorforce import Agent, Environment
import matplotlib.pyplot as plt
import numpy as np
import math
import pickle
from tqdm import tqdm
from Normal import episode_number
from Normal import average_over
from Normal import evaluation_episode_number
from Normal import exploration
from Normal import measure_length
from Normal import moving_average
from Normal import prohibition_parameter
from Normal import prohibition_position
from Normal import environment

kp=40
kd=2.27645649
#training with coaching
reward_record_average=np.zeros((len(prohibition_position),len(prohibition_parameter),len(measure_length)))
reward_record=np.zeros((len(prohibition_position),len(prohibition_parameter),episode_number))
evaluation_reward_record=np.zeros((len(prohibition_position),len(prohibition_parameter),evaluation_episode_number))


for k in range(len(prohibition_position)):
    #training
    for i in range(len(prohibition_parameter)):
        record=[]
        velocity_batch=[0]
        agent = Agent.create(agent='agent.json', environment=environment)
        print('training agent with boundary position at %s and prohibitive parameter %s' %(prohibition_position[k],prohibition_parameter[i]))
        for _ in tqdm(range(episode_number)):
            episode_reward=0
            states = environment.reset()
            terminal = False
            count=0
            positive=0
            consecutive=[0]
            cons_position=0

            while not terminal:
                velocity_old=velocity_batch[count]
                count+=1
                theta=states[1]
                angular_velocity=states[3]
                velocity_batch.append(angular_velocity)

                if abs(angular_velocity)<=prohibition_position[k]:
                    if angular_velocity*velocity_old>0:
                        old_count=consecutive[cons_position]
                        consecutive.append(count)
                        cons_position+=1
                        if old_count==count-1:
                            #print('count %s difference %s' %(count,(abs(theta)-abs(theta_old))))
                            positive+=1
                        else:
                            positive=1
                            #print('count %s difference %s' %(count,(abs(theta)-abs(theta_old))))

                    if positive==3:
                        positive=0
                        actions=kp*theta+kd*angular_velocity
                        print('intervention:',actions)
                        states, terminal, reward = environment.execute(actions=actions)
                        if terminal == True:
                            episode_reward=0
                            states = environment.reset()
                            terminal = False
                            count=0
                            positive=0
                            consecutive=[0]
                            cons_position=0
                            break
                
                actions = agent.act(states=states)
                states, terminal, reward = environment.execute(actions=actions)
                agent.observe(terminal=terminal, reward=reward)
                episode_reward+=reward
            record.append(episode_reward)
        reward_record[k][i]=record
        temp=np.array(record)
        reward_record_average[k][i]=moving_average(temp,average_over)


        #evaluate
        episode_reward = 0.0
        eva_reward_record=[]
        print('evaluating agent with boundary position at %s and prohibitive parameter %s' %(prohibition_position[k],prohibition_parameter[i]))
        for j in tqdm(range(evaluation_episode_number)):
            episode_reward=0
            states = environment.reset()
            internals = agent.initial_internals()
            terminal = False
            while not terminal:
                actions, internals = agent.act(states=states, internals=internals, independent=True, deterministic=True)
                states, terminal, reward = environment.execute(actions=actions)
                episode_reward += reward
            eva_reward_record.append(episode_reward)
        evaluation_reward_record[k][i]=eva_reward_record
        agent.close()
#save data
pickle.dump(reward_record, open( "record.p", "wb"))
pickle.dump(reward_record_average, open( "average_record.p", "wb"))
pickle.dump(evaluation_reward_record, open( "evaluation_record.p", "wb"))
environment.close()