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
