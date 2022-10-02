# Command Line API

Use the python help command to learn about the API.

## Example

Transformations on a generator. Use case example:

```python
from omforme.omforme import Omforme
```

Given a stream of lines e.g. in gen

```python
gen = (x for x in ('a', 'b', 'c', 'c', 'c', 'd', '1', '2', '3', 'e'))
```

with defining a playbook of:

```python
playbook = (('b', 'ignore', lambda: None), ('d', 'collect', list()), ('e', 'return', lambda: None),)
```

when calling

```python
transform = Omforme(playbook)(gen)
```

then transform should become:

```python
(
    ('b', 'ignore', <function <lambda> at 0x...>),
    ('d', 'collect', ['1', '2', '3']),
    ('e', 'return', <function <lambda> at 0x...>)
)
```

## Interactive Example

Provide a generator borrowing consumer that returns the transform applying playbook to the stream.

The playbook is a tuple of (trigger, action, function) triplets.

Actions are epected to be within ('ignore', 'collect', 'return')

### Doctest from Implementation

```python
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
```
