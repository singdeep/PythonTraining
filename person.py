# Define a class named Person in a module named person.py
class Person:
    def __init__(self, name):
        self.name = name
    
    def say_hello(self):
        print(f"Hello, my name is {self.name}.")

# Define another class named Animal in the same module
class Animal:
    def __init__(self, species):
        self.species = species
    
    def say_species(self):
        print(f"I am a {self.species}.")