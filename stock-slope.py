
class Company:
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return str(self.__dict__.keys())
        
apple_company = Company("Apple")

print apple_company



