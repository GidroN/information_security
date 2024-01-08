class DateTimeCalculator:
    def __init__(self, start: str, period: str, weekday: str = None):
        self.start = start
        self.period = period
        self.weekday = weekday

    def calculate(self):
        ...


