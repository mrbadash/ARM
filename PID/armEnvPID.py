#armBrain

import serial
import random
import numpy as np


class armEnv:
#armEnv mimics the environment of an openAI gym environment
#Uses the same functions, such as gym.make, except it will be armEnv.make
#should be scalable to the size of the arm and all
#Created by Ash Robbins
#****************************************************

  def __init__(self):
  
    pass
    
  def make(self):
    #Open Serial port for data transferring
    print('Searching for Serial...')
    self.ser = serial.Serial('COM4', 57600)
    print('Serial Connected')
    
    #For the velocity observation
    self.velocity = 0
    self.lastZ = 0
    self.z = 0
    self.velocityAverage = 0
    
    
    
    #Currently there is 1 action, which is the bicep motor(up or down
    self.action_space = 1
    
    
    self.write_data = True
    
    self.discrete = False
    
    self.resetPoint = 25
    self.maxSteps = 150
    
    self.goalState = 65
    self.steps = 0
    #Currently getting 1 observation, just the IMU pitch
    self.observation_space = self.getObservation()
    print('Environment has been made!')
    
    
    #I don't know if this works but hopefully it gives itself as a callable object
    return self 
    
    
    
    
  def reset(self):
    #Move arm to somewhere relevant inside of the observation space
    #return the observation and stop
    
    
    self.steps = 0
    #Todo: Add randomly generated goal states 
    #self.goalState = 45
    
    while True:
    #Get observation
      state = self.getObservation()
      
      
    
      #Move arm to the center of the observation space
      #With a really bad "controller"
      if state[0] > self.resetPoint + 1:
        self.doAction(.6)
        #self.ser.write( + '\n')
        #print('resetting up')
      elif state[0] < self.resetPoint - 1:
        self.doAction(-.6)
        #print('resetting down')
      else:
        print('Reset Complete!')
        self.currentState = self.getObservation()
        
        #Returns NP array of list of actions
        return (np.array(self.currentState))
        
        
        
  def doAction(self,action):
    #Takes an input from -1 - 1, sets this to be a value between -150 - 150
    self.ser.write((str(int(action*255)) + '\n').encode())
    
  def doDiscreteAction(self, action):
    #Move range to -action_space/2 to action_space/2
    val = (self.action_space - 1)/2.0
    temp = action - val
    #Scale from -1 to 1, keep as a float
    temp = float(temp/val)
    #print(temp)
    self.doAction(temp)
      
  def getObservation(self):
    #Gets IMU data over serial
    #Returns as tuple (X,Y,Z)
    
    
    #First IMU
    for i in range(2):
    
      #raw = self.ser.readline()
      raw = self.ser.readline()
      # raw = self.ser.readline()#don't know why but it worked so...
      raw = raw.strip()
      dev_id, xin, yin, zin = raw.decode().split(',')
      
      if dev_id is '2':
        x = float(xin)
        y = float(yin)
        z = float(zin)
      
      else:
        x2 = float(xin)
        y2 = float(yin)
        z2 = float(zin)
      

    
    
    
    
    self.currentState = np.array([z,z2])
    
    #print('Recieved Observation', self.currentState)
    self.lastZ = z
    return self.currentState
  
  def step(self, action):
    #Does the action input, gives back nextState, reward, done, info
    if self.discrete:
      self.doDiscreteAction(action)
    else:
      self.doAction(action)
    state = self.getObservation()
    self.currentState = state
    
    #TODO:Preprocess later in here but probably getObservation
    reward = self.getReward()
    done = self.goalCheck() 
    if done:
      reward += 100
    done |= self.steps > self.maxSteps
    info = ''
    
    self.steps += 1
    #print('Action chosen:', action)
    if self.steps % 25 == 0:
      print('Steps so far:',self.steps, '\tPosition:',self.currentState[0])
    return np.array(state), reward, done, info
  
  def getReward(self):
  #Takes in a state and gets the reward value
  #Currently only for linear rewards
    return float(2.0/abs(self.currentState[0] - self.goalState + .01))
    
  def goalCheck(self):
    #Return true if within a certain bounds, or at the goal`
  
    if abs(self.currentState[0] - self.goalState) > .1 or abs(self.velocityAverage) >.1:
      return False
    else:
      return True
  
  
  
    
#while True:
#    step += 1
#    raw = ser.readline()
# 
#    raw = ser.readline()
    # raw = raw.strip()
    # dev_id,x,y,z = raw.split(',')
    # x = float(x)
    # y = float(y)
    # z = float(z)
    
    # if z <= (goal[2]+.5)  and z>= (goal[2]-.5):
      
      # rewardWait += 1
     # # print 'I am waiting'
      # if rewardWait >= 20:
        # rewardWait = 0
        # arm.setGoal(goal)
    # #break
    # else:
      # reward = 0
    # action = arm.chooseAction((x,y,z), reward)

    
    # ser.write(action + '\n')
    
    
    
    
    #error = set_point - z
    #output = error * kp
    #print z,output
    #ser.write(str(output) + '\n')