class Income:
    def __init__(self, amount, source, date):
        self.amount = amount
        self.source = source
        self.date = date

    def __str__(self):
        return f"Income({self.amount}, {self.source}, {self.date})"
