import json
import attr

from .deck import shuffled_deck

CARDS_PER_USER = 21


@attr.s
class GameState:
    names = attr.ib()
    joker = attr.ib()
    hands_per_user = attr.ib()
    draw_pile = attr.ib()
    discard_pile = attr.ib()

    next_valid_action = attr.ib()
    actions = attr.ib()

    @classmethod
    def create(cls, names):
        cards = shuffled_deck(3)
        hands = {}
        for name in names:
            hands[name] = cards[:CARDS_PER_USER]
            cards = cards[CARDS_PER_USER:]
        joker = cards[0]
        cards = cards[1:]
        discard_pile = [cards[0]]
        cards = cards[1:]
        return cls(
            names=names,
            joker=joker,
            hands_per_user=hands,
            draw_pile=cards,
            discard_pile=discard_pile,
            next_valid_action=[(names[0], "draw")],
            actions=[],
        )

    def act(self, user, action):
        self.actions += [(user, action)]
        return self.summary(user)

    def serialize(self):
        return {a.name: getattr(self, a.name) for a in self.__attrs_attrs__}

    def summary(self, user):
        return json.dumps(dict(hand=self.hands_per_user[user], state=self.serialize()))
