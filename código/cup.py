class Cup:

    def __init__(self, weight_limit, filling_rate):

        self.state  = 0
        self.weight = 0
        self.weight_limit = weight_limit
        self.filling_rate = filling_rate

    def has_overwight(self):

        return  self.weight > self.weight_limit

    def fill(self):

        self.weight += self.filling_rate