class Player:
    def __init__(self, id):
        self.ID = id
        self.points = 0
        self.ifready = False

    def addpoint(self):
        self.points += 1

    def ready(self):
        self.ifready = True

    def quit(self):
        self.ifready = False

    def clear(self):
        self.points = 0
        self.ifready = False