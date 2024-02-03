"""Provide the class Omforme for transformations on a generator.

Use case example:

from omforme.omforme import Omforme

Given a stream of lines e.g. in gen

gen = (x for x in ('a', 'b', 'c', 'c', 'c', 'd', '1', '2', '3', 'e'))

with defining a playbook of:

playbook = (('b', 'ignore', lambda: None), ('d', 'collect', list()), ('e', 'return', lambda: None),)

when calling

transform = Omforme(playbook)(gen)

then transform should become:

(
    ('b', 'ignore', <function <lambda> at 0x...>),
    ('d', 'collect', ['1', '2', '3']),
    ('e', 'return', <function <lambda> at 0x...>)
)

"""

import argparse
from typing import no_type_check

from omforme import DEBUG, ENCODING, ENCODING_ERRORS_POLICY, log


class Omforme:
    """Provide a generator borrowing consumer that returns the transform applying playbook to the stream.

    The playbook is a tuple of (trigger, action, function) triplets.

    Actions are epected to be within ('ignore', 'collect', 'return')

    Example:

    >>> # from omforme.omforme import Omforme
    >>> gen = (x for x in ('a', 'b', 'c', 'c', 'c', 'd', '1', '2', '3', 'e'))
    >>> playbook = (('b', 'ignore', lambda: None), ('d', 'collect', list()), ('e', 'return', lambda: None),)
    >>> transform = Omforme(playbook)(gen) # doctest: +ELLIPSIS
    0 3 a b ignore <function <lambda> at 0x...> d
    0 3 b b ignore <function <lambda> at 0x...> d
    0 3 c b ignore <function <lambda> at 0x...> d
    0 3 c b ignore <function <lambda> at 0x...> d
    0 3 c b ignore <function <lambda> at 0x...> d
    1 3 1 d collect ['1'] e
    1 3 2 d collect ['1', '2'] e
    1 3 3 d collect ['1', '2', '3'] e
    1 3 e d collect ['1', '2', '3'] e
    >>> transform[1]
    ('d', 'collect', ['1', '2', '3'])
    >>>

    """

    @no_type_check
    def __init__(self, playbook):
        """Later alligator."""
        self.playbook = playbook

    @no_type_check
    def __call__(self, gen):
        """Apply transform to generator stream of events."""
        phase = 0
        trigger, what, where_to = self.playbook[phase]
        peek = self.playbook[phase + 1][0]
        stop = len(self.playbook)
        for data in gen:
            if data == peek:
                if phase + 2 < stop:
                    phase += 1
                    trigger, what, where_to = self.playbook[phase]
                    peek = self.playbook[phase + 1][0]
                    continue
            if what == 'return':
                break
            if what == 'collect' and data != peek:
                where_to.append(data)
            print(phase, stop, data, trigger, what, where_to, peek)

        return self.playbook


def main(options: argparse.Namespace) -> int:
    log.info(f'{DEBUG=}, {ENCODING=}, {ENCODING_ERRORS_POLICY=}')
    return 0


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True, optionflags=doctest.ELLIPSIS)
