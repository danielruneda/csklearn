

class PersonForBMI:

    def __init__(self, age, weight, height, gender):

        self.age = age
        self.weight = weight
        self.height = height
        self.gender = gender


    def calculate_bmi(self):
        if self.gender.upper() == 'MALE':
            self.bmi = self.weight / (self.height/100 * self.height/100) * .98
        elif self.gender.upper() == 'FEMALE':
            self.bmi = self.weight / (self.height/100 * self.height/100) * .94

        return self.bmi

    
    def conclusions(self):
        print('ASDF')
