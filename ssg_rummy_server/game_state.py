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
        while True:
            cards = shuffled_deck(3)
            hands = {}
            for name in names:
                hands[name] = cards[:CARDS_PER_USER]
                cards = cards[CARDS_PER_USER:]
            joker = cards[0]
            if joker == ["$", "$"]:
                continue
            cards = cards[1:]
            discard_pile = [cards[0]]
            cards = cards[1:]
            break
        return cls(
            names=names,
            joker=joker,
            hands_per_user=hands,
            draw_pile=cards,
            discard_pile=discard_pile,
            next_valid_action=(names[0], "draw"),
            actions=[],
        )

    def act(self, user, action):
        self.actions += [(user, action)]
        action = action.copy()
        typ = action.pop("type")
        methods = {
            "view": self.view,
            "update-order": self.update_order,
            "draw-shown": self.draw_shown,
            "draw-hidden": self.draw_hidden,
            "throw": self.throw,
        }
        if typ not in methods:
            print("ERROR: unrecognized", typ, flush=True)
            return
        methods[typ](user, **action)

    def view(self, user):
        pass

    def update_order(self, user, new_order):
        if sorted(tuple(x) for x in self.hands_per_user[user]) == sorted(
            tuple(x) for x in new_order
        ):
            self.hands_per_user[user] = new_order
        else:
            print("ERROR: invalid order", flush=True)
            print(sorted(self.hands_per_user[user]))
            print(sorted(tuple(x) for x in new_order))
            # TODO handle error
            pass

    def draw_shown(self, user):
        if self.next_valid_action != (user, "draw"):
            # TODO handle error
            return
        # there should always be at least one card in the draw pile
        self.hands_per_user[user] += [self.discard_pile.pop()]
        self.next_valid_action = (user, "throw")
        self.actions += [(user, {"type": "draw-shown"})]

    def draw_hidden(self, user):
        if self.next_valid_action != (user, "draw"):
            # TODO handle error
            return
        # TODO handle case where draw pile is empty, should reshuffle discard pile
        self.hands_per_user[user] += [self.draw_pile.pop()]
        self.next_valid_action = (user, "throw")
        self.actions += [(user, {"type": "draw-hidden"})]

    def throw(self, user, card, index):
        if self.next_valid_action != (user, "throw"):
            # TODO handle error
            return
        if tuple(self.hands_per_user[user][index]) != tuple(card):
            # TODO handle error
            return

        self.hands_per_user[user].pop(index)
        self.discard_pile += [card]
        self.next_valid_action = (self.next_user(user), "draw")
        self.actions += [(user, {"type": "throw", "card": card, "index": index})]

    def serialize(self):
        return {a.name: getattr(self, a.name) for a in self.__attrs_attrs__}

    def summary(self, user):
        return json.dumps(
            dict(
                next_valid_action=self.next_valid_action,
                joker=self.joker,
                discarded=self.discard_pile[-1] if self.discard_pile else None,
                hand=self.hands_per_user[user],
                state=self.serialize(),
            )
        )

    def next_user(self, user):
        return self.names[(self.names.index(user) + 1) % len(self.names)]
