import random


class Box:
    def __init__(self, **balls):
        self.balls = balls

    def draw_balls(self, attempts):
        drawn_balls = []
        for _ in range(attempts):
            ball_color = random.choice(list(self.balls.keys()))
            drawn_balls.append(ball_color)
        return drawn_balls


def counter(box, expects, nums, num_exp):
    success_count = 0

    for _ in range(num_exp):
        drawn_balls = box.draw_balls(nums)
        ball_count = {color: drawn_balls.count(color) for color in set(drawn_balls)}

        if all(ball_count.get(color, 0) >= count for color, count in expects.items()):
            success_count += 1

    probability = success_count / num_exp
    return probability


if __name__ == '__main__':
    box1 = Box(черный=5, синий=3, зеленый=8)
    expected_result = {'черный': 2, 'зеленый': 3}
    num_attempts = 8
    num_experiments = 1000

    probability = counter(box=box1, expects=expected_result, nums=num_attempts, num_exp=num_experiments)
    print(f"Вероятность вытащить {expected_result} за {num_attempts} попыток: {probability}")
