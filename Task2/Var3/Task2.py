import random
import math


class Box:
    def __init__(self, **balls):
        self.balls = []
        self.total_balls = len(self.balls)
        for color, count in balls.items():
            self.balls.extend([color] * count)

    def calculate_probability(self, balls: dict) -> tuple[float, float]:
        color_comb = 1
        total_balls_chosen = 0

        for color, count in balls.items():
            color_comb *= math.comb(self.balls.count(color), count)
            total_balls_chosen += count

        total_comb = math.comb(len(self.balls), total_balls_chosen)
        result = color_comb / total_comb

        return round(result * 100, 3), round(result, 3)


if __name__ == '__main__':
    box = Box(black=5, white=5, red=5, blue=5)
    print(box.calculate_probability({'black': 1, 'blue': 1, 'red': 1, 'white': 1}))