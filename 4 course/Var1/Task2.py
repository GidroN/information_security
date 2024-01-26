from datetime import datetime, timedelta


class DateTimeCalculator:
    WEEKDAYS = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]

    def __init__(self, start: str, period: str, weekday: str = None):
        self.start = start
        self.period = period
        self.weekday = weekday

    def calculate(self):
        start_time = datetime.strptime(self.start, '%I:%M %p')
        hours, minutes = map(int, self.period.split(':'))
        final_time = start_time + timedelta(hours=hours, minutes=minutes)
        days_passed = final_time.day - start_time.day
        result_time = final_time.strftime('%I:%M %p')

        if self.weekday:
            start_weekday_idx = self.WEEKDAYS.index(self.weekday.capitalize())
            final_weekday_idx = (start_weekday_idx + days_passed) % 7
            final_weekday = self.WEEKDAYS[final_weekday_idx]
            result_time += ', ' + final_weekday

        if days_passed == 1:
            result_time += ' (следующего дня)'
        elif days_passed > 1:
            result_time += f' ({days_passed} дней позже)'

        return result_time


if __name__ == '__main__':
    calc = DateTimeCalculator('11:47 PM', '24:20', 'вторник')
    print(calc.calculate())
