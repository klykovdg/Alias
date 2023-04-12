class Team:
    def __init__(self, name):
        self.name = name
        self.score = 0

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def up(self):
        self.score += 1

    def down(self):
        if self.score > 0:
            self.score -= 1

    def reset_score_to_zero(self):
        self.score = 0


