class Uid:
    name = 'hisheng'
    age = 1
    def __init__(self):
        self.age += 1

    def displayNmae(self):
        print('my name is ' + self.name)

    def displayAge(self):
        print('my age is '+ str(self.age))





uid1 = Uid()
print(uid1.age)
print(uid1.name)
uid1.displayAge()
uid1.displayNmae()