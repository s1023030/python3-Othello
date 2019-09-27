from Agent.Agent import AI
class AI_DL(AI):
    def __init__(self,is_human=False):
        super().__init__(is_human)
        self.name = 'AI_DL'


    def placing_desk(self,winner,you_are,board,reward,poss_next_steps):
        if winner>-1:
            pass
        else:
            return [(-1,-1)]

    def construct_network(self):
        pass