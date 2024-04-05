a = 2
self = 4
class A():
    def __init__(self,a):
        self.a = a
        
    def funct(self):
        print(self.a)
        print(a)
    

A(3).funct()
print(self)