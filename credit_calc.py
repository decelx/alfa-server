class Calculator:
    def __init__(self, age, married, job):
        self.age = age
        self.married = married
        self.job = job

    def calculate(self):
        if 20 <= self.age < 30:
            if self.married == True and self.job == True:
                return True
            if self.married == False and self.job == True:
                return False
            if self.married == True and self.job == False:
                return False

        if 30 <= self.age < 40:
            if self.married == True and self.job == True:
                return True
            if self.married == False and self.job == True:
                return True
            if self.married == True and self.job == False:
                return False

        if 40 <= self.age < 50:
            if self.married == True and self.job == True:
                return True
            if self.married == False and self.job == True:
                return True
            if self.married == True and self.job == False:
                return True

        if 50 <= self.age < 60:
            if self.married == True and self.job == True:
                return True
            if self.married == False and self.job == True:
                return True
            if self.married == True and self.job == False:
                return False
        else:
            return False