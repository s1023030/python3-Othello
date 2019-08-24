class Agent:
    def __init__(self,is_human=True):
        self.is_human=is_human
        
class Human(Agent):
    def __init__(self,is_human=True):
        super().__init__(is_human)

class AI_factory:
    def generate_AI(AI_type=""):
        return {
            "Random":AI_Random()
        }[AI_type]

class AI(Agent):
    def __init__(self,is_human=False):
        super().__init__(is_human)
    def placing_desk(self,winner,you_are,board,reward,poss_next_steps):
        pass

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

