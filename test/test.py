# hello.py

def hello():
    print("hello")
    
class Content:
    def __init__(self, x):
        self._x = x
        
    @property
    def x(self):
        return self._x

    def __repr__(self):
        return f"Content [x = {self.x}]"
    
class Container:
    def __init__(self, contents):
        self.contents = contents
        
    @property
    def first(self):
        return self.contents[0]

# main.py

import math

hello()
print(math.pow(2, 2))

contents = [Content(1), Content(2)]
container = Container(contents)
print(container.first)
container.first.x = 3
print(container.first)
