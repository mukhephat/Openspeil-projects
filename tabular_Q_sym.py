# Copyright 2019 DeepMind Technologies Ltd. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tabular Q-learning agent."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import numpy as np

import rl_agent
import rl_tools


class QLearner(rl_agent.AbstractAgent):
  
  """Tabular Q-Learning agent.

  See open_spiel/python/examples/tic_tac_toe_qlearner.py for an usage example.
  """

  def __init__(self,
               player_id,
               num_actions,
               step_size=0.1,
               epsilon_schedule=rl_tools.ConstantSchedule(0.2),
               discount_factor=1.0):
    """Initialize the Q-Learning agent."""
    self._player_id = player_id
    self._num_actions = num_actions
    self._step_size = step_size
    self._epsilon_schedule = epsilon_schedule
    self._epsilon = epsilon_schedule.value
    self._discount_factor = discount_factor
    self._q_values = collections.defaultdict(
        lambda: collections.defaultdict(float))
    self._prev_info_state = None
    self._last_loss_value = None

  
#____________________________________________________
  def flipBoard(self,board):    
    boardR = ['','',''],['','',''],['','','']
    
    line0 = board[2]
    line1 = board[1]
    line2 = board[0]    
    boardFh = [line0,line1,line2]

    return boardFh

  def rotBoard(self,boardL):
    numBoard = []
    index = 1
    for i in range(27):
       numBoard.append(boardL[index])
       index+=5
        
    #print('Rot board',numBoard)  
    board = self.unconvertBoard((numBoard))
    #print('unconvert board',board)  
    boardOrig = board
    brdf = self.flipBoard(boardOrig)
    boardR = board
    for i in range(3):

        #print('i',i) 

        board = boardR 
        board = np.array(board)
        #print(type(board)) 
        boardR = ['','',''],['','',''],['','','']
        line0 = board[0,:]
        line1 = board[1,:]
        line2 = board[2,:]    
        #print(line0) 
        #print(line1) 
        #print(line2) 
        L1 = [line2[0],line1[0],line0[0]]
        L2 = [line2[1],line1[1],line0[1]]
        L3 = [line2[2],line1[2],line0[2]]   
        boardR = [L1,L2,L3]
        boardf = self.flipBoard(boardR)
        #print('Board rot',np.array(boardR))
        #print('Board flip',np.array(boardf))
        #print(line2)
        if i == 0:
            b90 = boardR
            b90f = boardf
        elif i == 1:
            b180 = boardR
            b180f = boardf
        else:
            b270 = boardR
            b270f = boardf

    boardOrig = list(self.convertBoard(boardOrig))
    brdf = list(self.convertBoard(brdf))
    b90 = list(self.convertBoard(b90))
    b90f = list(self.convertBoard(b90f))
    b180 = list(self.convertBoard(b180))
    b180f = list(self.convertBoard(b180f))
    b270 = list(self.convertBoard(b270))
    b270f = list(self.convertBoard(b270f))

    return boardOrig,brdf,b90,b90f,b180,b180f,b270,b270f

  def convertBoard(self,board):    
    board = np.array(board)
    #print('Type',type(board))
    bList0 = np.zeros(9)
    bListO= np.zeros(9)
    bListX = np.zeros(9)
    counter = -1

    for i in range(3):
        for j in range(3):
            counter +=1
            #print(counter)
            if board[i,j] == "":
                bList0[counter] = 1
            elif board[i,j] == "X":
                bListX[counter] = 1
            elif board[i,j] == "O":
                bListO[counter] = 1
            #print(bList0)
            #print(bListX)
            #print(bListO)
        new =  np.append(bList0,(bListO,bListX))
    #print('New appended list 0OX',new)
    return new


  def unconvertBoard(self,board):
    #print('shape board unconvert',len(board))
    bList0 = board[0:9]
    #print(bList0)
    bListO=  board[9:18]
    #print(bListO)
    bListX = board[18:27]
    #print(bListX)
    bGrid = np.zeros((3,3),str)
    counter = -1
    for i in range(3):
        for j in range(3):
            counter +=1
            #print(counter)
            if bListO[counter] == '1':
                bGrid[i,j] = "O"
            elif bListX[counter] == '1':
                bGrid[i,j] = "X"
            #print(bGrid)
            #print(bListX)
            #print(bListO)
    return bGrid

  def convertMove(self,move):
    #if move == None:
        #return [0,0,0,0,0,0,0,0]
    #print('The move',move)
    move = str(move)
    dictn = {'0':[0,6,2,8,8,2,6,0]
            ,'1':[1,7,5,5,7,1,3,3]
            ,'2':[2,8,8,2,6,0,0,6]
            ,'3':[3,3,1,7,5,5,7,1]
            ,'4':[4,4,4,4,4,4,4,4]
            ,'5':[5,5,7,1,3,3,1,7]
            ,'6':[6,0,0,6,2,8,8,2]
            ,'7':[7,1,3,3,1,7,5,5]
            ,'8':[8,2,6,0,0,6,2,8]
            }
    return(dictn[move])
#________________

    
  def _epsilon_greedy(self, info_state, legal_actions, epsilon):
    """Returns a valid epsilon-greedy action and valid action probs.

    If the agent has not been to `info_state`, a valid random action is chosen.

    Args:
      info_state: hashable representation of the information state.
      legal_actions: list of actions at `info_state`.
      epsilon: float, prob of taking an exploratory action.

    Returns:
      A valid epsilon-greedy action and valid action probabilities.
    """
    #a = self._num_actions
    #print('Test to see',a)
    probs = np.zeros(self._num_actions)
    
    #print('From TQ the num_actions',self._num_actions)
    #print('From TQ the probs',probs)
    #print('The q_values in TQ',self._q_values)
    #print('The legal actions in TQ',legal_actions)
    greedy_q = max([self._q_values[info_state][a] for a in legal_actions])
    greedy_actions = [
        a for a in legal_actions if self._q_values[info_state][a] == greedy_q
    ]
    #print('greedy_actions',greedy_actions)     
    #print('Probs[]',probs[legal_actions])
    #print('e/len',epsilon/len(legal_actions))
    #print('Greedy[]',probs[greedy_actions])
    #print('e/len',(1-epsilon)/len(greedy_actions))    
    
    probs[legal_actions] = epsilon / len(legal_actions)
    #print('explore',probs)
    probs[greedy_actions] += (1 - epsilon) / len(greedy_actions)
    #print('exploit',probs)
    action = np.random.choice(range(self._num_actions), p=probs)
        
    return action, probs

  def step(self, time_step, is_evaluation=False):
    #print(is_evaluation)
    """Returns the action to be taken and updates the Q-values if needed.

    Args:
      time_step: an instance of rl_environment.TimeStep.
      is_evaluation: bool, whether this is a training or evaluation call.

    Returns:
      A `rl_agent.StepOutput` containing the action probs and chosen action.
    """
    info_state = str(time_step.observations["info_state"][self._player_id])
    legal_actions = time_step.observations["legal_actions"][self._player_id]

    # Prevent undefined errors if this agent never plays until terminal step
    action, probs = None, None

    # Act step: don't act at terminal states.
    if not time_step.last():
      #print('QLearner time step',time_step.last())
      epsilon = 0.0 if is_evaluation else self._epsilon
      action, probs = self._epsilon_greedy(
          info_state, legal_actions, epsilon=epsilon)

    # Learn step: don't learn during evaluation or at first agent steps.
    if self._prev_info_state and not is_evaluation:
      target = time_step.rewards[self._player_id]
      #print('target initial',self._player_id,time_step.rewards)
      
      
      if not time_step.last():  # Q values are zero for terminal.
        target += self._discount_factor * max(
            [self._q_values[info_state][a] for a in legal_actions])
      
      prev_q_value = self._q_values[self._prev_info_state][self._prev_action]
      self._last_loss_value = target - prev_q_value
      self._q_values[self._prev_info_state][self._prev_action] += (
          self._step_size * self._last_loss_value)
      x = self._prev_action 
      moves8 = self.convertMove(x)
      y = self._prev_info_state
      #print('Prev check',y)
      infoState8 = self.rotBoard(y)
      #print('Info state8',infoState8)
      lValue8 = self._last_loss_value
      
      step8 = self._step_size
      #print('len in Q', len(self._q_values))
      for i in range(8):
          #print('\n_____',i)
          stateX = (infoState8[i])
          #print('StateX',stateX)
          move8 = moves8[i]
          
          #print('Q',(stateX))
          #print('Q',move8)
          #print('prev',(self._prev_info_state))
          #print('Mv',self._prev_action)
          #print(self._q_values[stateX])  
          self._q_values[str(stateX)][move8] += (step8 * lValue8)
            
      #print('len2 in Q', len(self._q_values))

      #print('Prev info state',self._prev_info_state)
      #print('Prev action',self._prev_action)
      #print('The target',target,prev_q_value)
      # Decay epsilon, if necessary.
      self._epsilon = self._epsilon_schedule.step()

      if time_step.last():  # prepare for the next episode.
        self._prev_info_state = None
        return

    # Don't mess up with the state during evaluation.
    if not is_evaluation:
      self._prev_info_state = info_state
      self._prev_action = action
    return rl_agent.StepOutput(action=action, probs=probs)

  @property
  def loss(self):
    return self._last_loss_value

