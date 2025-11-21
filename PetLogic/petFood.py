class Food():
    def __init__(self):
        self.restoration = 0 # amount of hunger decreased 
        self.price = 0 # price of the food


class Cupcake(Food):
    def __init__(self):
        self.restoration = 10 # decreases hunger by 10 
        self.price = 5
    
