"""
This Python code snippet illustrates how to set up the bot
"""
import numpy as np
import random
# import other packages here

"""
CODE SUBMISSION TEMPLATE
"""
class player:
    def __init__(self):
        pass

    def move(self,B,N,cur_x,cur_y): 
        """
        This function decides how a bot moves within the grid. That is, the participants can code their strategy in this function.
        Input:
            B: the board (list of lists of 30 element each)
            N: the size of the N x N board (N=30 by default)
            cur_x: current x location of this bot
            cur_y: current y location of this bot
        Return:
            The function returns the direction (via the variable Direction) in which the bot should move next.
            Direction: This is a tuple that can hold either of the following values:
                (0,0)   : don't move
                (-1,0)  : move left
                (1,0)   : move right
                (0,-1)  : move up
                (0,1)   : move down
        """
        
        # Compute how the bot will move (i.e., how the value of the variable Direction is computed)
        # Function body - BEGINS
        
        # Function body - END
        return Direction 