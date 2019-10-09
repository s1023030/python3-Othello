from Agent.Agent import AI
import random
import numpy as np
class AI_Random(AI):
    def __init__(self,is_human=False):
        super().__init__(is_human)
    def placing_desk(self,winner,you_are,board,reward,poss_next_steps):
        '''
        board
        00  10  20  30  40  50  60  70
        01  11  21  31  41  51  61  71
        02  12  22  32  42  52  62  72
        03  13  23  33  43  53  63  73
        04  14  24  34  44  54  64  74
        05  15  25  35  45  55  65  75
        06  16  26  36  46  56  66  76
        07  17  27  37  47  57  67  77
        '''

        if winner>-1:
            pass
        secure_random = random.SystemRandom()
        print(you_are)
        print(reward)
        print("=====================")
        if len(poss_next_steps)>0:
            return secure_random.sample(poss_next_steps,1)
        else:
            return [(-1,-1)]

