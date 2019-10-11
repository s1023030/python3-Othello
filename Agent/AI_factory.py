from Agent.Random import AI_Random
from Agent.DQN import AI_DQN

class AI_factory:
    def generate_AI(AI_type=""):
        return {
            "Random":AI_Random(),
            "DQN":AI_DQN()
        }[AI_type]