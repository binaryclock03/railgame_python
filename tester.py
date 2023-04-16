class Test():
    def __str__(self):
        return str(self.a)
    
    def __add__(self, a):
        self.a += a
        return self

    def __init__(self, a):
        self.a = a
    
    def do_thing(self):
        self.a += 1

b = Test(2)
test = Test(b)

print("test 1")
print(b)
print(test.a)

print("test 2")
b = b + 1
print(b)
print(test.a)

print("test 3")
test.do_thing()
print(b)
print(test.a)

print("test 4")
b = 3
print(b)
print(test.a)