class Budget:
    def __init__(self, category, limit, period):
        self.category = category
        self.limit = limit
        self.period = period

    def is_over_budget(self, expenses):
        total = sum(exp.amount for exp in expenses if exp.category == self.category)
        return total > self.limit
