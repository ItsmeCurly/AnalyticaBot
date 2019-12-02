from random import Random

class Profile:
    def __init__(self, name, age, rel_stat, loc):
        self.name = name
        self.age = age
        self.relationship_status = rel_stat
        self.location = loc

    def display_profile(self):
        print(self.name, self.age, self.relationship_status, self.location)

a = Profile("Adam", 22, "turkey", "Orono")

a.display_profile()
