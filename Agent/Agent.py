class Agent:
    def __init__(self,is_human=True):
        self.is_human=is_human
        
class Human(Agent):
    def __init__(self,is_human=True):
        super().__init__(is_human)

'''class AI_factory:
    def generate_AI(AI_type=""):
        return {
            "Random":AI_Random()
        }[AI_type]'''

class AI(Agent):
    def __init__(self,is_human=False):
        super().__init__(is_human)

    def new_episode(self):
        pass

    def placing_desk(self,winner,you_are,board,reward,poss_next_steps):
        pass

