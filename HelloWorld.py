# Import the person module and create instances of its classes
import pyttsx3
#import person 

#person1 = person.Person("Alice")
#person1.say_hello()

#animal1 = person.Animal("Dog")
#animal1.say_species()

engine = pyttsx3.init()
engine.say("Hello, World!")
engine.runAndWait()