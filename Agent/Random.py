from Agent.Agent import AI
class AI_Random(AI):
    def __init__(self,is_human=False):
        super().__init__(is_human)
    def placing_desk(self,winner,you_are,board,reward,poss_next_steps):
        if winner>-1:
            pass
        import random
        secure_random = random.SystemRandom()
        if len(poss_next_steps)>0:
            return secure_random.sample(poss_next_steps,1)
        else:
            return [(-1,-1)]
