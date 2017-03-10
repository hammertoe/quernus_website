---
layout: post
title: Testing Randomness in Python
comments: True
tags: python, testing, random
summary: I needed to be able to unit test some python code that had a random element to it. Here's how I made it deterministic.
---

In a side project I've been working on recently I've needed to write unit tests for some methods that return a non-deterministic random result. 

In this case there was a method that would simulate an event happening based on some kind of probability factor. Eg if the factor was `0.2` then the event would happen on average every fifth time the method was called. It is pretty hard to unit test the outcome of that as the tests will fail 4/5 of the time. I needed to test that if I called that method 100 times with a factor of `0.2` that the event would happen roughly 20 times. Although of course sometimes it would be 19 times, sometimes 21. How do you test that?

After lots of messing about trying to Mock the random number generator and the random functions I discovered a much simpler approach. The random number generator on a computer is never actually truly random. It is a pseudo-random number generator (PRNG) which is in turn seeded with some 'randomness', eg the interrupts from the disk and network controller. But given the same seed the PNRG will always produce the same sequence of numbers when called. 

So all I have to do is seed the PNRG with a known value before my test and the test outcome will always be deterministic. 

An example below in Python, but most other languages have a similar `seed()` function. 

```python
import random

class MyClass:
  samples = ['a', 'b', 'c', 'd', 'e']

  def pickone():
    return random.choice(samples)

class MyTests():

  def testPickOne():
    random.seed(0)
    picker = MyClass()
    choice = picker.pickone()
    self.assertEqual(choice, 'c')

if __class__ == '__main__':
  Tests

```

You don't know what the outcome is going to be the first time you run the test. So you are likely to have to run it and then substitute in the returned value. 

Actually in Python we can make this even nicer by using a decorator. In this way we can write a decorator that stores the random seed before we reset it and restores if afterward:

```python
from decorator import decorator
import random

@decorator
def fix_random(f, *args, **kw):
    state = random.getstate()
    random.seed(0)
    res = f(*args, **kw)
    random.setstate(state)
    return res
```

or even as a context manager:

```python
import random
class FixRandom():

    def __enter__(self):
        self.state = random.getstate()
        random.seed(0)

    def __exit__(self, *args):
        random.setstate(self.state)
```

and can then be used:

```python
print random.randint(0,100)

for i in range(10):
  with FixRandom():
    print random.randint(0,100)

print random.randint(0,100)
```

As you can see, produces the same ‘random’ number when called within the context, but an actual random one outside.

```
93
85
85
85
85
85
85
85
85
85
85
43
```