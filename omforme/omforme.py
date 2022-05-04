"""Provide the class Omforme for transformations on a generator.

Use case example: Given a stream of lines e.g. in gen

gen = (x for x in ('a', 'b', 'c', 'c', 'c', 'd', '1', '2', '3', 'e'))

with defining a playbook of:

playbook = (
    ('b', 'ignore', lambda: None),
    ('d', 'collect', list()),
    ('e', 'return', lambda: None),
)

when calling

transform = Omforme(playbook)(gen)


"""

class Omforme:
    """Provide a generator borrowing consumer that returns the transform applying playbook to the stream.

    The playbook is a tuple of (trigger, action, function) triplets.

    Actions are epected to be within ('ignore', 'collect', 'return')

    """
    def __init__(self, playbook):
        """Later alligator."""
        self.playbook = playbook

    def __call__(self, gen):
        """Apply transform to generator stream of events."""
        phase = 0
        trigger, what, where_to = self.playbook[phase]
        for data in gen:
            if data == trigger:
                if phase + 2 < len(self.playbook):
                    phase += 1
                    trigger, what, where_to = self.playbook[phase]
                    continue
            else:
                if what == 'collect':
                    where_to.append(data)
        return self.playbook
