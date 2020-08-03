class Greeter:
  greeting = "Hello there."
  def __init__(self):
    self.name = "John"

  def greet(self):
    print(self.greeting + " Hello my name is " + self.name)

p1 = Greeter()
p1.greet()

p1.greeting = "Guten tag."
p1.greet()