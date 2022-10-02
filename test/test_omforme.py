from omforme.omforme import Omforme


def test_omforme():
    gen = (x for x in ('a', 'b', 'c', 'c', 'c', 'd', '1', '2', '3', 'e'))
    playbook = (
        ('b', 'ignore', lambda: None),
        ('d', 'collect', list()),
        ('e', 'return', lambda: None),
    )
    transform = Omforme(playbook)(gen)
    assert transform[1] == ('d', 'collect', ['1', '2', '3'])
