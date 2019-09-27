from Agent.Random import AI_Random

class AI_factory:
    def generate_AI(AI_type=""):
        return {
            "Random":AI_Random()
        }[AI_type]