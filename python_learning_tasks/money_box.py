class MoneyBox:
    def __init__(self, capacity):
        self.curr = 0
        self.lim = capacity

    def can_add(self, v):
        if self.curr + v <= self.lim:
            return True
        else:
            return False

    def add(self, v):
        if self.can_add(v):
            self.curr += v