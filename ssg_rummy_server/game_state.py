import attr


@attr.s
class GameState:
    actions = attr.ib()

    @classmethod
    def create(cls):
        return cls([])

    def act(self, user, action):
        self.actions += [(user, action)]
        return self.summary()
    
    def summary(self):
        return str(self)